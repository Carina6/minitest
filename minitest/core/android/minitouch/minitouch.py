#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import re
import socket
import time
from pathlib import Path

from retry import retry

from logger import get_logger
from minitest.core.android.minitouch import MINITOUCH_PATH
from minitest.core.android.minitouch.exceptions import MinitouchException
from minitest.core.helper import on_method_ready, logwrap
from minitest.core.utils.non_blocking_stream_reader import NonBlockingStreamReader
from minitest.core.utils.simple_socket import *

LOGGER = get_logger(__name__)


class Minitouch(object):
    def __init__(self, adb):
        self.adb = adb
        self.dir = '/data/local/tmp'

        self.local_port = None
        self.device_port = None
        self.server_process = None

        self.max_x = 32767
        self.max_y = 32767

        self.client = None

    def install_server(self):
        abi = self.adb.shell_command('getprop ro.product.cpu.abi')[0]
        sdk_version = int(self.adb.shell_command('getprop ro.build.version.sdk')[0])

        minitouch_bin = 'minitouch' if sdk_version >= 16 else 'minitouch-nopie'

        minitouch_bin_path = Path.joinpath(MINITOUCH_PATH, abi, minitouch_bin)
        self.adb.push_local_file(str(minitouch_bin_path), '{}/minitouch'.format(self.dir))
        self.adb.shell_command('chmod 755 {}/minitouch'.format(self.dir))

    def uninstall_server(self):
        self.adb.shell_command('rm -rf {}/minitouch*'.format(self.dir))

    def start_server(self):
        def before_start(server_process):
            if server_process is not None:
                server_process.kill()

        def after_start():
            pass

        def start(adb):
            @retry(exceptions=MinitouchException, tries=3)
            def get_local_port(adb):
                candidate_port = random.randint(30000, 32000)
                _, outputs = adb.run_cmd(['forward', '--list'])

                for output in outputs:
                    if 'tcp:{}'.format(candidate_port) in output:
                        raise MinitouchException('candidate port() is not available.'.format(candidate_port))

                return candidate_port

            self.local_port = get_local_port(adb)
            self.device_port = 'minitouch_{}'.format(self.local_port)
            adb.forward_socket('tcp:{}'.format(self.local_port), 'localabstract:{}'.format(self.device_port))

            process = adb.shell_command_ext('{}/minitouch -n {} 2>&1'.format(self.dir, self.device_port))
            stream_reader = NonBlockingStreamReader(process.stdout)

            while True:
                line = stream_reader.readline(timeout=5.0)
                if line is None:
                    raise RuntimeError('minitouch setup timeout!')

                line = line.decode('utf-8')

                m = re.match("Type \w touch device .+ \((\d+)x(\d+) with \d+ contacts\) detected on .+ \(.+\)", line)
                if m is not None:
                    self.max_x = int(m.group(1))
                    self.max_y = int(m.group(2))
                    break

            if process.poll() is not None:
                raise RuntimeError('minitouch server quit immediately')

            self.server_process = process
            return process

        before_start(self.server_process)
        start(self.adb)
        after_start()

    def kill_server(self):
        pass

    def start_client(self):
        self.client = SimpleClient(host='localhost', port=self.local_port)
        self.client.connect()

        def test_connection(client):
            data = ''
            while True:
                try:
                    data += client.receive(4096)

                    if data.count('\n') >= 3:
                        break
                except socket.timeout:
                    break

        test_connection(self.client)

    def kill_client(self):
        self.client.close()

    def install_and_set_up(self):
        self.install_server()
        self.start_server()
        self.start_client()

    def __convert_xy(self, xy):
        x, y = xy

        return tuple(x, y)

    # tap or long tap depends on interval
    @on_method_ready('install_and_set_up')
    @logwrap(LOGGER)
    def touch(self, xy, interval=0.01):
        '''
        https://github.com/openstf/minitouch
        
        Tap on (10, 10) with 50 pressure using a single contact.

        d 0 10 10 50
        c
        u 0
        c
        
        '''

        x, y = xy

        self.client.send("d 0 {:.0f} {:.0f} 50\nc\n".format(x, y))
        time.sleep(interval)
        self.client.send("u 0\nc\n")

    @on_method_ready('install_and_set_up')
    @logwrap(LOGGER)
    def touch_two_point(self, pos1, pos2, interval=0.01):
        '''
        https://github.com/openstf/minitouch

        Tap on (10, 10) and (20, 20) simultaneously with 50 pressure using two contacts.

        d 0 10 10 50
        d 1 20 20 50
        c
        u 0
        u 1
        c

        '''

        x1, y1 = pos1
        x2, y2 = pos2

        self.client.send("d 0 {:.0f} {:.0f} 50\nd 1 {:.0f} {:.0f} 50\nc\n".format(x1, y1, x2, y2))
        time.sleep(interval)
        self.client.send("u 0\nu 1\nc\n")

    @on_method_ready('install_and_set_up')
    @logwrap(LOGGER)
    def swipe(self, from_xy, to_xy, interval=0.1, steps=5):
        '''
        https://github.com/openstf/minitouch
        
        Swipe from (0, 0) to (100, 0) using a single contact. You'll need to wait between commits in your own code to slow it down.

        d 0 0 0 50
        c
        m 0 20 0 50
        c
        m 0 40 0 50
        c
        m 0 60 0 50
        c
        m 0 80 0 50
        c
        m 0 100 0 50
        c
        u 0
        c
        
        '''
        from_x, from_y = from_xy
        to_x, to_y = to_xy

        self.client.send("d 0 {:.0f} {:.0f} 50\nc\n".format(from_x, from_y))
        time.sleep(interval)

        for i in range(1, steps):
            self.client.send("m 0 {:.0f} {:.0f} 50\nc\n".format(
                from_x + (to_x - from_x) * i / steps,
                from_y + (to_y - from_y) * i / steps,
            ))
            time.sleep(interval)
        for i in range(steps):
            self.client.send("m 0 {:.0f} {:.0f} 500\nc\n".format(to_x, to_y))
            time.sleep(interval)
        self.client.send("u 0\nc\n")

    @on_method_ready('install_and_set_up')
    @logwrap(LOGGER)
    def pinch(self, *args, **kwargs):
        raise MinitouchException()
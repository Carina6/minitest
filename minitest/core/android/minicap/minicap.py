#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from pathlib import Path

from logger import get_logger
from minitest.core.android.minicap import MINICAP_PATH, MINICAP_SHARED_PATH
from minitest.core.helper import on_method_ready, logwrap

LOGGER = get_logger(__name__)


class Minicap(object):
    def __init__(self, adb):
        self.adb = adb
        self.dir = '/data/local/tmp'

    @on_method_ready('install')
    @logwrap(LOGGER)
    def wake_up(self):
        is_slept = self.adb.shell_command('dumpsys window policy|grep mScreenOnFully|grep false')
        if is_slept:
            self.adb.shell_command('input keyevent 26')
            self.adb.shell_command('input swipe 500 700 500 50')

    def install(self):
        abi = self.adb.shell_command('getprop ro.product.cpu.abi')[0]
        pre_sdk_version = int(self.adb.shell_command("getprop ro.build.version.preview_sdk")[0])
        sdk_version = int(self.adb.shell_command('getprop ro.build.version.sdk')[0])
        rel_version = int(self.adb.shell_command('getprop ro.build.version.release')[0].split('.')[0])

        sdk_version = sdk_version + 1 if pre_sdk_version > 0 else sdk_version
        minicap_bin = 'minicap' if sdk_version >= 16 else 'minicap-nopie'

        minicap_bin_path = Path.joinpath(MINICAP_PATH, abi, minicap_bin)
        self.adb.push_local_file(str(minicap_bin_path), '{}/minicap'.format(self.dir))
        self.adb.shell_command('chmod 755 {}/minicap'.format(self.dir))

        minicap_so_path = Path.joinpath(MINICAP_SHARED_PATH, 'android-{}/{}/minicap.so'.format(rel_version, abi))
        if minicap_so_path.exists() is False:
            minicap_so_path = Path.joinpath(MINICAP_SHARED_PATH, 'android-{}/{}/minicap.so'.format(sdk_version, abi))
        self.adb.push_local_file(str(minicap_so_path), '{}/minicap.so'.format(self.dir))
        self.adb.shell_command('chmod 755 {}/minicap.so'.format(self.dir))

    @logwrap(LOGGER)
    def uninstall(self):
        self.adb.shell_command('rm -rf {}/minicap*'.format(self.dir))

    @on_method_ready('install')
    @logwrap(LOGGER)
    def get_display_info(self):
        raw_display_info = self.adb.shell_command('LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -i')
        display_info = json.loads(''.join(raw_display_info))

        return display_info

    @on_method_ready('install')
    @logwrap(LOGGER)
    def get_frame(self):
        display_info = self.get_display_info()
        width = display_info['width']
        height = display_info['height']
        rotation = display_info['rotation']

        frame = self.adb.shell_command('LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P {}x{}@{}x{}/{} -s'
                                       .format(width, height, width, height, rotation))
        # jpg_data = frame.split(b"for JPG encoder" + b"\r\n")[-1]
        jpg_data = frame.replace(b"\r\n", b"\n")
        return jpg_data


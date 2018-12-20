# -*- coding: utf-8 -*-
import re
import six

from logger import get_logger
from minitest.core.android.ime.ime import YosemiteIme
from minitest.core.utils.non_blocking_stream_reader import NonBlockingStreamReader

YOSEMITE_PACKAGE = 'com.netease.nie.yosemite'

LOGGING = get_logger(__name__)


class Recorder(YosemiteIme):
    """Screen recorder"""

    def __init__(self, adb):
        super(Recorder, self).__init__(adb)
        self.recording_proc = None
        self.recording_file = None

    # @on_method_ready('install_or_upgrade')
    def start_recording(self, max_time=2, bit_rate=None, vertical=None):
        """
        Start screen recording

        Args:
            max_time: maximum rate value, default is 1800
            bit_rate: bit rate value, default is None
            vertical: vertical parameters, default is None

        Raises:
            RuntimeError: if any error occurs while setup the recording

        Returns:
            None if recording did not start, otherwise True

        """
        if getattr(self, "recording_proc", None):
            LOGGING.error("recording_proc has already started")

        pkg_path = self.adb.app_path(YOSEMITE_PACKAGE)
        max_time_param = "-Dduration=%d" % max_time if max_time else ""
        bit_rate_param = "-Dbitrate=%d" % bit_rate if bit_rate else ""
        if vertical is None:
            vertical_param = ""
        else:
            vertical_param = "-Dvertical=true" if vertical else "-Dvertical=false"
        # p = self.adb.shell_command('CLASSPATH=%s exec app_process %s %s %s /system/bin %s.Recorder --start-record' %
        #                            (pkg_path, max_time_param, bit_rate_param, vertical_param, YOSEMITE_PACKAGE))
        p = self.adb.shell_command('screenrecord /sdcard/filename.mp4')
        nbsp = NonBlockingStreamReader(p.stdout)
        while True:
            line = nbsp.readline(timeout=5)
            if line is None:
                raise RuntimeError("start recording error")
            if six.PY3:
                line = line.decode("utf-8")
            m = re.match("start result: Record start success! File path:(.*\.mp4)", line.strip())
            if m:
                output = m.group(1)
                self.recording_proc = p
                self.recording_file = output
                return True

    # @on_method_ready('install_or_upgrade')
    def stop_recording(self, output="screen.mp4", is_interrupted=False):
        """
        Stop screen recording

        Args:
            output: default file is `screen.mp4`
            is_interrupted: True or False. Stop only, no pulling recorded file from device.

        Raises:
            AirtestError: if recording was not started before

        Returns:
            None

        """
        pkg_path = self.adb.app_path(YOSEMITE_PACKAGE)
        p = self.adb.shell_command(
            'CLASSPATH=%s exec app_process /system/bin %s.Recorder --stop-record' % (pkg_path, YOSEMITE_PACKAGE))
        p.wait()
        self.recording_proc = None
        if is_interrupted:
            return
        for line in p.stdout.readlines():
            if line is None:
                break
            if six.PY3:
                line = line.decode("utf-8")
            m = re.match("stop result: Stop ok! File path:(.*\.mp4)", line.strip())
            if m:
                self.recording_file = m.group(1)
                self.adb.pull(self.recording_file, output)
                return True
        LOGGING.error("start_recording first")

    # @on_method_ready('install_or_upgrade')
    def pull_last_recording_file(self, output='screen.mp4'):
        """
        Pull the latest recording file from device. Error raises if no recording files on device.

        Args:
            output: default file is `screen.mp4`

        """
        recording_file = 'mnt/sdcard/test.mp4'
        self.adb.pull(recording_file, output)

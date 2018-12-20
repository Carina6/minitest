#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/12/12 17:47
# @Author: hlliu
import time
import re
import os
from copy import copy

from minitest.core.android.adb.pyadb import ADB
from minitest.core.android.ime.ime import YosemiteIme
from minitest.core.android.minicap.minicap import Minicap
from minitest.core.android.minitouch.minitouch import Minitouch
from minitest.core.android.recorder.recorder import Recorder
from minitest.core.cv2.img_utils import ImgUtils
from minitest.core.device import Device


class Android(Device):
    def __init__(self, host=None, port=None, serial=None):
        super(Android, self).__init__()

        self.adb = ADB(host=host, port=port, serial=serial)
        self.adb.wait_for_device_ext()

        self.minicap = Minicap(self.adb)
        self.minitouch = Minitouch(self.adb)
        self.ime = YosemiteIme(self.adb)
        self.recorder = Recorder(self.adb)

        self._display_info = {}
        # self._current_orientation = None

    def app_list(self, third_only=False):
        """
        Return list of packages

        Args:
            third_only: if True, only third party applications are listed

        Returns:
            array of applications

        """
        return self.adb.app_list(third_only)

    def app_path(self, package):
        """
        Print the full path to the package

        Args:
            package: package name

        Returns:
            the full path to the package

        """
        return self.adb.app_path(package)

    def check_app(self, package):
        """
        Check is package exists on the device

        Args:
            package: package name

        Returns:
            True or False whether the package exists on the device or not

        """
        return self.adb.check_app(package)

    def start_app(self, package, activity=None):
        """
        Start the application and activity

        Args:
            package: package name
            activity: activity name

        Returns:
            None

        """
        return self.adb.start_app(package, activity)

    def start_app_timing(self, package, activity):
        """
        Start the application and activity, and measure time

        Args:
            package: package name
            activity: activity name

        Returns:
            app launch time

        """
        outputs = str(self.adb.start_app_timing(package, activity))
        p = re.compile('Status:\s*ok')
        m = p.search(outputs)
        if m:
            p = re.compile('TotalTime:\s*(\d+)')
            return p.search(outputs).group(1)

    def stop_app(self, package):
        """
        Stop the application

        Args:
            package: package name

        Returns:
            None

        """
        return self.adb.stop_app(package)

    def clear_app(self, package):
        """
        Clear all application data

        Args:
            package: package name

        Returns:
            None

        """
        return self.adb.clear_app(package)

    def install_app(self, fwdlock=False, reinstall=False, sdcard=False, pkgapp=None):
        return self.adb.install(fwdlock=fwdlock, reinstall=reinstall, sdcard=sdcard, pkgapp=pkgapp)

    def uninstall_app(self, package, keepdata=False):
        """
        Uninstall the application from the device

        Args:
            package: package name

        Returns:
            output from the uninstallation process

        """
        return self.adb.uninstall(package, keepdata)

    def snapshot(self, file_path=None):
        """
        Take the screenshot of the display. The output is send to stdout by default.

        Args:
            file_path: name of the file where to store the screenshot, default is None which si stdout

        Returns:
            screenshot output

        """
        """default not write into file."""
        screen = self.minicap.get_frame()

        if file_path:
            file_name = str(time.time()*1000) + '.jpg'
            file_path = os.path.join(file_path, file_name)
            ImgUtils.imwrite(file_path, screen)

        # '''t_img 需转换为cv2可解码的文件，不然会抛错 src is not a numpy array, neither a scalar'''
        # try:
        #     screen = ImgUtils.str2img(screen)
        # except Exception:
        #     # may be black/locked screen or other reason print exc for debugging
        #     import traceback
        #     traceback.print_exc()
        #     return None

        return screen

    def shell(self, cmd):
        return self.adb.shell_command(cmd)

    def keyevent(self, keyname):
        """
        Perform keyevent on the device
        Args:
            keyname: keyeven name

        Returns:
            None

        """
        self.adb.key_events(keyname)

    def home(self):
        """
        Press HOME button

        Returns:
            None

        """
        self.keyevent("HOME")

    def text(self, text, enter=True):
        """
        Input text on the device

        Args:
            text: text to input
            enter: True or False whether to press `Enter` key

        Returns:
            None

        """
        self.ime.text(text)

        if enter:
            self.adb.shell_command("input keyevent ENTER")

    def touch(self, pos, interval=0.01):
        """
        Perform touch event on the device

        Args:
            pos: coordinates (x, y)
            interval: how long to touch the screen

        Returns:
            None

        """
        # 根据屏幕方向，确定真正的点击位置，分四个方向
        # pos = self._touch_point_by_orientation(pos)
        self.minitouch.touch(pos, interval=interval)

    def double_click(self, pos):
        self.touch(pos)
        time.sleep(0.05)
        self.touch(pos)

    def swipe(self, p1, p2, interval=0.5, steps=5):
        """
        Perform swipe event on the device

        Args:
            p1: start point
            p2: end point
            interval: how long to swipe the screen, default 0.5
            steps: how big is the swipe step, default 5

        Returns:
            None

        """
        self.minitouch.swipe(p1, p2, interval=0.1, steps=steps)

    def pinch(self, *args, **kwargs):
        """
        Perform pinch event on the device

        Args:
            *args: optional arguments
            **kwargs: optional arguments

        Returns:
            None

        """
        return self.minitouch.pinch(*args, **kwargs)

    def logcat(self, *args, **kwargs):
        """
        Perform `logcat`operations
        Args:
            *args: optional arguments
            **kwargs: optional arguments

        Returns:
            `logcat` output

        """
        return self.adb.get_logcat(*args, **kwargs)

    def getprop(self, key, strip=True):
        """
        Get properties for given key

        Args:
            key: key name
            strip: True or False whether to strip the output or not

        Returns:
            property value(s)

        """
        return self.adb.getprop(key, strip)

    def get_ip_address(self):
        """
        Perform several set of commands to obtain the IP address
            * `adb shell netcfg | grep wlan0`
            * `adb shell ifconfig`
            * `adb getprop dhcp.wlan0.ipaddress`

        Returns:
            None if no IP address has been found, otherwise return the IP address

        """
        return self.adb.get_ip_address()

    def get_top_activity(self):
        """
        Get the top activity

        Returns:
            package, activity and pid

        """
        bat = self.adb.get_top_activity_info()
        pattern = re.compile('\s*ACTIVITY ([A-Za-z0-9_.]+)/([A-Za-z0-9_.]+) \w+ pid=(\d+)')
        out = pattern.search(str(bat))

        if out:
            return [out.group(1), out.group(2), out.group(3)]

        return None

    def is_keyboard_shown(self):
        """
        Return True or False whether soft keyboard is shown or not

        Notes:
            Might not work on all devices

        Returns:
            True or False

        """
        out = self.adb.get_input_method_info()
        if 'mInputShown=ture' in str(out):
            return True
        else:
            return False

    def is_screen_on(self):
        """
        Return True or False whether the screen is on or not

        Notes:
            Might not work on all devices

        Returns:
            True or False

        """
        out = self.adb.get_window_policy_info()
        pattern = re.compile('mScreenOnFully=(true|false)')
        return pattern.search(str(out)).group(1)

    def is_locked(self):
        """
        Return True or False whether the device is locked or not

        Notes:
            Might not work on some devices

        Returns:
            True or False

        """
        out = self.adb.get_window_policy_info()

        pattern = re.compile('mShowingLockscreen=(true|false)')
        return pattern.search(str(out)).group(1)

    def unlock(self):
        self.minicap.wake_up()

    @property
    def display_info(self):
        """
        Return the display info (width, height, orientation and max_x, max_y)

        Returns:
            display information

        """
        if not self._display_info:
            self._display_info = self.minicap.get_display_info()
        display_info = copy(self._display_info)
        # update ow orientation, which is more accurate
        # if self._current_orientation is not None:
        #     display_info.update({
        #         "rotation": self._current_orientation * 90,
        #         "orientation": self._current_orientation,
        #     })
        return display_info

    def get_display_info(self):
        """
        Return the display info (width, height, orientation and max_x, max_y)

        Returns:
            display information

        """
        return self.display_info

    def get_current_resolution(self):
        """
        Return current resolution after rotation

        Returns:
            width and height of the display

        """
        return self.display_info["width"], self.display_info["height"]

    def start_recording(self, *args, **kwargs):
        """
        Start recording the device display

        Args:
            *args: optional arguments
            **kwargs:  optional arguments

        Returns:
            None

        """
        return self.recorder.start_recording(*args, **kwargs)

    def stop_recording(self, *args, **kwargs):
        """
        Stop recording the device display. Recoding file will be kept in the device.

        Args:
            *args: optional arguments
            **kwargs: optional arguments

        Returns:
            None

        """
        return self.recorder.stop_recording(*args, **kwargs)

    # def _touch_point_by_orientation(self, tuple_xy):
    #     """
    #     Convert image coordinates to physical display coordinates, the arbitrary point (origin) is upper left corner
    #     of the device physical display
    #
    #     Args:
    #         tuple_xy: image coordinates (x, y)
    #
    #     Returns:
    #
    #     """
    #     x, y = tuple_xy
    #     x, y = XYTransformer.up_2_ori(
    #         (x, y),
    #         (self.display_info["width"], self.display_info["height"]),
    #         self.display_info["orientation"]
    #     )
    #     return x, y

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/12/6 18:12
# @Author: hlliu

from logger import get_logger
from minitest.core.android.android import Android
from minitest.core.cv import loop_find, Template
from minitest.core.helper import G

LOGGER = get_logger(__name__)


def auto_setup():
    G.DEVICE = Android()


def touch(s_img):
    pos = loop_find(Template(s_img))

    # 点击 目标图片匹配到的区域的中间点 (使用minitouch)
    G.DEVICE.minitouch.touch(pos)


def assert_exit(s_img):
    try:
        pos = loop_find(s_img)
    except Exception as e:
        LOGGER.info(e)
        return False

    return True


def text(str):
    G.DEVICE.ime.text(str)


def swipe(from_xy, to_xy):
    G.DEVICE.swipe(from_xy, to_xy)


def install(filepath):
    G.DEVICE.install_app(pkgapp=filepath)


def uninstall(package):
    G.DEVICE.uninstall_app(package)


def start_app(package, activity=None):
    G.DEVICE.start_app(package, activity)


def start_app_timing(package, activity):
    return G.DEVICE.start_app_timing(package, activity)


def home():
    G.DEVICE.keyevent('HOME')


def key_events(event):
    G.DEVICE.keyevent(event)


def list_app():
    return G.DEVICE.app_list(third_only=True)


def path_app(package):
    return G.DEVICE.app_path(package)


def getprop(key):
    return G.DEVICE.getprop(key)


def get_ip_address():
    return G.DEVICE.get_ip_address()


def get_top_activity():
    return G.DEVICE.get_top_activity()


def is_screen_on():
    return G.DEVICE.is_screen_on()


def get_display_info():
    return G.DEVICE.get_display_info()



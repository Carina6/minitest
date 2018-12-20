#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/12/7 18:16
# @Author: hlliu
from minitest.core.android.adb.pyadb import ADB
from minitest.core.android.minitouch.minitouch import Minitouch

adb = ADB()
mini_touch = Minitouch(adb)
mini_touch.install_server()
mini_touch.start_server()
mini_touch.start_client()
# mini_touch.touch((771, 629))
# mini_touch.touch((771, 1500))
mini_touch.swipe((771, 1600), (771, 500))

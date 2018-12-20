#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/12/7 10:11
# @Author: hlliu
from minitest.config import MINITEST_ROOT
from minitest.core.android.adb.pyadb import ADB
from minitest.core.android.minicap.minicap import Minicap

adb = ADB()

cap = Minicap(adb)
cap.install()
cap.screenshot(MINITEST_ROOT)
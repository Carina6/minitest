#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/12/5 18:33
# @Author: hlliu
import sys

from minitest.core.android.adb.pyadb import ADB

# print(sys.platform)
from minitest.core.android.ime.ime import YosemiteIme

adb = ADB()

# apps = adb.shell_command("pm list packages")
ime = YosemiteIme(adb)
ime.text('1234qwer')
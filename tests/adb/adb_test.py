#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/12/5 18:33
# @Author: hlliu
import sys

from minitest.core.android.adb.pyadb import ADB

# print(sys.platform)
adb = ADB()
print(adb.pyadb_version())
print(adb.get_version())

apps = adb.shell_command("pm list packages")

for app in apps:
    path = adb.shell_command("pm path {}".format(app.split(':')[1]))
    print("{}:{}".format(app, path))

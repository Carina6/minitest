#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pyaxmlparser import APK


a = APK("/Users/Xiaobo/Workspace_ARD/minitest/core/resources/poco/pocoservice-debug.apk")
print(a.xml)
print(a.axml)
print(a.version_name)
print(a.get_target_sdk_version)
print(a.get_main_activity())
print(a.apk)
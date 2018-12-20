#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/12/18 17:15
# @Author: hlliu
from minitest.core.api import auto_setup, getprop, get_ip_address, get_top_activity, is_screen_on, get_display_info, \
    start_app_timing

auto_setup()
# home()

# start_app('com.netease.nie.yosemite')

# keyevent('back')

# l = list_app()

# p = path_app('com.netease.nie.yosemite')

# check = check_app('com.netease.nie.yosemite')
# print(check)

# stop_app('com.netease.nie.yosemite')

# snapshot(os.path.join(MINITEST_ROOT, 'screet.png'))

# o = getprop('ro.serialno')
o = start_app_timing('com.xiaomi.loan', 'com.xiaomi.jr.MiFinanceActivity')
print(o)
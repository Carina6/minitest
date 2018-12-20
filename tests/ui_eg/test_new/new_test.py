# -*- encoding=utf8 -*-
from minitest.config import MINITEST_ROOT
from minitest.core.api import auto_setup, touch
import os

__author__ = "hlliu"

# from airtest.core.api import *


auto_setup()
# dev.home()
# dev.start_app('com.netease.nie.yosemite')
# dev.keyevent('back')
# l = dev.list_app()
# p = dev.path_app('com.netease.nie.yosemite')
# check = dev.check_app('com.netease.nie.yosemite')
# dev.stop_app('com.netease.nie.yosemite')
# print(check)
# dev.snapshot(os.path.join(MINITEST_ROOT, 'screet.png'))
# record = Recorder(set_up.adb)
# record.start()
# record.start_recording()
# time.sleep(2)
# record.stop_recording()

# apk_file = os.path.join(MINITEST_ROOT, 'resources')
# apk_file = os.path.join(apk_file, 'android')
# apk_file = os.path.join(apk_file, 'ime')
# apk_file = os.path.join(apk_file, 'Yosemite.apk')
# set_up.install(apk_file)
# set_up.home()
# set_up.start_app('com.netease.nie.yosemite')


touch("tpl1544064088909.png")
# set_up.touch("tpl1544064116640.png")
# set_up.touch("tpl1544064195292.png")





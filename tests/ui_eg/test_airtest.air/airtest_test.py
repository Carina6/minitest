# -*- encoding=utf8 -*-
from airtest.core.android.recorder import Recorder

__author__ = "hlliu"

from airtest.core.api import *

auto_setup(__file__)
dev = connect_device('android:///')
o = dev.get_ip_address()
print(o)
# start_time = dev.start_app_timing('com.android.chrome', 'org.chromium.chrome.browser.ChromeTabbedActivity')
# print(start_time)
# dev = connect_device('android://adbhost:adbport/1234566?cap_method=javacap&touch_method=adb')
# dev.start_recording()
# time.sleep(3)
# dev.stop_recording()
# home()
# start_app('com.netease.nie.yosemite')


# touch(Template(r"tpl1544064088909.png", record_pos=(0.356, 0.354), resolution=(1080.0, 1920.0)))
# touch(Template(r"tpl1544064116640.png", record_pos=(-0.409, -0.75), resolution=(1080.0, 1920.0)))
# touch(Template(r"tpl1544064195292.png", record_pos=(-0.343, -0.542), resolution=(1080.0, 1920.0)))
# touch(Template(r"tpl1544064205331.png", record_pos=(0.007, 0.75), resolution=(1080.0, 1920.0)))
# touch(Template(r"tpl1544064211556.png", record_pos=(0.08, 0.298), resolution=(1080.0, 1920.0)))
# touch(Template(r"tpl1544064218444.png", record_pos=(-0.364, -0.08), resolution=(1080.0, 1920.0)))
# text('4166015')
# touch(Template(r"tpl1544064258936.png", record_pos=(-0.394, 0.06), resolution=(1080.0, 1920.0)))
# touch(Template(r"tpl1544064270787.png", record_pos=(-0.003, 0.274), resolution=(1080.0, 1920.0)))
#
# assert_exists(Template(r"tpl1541576556930.png", record_pos=(0.001, -0.037), resolution=(1080, 1920)), "进入未登录首页")
#
# keyevent("BACK")





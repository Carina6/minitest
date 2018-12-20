#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/12/7 16:25
# @Author: hlliu
import time
from pathlib import Path

from airtest.core.android.adb import ADB
from airtest.core.android.minicap import Minicap

from minitest.config import MINITEST_ROOT

adb = ADB(serialno='d3bacaf50604')

cap = Minicap(adb)

frame = cap.get_frame()

file_name = str(time.time()) + '.jpg'
file_path = Path.joinpath(MINITEST_ROOT, file_name)
with open(file_path, 'wb+') as f:
    f.write(frame)
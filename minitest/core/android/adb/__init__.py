#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

from minitest.config import MINITEST_ROOT

# ADB binary path
if sys.platform.startswith('win'):
    ADB_PATH = Path.joinpath(MINITEST_ROOT, 'resources/android/adb/win32/adb.exe')
else:
    ADB_PATH = Path.joinpath(MINITEST_ROOT, 'resources/android/adb/{}/adb'.format(sys.platform))

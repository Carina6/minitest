#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path

from minitest.config import MINITEST_ROOT

YOSEMITE_APK_PATH = str(Path.joinpath(MINITEST_ROOT, 'resources/android/ime/Yosemite.apk'))
YOSEMITE_IME_SERVICE_NAME = 'com.netease.nie.yosemite/.ime.ImeService'
YOSEMITE_IME_PACKAGE_NAME = 'com.netease.nie.yosemite'

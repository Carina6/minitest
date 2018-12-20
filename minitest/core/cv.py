#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/12/20 15:15
# @Author: hlliu
import os
import time

import cv2

from config import IMAGE_ROOT
from minitest.core.cv2.img_utils import ImgUtils
from minitest.core.error import TargetNotFoundError
from minitest.core.helper import G
from minitest.core.settings import FIND_TIMEOUT, LOG_DIR


def loop_find(t, time_out=FIND_TIMEOUT, interval=0.5):
    if not isinstance(t, Template):
        raise TypeError('t is not the Template type')

    start_time = time.time()
    while True:
        screen = G.DEVICE.snapshot()
        screen_gray = cv2.cvtColor(ImgUtils.str2img(screen), cv2.COLOR_BGR2GRAY)
        pos = t.match_in(screen_gray)
        if pos:
            log_screen(screen)
            return pos
        if time.time() - start_time > time_out:
            log_screen(screen)
            raise TargetNotFoundError('Picture {} not found in screen'.format(t))
        else:
            time.sleep(interval)


def log_screen(screen=None):
    if screen is None:
        screen = G.DEVICE.snapshot()

    file_name = str(time.time() * 1000) + '.jpg'
    file_path = os.path.join(LOG_DIR, file_name)
    ImgUtils.imwrite(file_path, screen)


class Template(object):
    def __init__(self, img_name):
        self.img_path = os.path.join(IMAGE_ROOT, img_name)
        self.img_cv2 = cv2.imread(self.img_path)
        self.img_cv2_gray = cv2.cvtColor(self.img_cv2, cv2.COLOR_BGR2GRAY)

    def match_in(self, target_gray):
        # 图片匹配 (使用cv2的图像匹配)
        res = cv2.matchTemplate(target_gray, self.img_cv2_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        h, w = self.img_cv2.shape[:2]

        focus_pos = None
        if max_val > 0.8:
            focus_pos = max_loc[0] + w / 2, max_loc[1] + h / 2

        return focus_pos




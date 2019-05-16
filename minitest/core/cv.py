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
        # 截图，rgb图像
        screen = G.DEVICE.snapshot()
        # 创建一个原始图像的灰度版
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
        # 灰度图像
        self.img_cv2_gray = cv2.cvtColor(self.img_cv2, cv2.COLOR_BGR2GRAY)

    def match_in(self, target_gray):
        # 图片匹配 (使用cv2的图像匹配)
        # 使用matchTemplate对原始灰度图像和图像模板进行匹配
        res = cv2.matchTemplate(target_gray, self.img_cv2_gray, cv2.TM_CCOEFF_NORMED)
        # res 矩阵中最小值，最大值，最小值坐标，最大值坐标
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # 模板图片的高和宽
        h, w = self.img_cv2.shape[:2]

        focus_pos = None
        # 设置阈值，如果匹配的最大值大于0.8，则表明匹配到了
        if max_val > 0.8:
            focus_pos = max_loc[0] + w / 2, max_loc[1] + h / 2

        return focus_pos




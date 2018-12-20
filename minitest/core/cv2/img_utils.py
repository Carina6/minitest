#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np


class ImgUtils:
    @staticmethod
    def img2str(img):
        _, png = cv2.imencode('.png', img)
        return png.tostring()

    @staticmethod
    def str2img(pngstr):
        np_arr = np.fromstring(pngstr, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return img

    @staticmethod
    def imwrite(filename, screen):
        with open(filename, 'wb+') as f:
            f.write(screen)

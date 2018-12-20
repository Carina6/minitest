#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/12/20 17:43
# @Author: hlliu


class BaseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TargetNotFoundError(BaseError):
    pass


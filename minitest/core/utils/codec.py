#!/usr/bin/env python
# -*- coding: utf-8 -*-
from six import text_type


def unicode(v):
    if type(v) is not text_type:
        try:
            v = v.decode('utf-8')
        except UnicodeDecodeError:
            v = v.decode('gbk')
    return v

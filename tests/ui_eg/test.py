#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/12/12 18:27
# @Author: hlliu
from urllib.parse import urlparse, parse_qsl


def test():
    d = urlparse('android://adbhost:adbport/1234566?cap_method=javacap&touch_method=adb')
    platform = d.scheme
    host = d.netloc
    uuid = d.path.lstrip("/")
    params = dict(parse_qsl(d.query))
    if host:
        params["host"] = host.split(":")

    print(uuid)
    print(params)
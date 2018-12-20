#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/12/12 17:05
# @Author: hlliu
from six import with_metaclass


class MetaDevice(type):
    REGISTRY = {}

    def __new__(meta, class_name, class_parent, class_attr):
        cls = type.__new__(meta, class_name, class_parent, class_attr)
        meta.REGISTRY[class_name] = cls

        return cls


class Device(with_metaclass(MetaDevice, object)):

    def __init__(self):
        super(Device, self).__init__()

    def start_app(self, package, activity=None):
        self._raise_not_implemented_error()

    def stop_app(self, package):
        self._raise_not_implemented_error()

    def clear_app(self, package):
        self._raise_not_implemented_error()

    def list_app(self):
        self._raise_not_implemented_error()

    def install_app(self, **kwargs):
        self._raise_not_implemented_error()

    def uninstall_app(self, package, keepdata):
        self._raise_not_implemented_error()

    def shell(self, cmd):
        self._raise_not_implemented_error()

    def touch(self, xy, interval):
        self._raise_not_implemented_error()

    def double_click(self, target):
        self._raise_not_implemented_error()

    def snapshot(self, *args, **kwargs):
        self._raise_not_implemented_error()

    def swipe(self, t1, t2, **kwargs):
        self._raise_not_implemented_error()

    def keyevent(self, key):
        self._raise_not_implemented_error()

    def text(self, text, enter=True):
        self._raise_not_implemented_error()

    def _raise_not_implemented_error(self):
        platform = self.__class__.__name__
        raise NotImplementedError("Method not implemented on %s" % platform)

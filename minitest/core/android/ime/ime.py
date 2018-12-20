#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from pyaxmlparser import APK

from minitest.core.android.ime import *
from minitest.core.android.ime.exceptions import ImeException
from minitest.core.helper import on_method_ready
from minitest.core.utils.codec import unicode


class Ime(object):
    def __init__(self, adb, apk_path, service_name):
        self.adb = adb
        self.apk_path = apk_path
        self.service_name = service_name

        def get_default_ime(adb):
            outputs = adb.shell_command("settings get secure default_input_method")

            ime = outputs[0] if len(outputs) == 1 else None
            return ime

        def get_package_name(service_name):
            return service_name.split('/')[0]

        self.default_ime = get_default_ime(self.adb)
        self.package_name = get_package_name(self.service_name)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def get_ime_list(self):
        outputs = self.adb.shell_command("ime list -a")

        ime_list = []
        for output in outputs:
            m = re.findall("mId=(.*?/.*?) ", output)
            ime_list += m
        return ime_list

    def start(self):
        if self.service_name not in self.get_ime_list():
            raise ImeException('IME service ({}) can not be found.'.format(self.service_name))
        if self.default_ime != self.service_name:
            self.adb.shell_command("ime enable {}".format(self.service_name))
            self.adb.shell_command("ime set {}".format(self.service_name))

    def stop(self):
        if self.default_ime and self.default_ime != self.service_name:
            self.adb.shell_command("ime disable {}".format(self.service_name))
            self.adb.shell_command("ime set {}".format(self.default_ime))

    def is_default(self):
        if self.default_ime and self.default_ime != self.service_name:
            return False
        return True

    def install(self):
        self.adb.install(reinstall=True, pkgapp=self.apk_path)

    def uninstall(self):
        self.adb.uninstall(self.package_name)

    def text(self, value):
        raise NotImplementedError


class YosemiteIme(Ime):
    def __init__(self, adb):
        super(YosemiteIme, self).__init__(adb, YOSEMITE_APK_PATH, YOSEMITE_IME_SERVICE_NAME)

    def start(self):
        def install_or_upgrade(adb, apk_path, service_name):
            installed_version_code = adb.get_package_version(service_name)
            apk_version_code = APK(apk_path).version_code

            if installed_version_code is None or int(apk_version_code) > int(installed_version_code):
                self.install()

        install_or_upgrade(self.adb, self.apk_path, self.service_name)
        super(YosemiteIme, self).start()

    def stop(self):
        super(YosemiteIme, self).stop()

    @on_method_ready('start')
    def text(self, value):
        if not self.is_default():
            self.start()
        value = unicode(value)
        self.adb.shell_command(u"am broadcast -a ADB_INPUT_TEXT --es msg '{}'".format(value))

# 更多的输入用法请见 https://github.com/macacajs/android-unicode#use-in-adb-shell_command

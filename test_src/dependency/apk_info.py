# -*- coding: utf-8 -*-

import os

import constants

class ApkInfo(object):
    def __init__(self, filename):
        self.filename   = filename
        self.aapt       = constants.AAPT

        self.apkinfo        = None
        self._package_name   = None
        self._class_name     = None

    def read_apk_info(self):
        cmd = '%s d badging %s' % (self.aapt, self.filename)
        self.apkinfo = os.popen(cmd).read()

    def get_package_name(self):
        if not self.apkinfo:
            self.read_apk_info()

        start = self.apkinfo.find("package")
        end = self.apkinfo.find("versionCode",start)
        package_name = self.apkinfo[start:end-1]
        self._package_name = package_name[package_name.find("'")+1:package_name.rfind("'")]

    def get_class_name(self):
        if not self.apkinfo:
            self.read_apk_info()

        start = self.apkinfo.find("launchable-activity")
        end = self.apkinfo.find("label",start)
        class_name = self.apkinfo[start:end-1]
        self._class_name = class_name[class_name.find("'")+1:class_name.rfind("'")]

    @property
    def apk_name(self):
        return os.path.basename(self.filename)

    @property
    def package_name(self):
        if self._package_name:
            return self._package_name
        else:
            self.get_package_name()
            return self._package_name


    @property
    def class_name(self):
        if self._class_name:
            return self._class_name
        else:
            self.get_class_name()
            return self._class_name

    @property
    def install_command(self):
        return 'install %s' % (self.filename)

    @property
    def start_command(self):
        if self._package_name and self._class_name:
            return 'shell am start -n %s/%s' % (self._package_name, self._class_name)
        else:
            if not self._package_name:
                self.get_package_name()

            if not self._class_name:
                self.get_class_name()

            return 'shell am start -n %s/%s' % (self._package_name, self._class_name)

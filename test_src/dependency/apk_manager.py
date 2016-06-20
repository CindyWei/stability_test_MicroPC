# -*- coding: utf-8 -*-

import os
import subprocess
import platform
import constants
import singleton
from non_block_stream_reader import NonBlockStreamReader
from apk_info import ApkInfo
from automation_device import AutomationDevice

class ApkManager(singleton.Singleton):
    def init(self):
        self.adb        = constants.ADB
        self.apk_path   = os.path.join(os.path.dirname(os.path.abspath(__file__)), constants.APKS_DIR)
        self.d          = AutomationDevice().get_device()


        self._local_apks       = []
        self._local_apks_info  = {}

        self.get_local_apks()
        self.get_local_apks_info()

    def get_local_apks(self):
        self._local_apks = []
        apks = []
        if os.path.exists(self.apk_path) and os.path.isdir(self.apk_path):
            apks = os.listdir(self.apk_path)
            if apks:
                for apk in apks:
                    name, ext = os.path.splitext(apk)
                    if ext == '.apk':
                        self._local_apks.append(os.path.join(self.apk_path, apk))

    def get_local_apks_info(self):
        self._local_apks_info = {}
        if self._local_apks:
            for apk in self._local_apks:
                apk_info = ApkInfo(apk)
                self._local_apks_info[apk_info.apk_name] = apk_info

    def check_install(self, apk, **kwargs):
        READLINE_TIMEOUT = 0.5
        apk_package_name = self._local_apks_info[apk].package_name
        apk_installed = False

        # check apk install status
        if kwargs and 'serial_number' in kwargs:
            adb_special = '%s -s %s' % (self.adb, kwargs['serial_number'])
        else:
            adb_special = '%s' % (self.adb)

        cmd = '%s shell pm list package' % (adb_special)
        if platform.system() == 'Linux':
            cmd = 'sudo %s shell pm list package' % (adb_special)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        nb_reader = NonBlockStreamReader(p.stdout)
        line_detect = False
        while True:
            line = nb_reader.readline(READLINE_TIMEOUT)
            if not line:
                if line_detect:
                    break
                else:
                    continue
            if apk_package_name in line:
                apk_installed = True
                break
            else:
                line_detect = True
        p.wait()

        if not apk_installed:
            install_command = '%s %s' % (adb_special, self._local_apks_info[apk].install_command)
            if platform.system() == 'Linux':
                install_command = 'sudo %s %s' % (adb_special, self._local_apks_info[apk].install_command)
            p_install = subprocess.Popen(install_command)
            p_install.wait()

    def start_apk(self, apk, **kwargs):
        self.check_install(apk, **kwargs)

        if kwargs and 'serial_number' in kwargs:
            adb_special = '%s -s %s' % (self.adb, kwargs['serial_number'])
        else:
            adb_special = '%s' % (self.adb)

        start_command = '%s %s' % (adb_special, self._local_apks_info[apk].start_command)
        if platform.system() == 'Linux':
            start_command = 'sudo %s %s' % (adb_special, self._local_apks_info[apk].start_command)
        if kwargs:
            additional = ''
            for item in kwargs:
                if item in ['a', 'd']:
                    additional = '%s -%s %s' % (additional, item, kwargs[item])
            start_command  = '%s%s' % (start_command, additional)
	    print start_command
        subprocess.Popen(start_command,shell=True, stdout=subprocess.PIPE)

    def close_apk(self, apk):
        close_btn = self.d(packageName=self._local_apks_info[apk].package_name, resourceId='android:id/pc_close')
        if close_btn.exists:
            close_btn.click()

    def get_apk_info(self, apk):
        if apk and apk in self._local_apks_info:
            return self._local_apks_info[apk]
        else:
            return None

    @property
    def local_apks(self):
        return self._local_apks

    @property
    def local_apks_info(self):
        return self._local_apks_info

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import subprocess

import constants
from adb_tools import AdbTools
from non_block_stream_reader import NonBlockStreamReader
from account import Account
from apk_manager import ApkManager
from automation_device import AutomationDevice

'''
prepare MPC box before doing the mpt_* test;
note1: if remount failed, please run command: echo "enable 0;" > /proc/alog;
'''

class PrepareMPT():
    def __init__(self):
        self.adb_tools          = AdbTools()
        self.d                  = AutomationDevice().get_device()
        self.account            = Account(self.d)

        self.fps                = None
        self.fps_full_file_name = '/system/build.prop'
        self.fps_file_name      = 'build.prop'
        self.fps_file_name_mod  = 'build_mod.prop'

        self.blacklist          = '/system/media/applist/blacklist.txt'
        self.gesturehelper      = '/system/bin/gesturehelper'

    def check_fps(self):
        self.fps = None

        # check debug.sf.fps
        self.adb_tools.adb_pull(self.fps_full_file_name, self.fps_file_name)
        f_read  = open(self.fps_file_name)
        for line in f_read:
            if not line:
                break
            if 'debug.sf.fps' in line:
                print line.rstrip()
                fps = line.rstrip().split('=')[1]
                if fps:
                    self.fps = int(fps)

    def modify_fps(self):
        self.check_fps()

        if not self.fps:
            self.adb_tools.adb_remount()
            self.adb_tools.adb_pull(self.fps_full_file_name, self.fps_file_name)
            try:
                f_read  = open(self.fps_file_name)
                f_write = open(self.fps_file_name_mod, 'w')
                for line in f_read:
                    if not line:
                        break
                    if 'debug.sf.fps' in line:
                        line = line.replace('debug.sf.fps=0', 'debug.sf.fps=1')
                    f_write.write(line)
                f_read.close()
                f_write.close()
            except Exception as e:
                print(e)
            self.adb_tools.adb_push(self.fps_file_name_mod, self.fps_full_file_name)

            self.check_fps()

            if self.fps:
                print('change OK! fps = %s' % (self.fps))
                self.adb_tools.adb_chmod('644', self.fps_full_file_name)
            else:
                print('change KO! fps = %s' % (self.fps))
        else:
            print('fps = %s' % (self.fps))

    def close_screen_protect(self):
        self.adb_tools.adb_remount()
        self.adb_tools.adb_rm(self.blacklist)
        self.adb_tools.adb_setprop('sys.settings.show', '1')

        # login system
        self.account.sleep()
        self.account.wakeup()
        self.account.login()
        time.sleep(2)

        # unlock the screen
        apk_manager = ApkManager()
        apk = 'Development.apk'
        apk_info = apk_manager.get_apk_info(apk)
        apk_manager.start_apk(apk)
        time.sleep(1)

        dev_option = self.d(packageName=apk_info.package_name, text=u'开发者选项')
        if dev_option.exists:
            dev_option.click()
            time.sleep(1)

            settings_apk = 'Settings.apk'
            settings_apk_info = apk_manager.get_apk_info(settings_apk)
            not_lock_screen = self.d(packageName=settings_apk_info.package_name, text=u'不锁定屏幕')
            if not_lock_screen.exists:
                not_lock_screen.click()
            else:
                print('not found not_lock_screen')
            time.sleep(1)

            apk_manager.close_apk(settings_apk)
            time.sleep(1)
        else:
            print('not found dev_option')

        apk_manager.close_apk(apk)
    
    def prepare_mpt(self):
        self.adb_tools.adb_devices()
        if self.adb_tools.devices:
#             self.adb_tools.adb_shell("\"echo 'enable 0;' > /proc/alog\"")
#             self.adb_tools.adb_remount()
            #self.modify_fps()
            #self.close_screen_protect()
            gesturehelperBinPath = os.path.join(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'gesturehelper'), 'gesturehelper')
            self.adb_tools.adb_push(gesturehelperBinPath, '/system/bin')
            self.adb_tools.adb_chmod(777, self.gesturehelper)
            self.account.sleep()
            self.account.wakeup()
            self.account.login()
            time.sleep(5)
            
            #if self.fps:
            self.adb_tools.adb_reboot()
            #else:
                #print('prepare mpt fps failed, please check it')
        else:
            print('not found devices, please check it')

if __name__ == '__main__':
    automation_device = AutomationDevice()

    prepare = PrepareMPT()
    prepare.prepare_mpt()

    if automation_device:
        automation_device.stop_device()

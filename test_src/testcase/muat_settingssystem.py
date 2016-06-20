#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import logging
import unittest
import shutil
import sys
from dependency import screen_shot
from dependency.parametrized_test_case import ParametrizedTestCase
from dependency.automation_device import AutomationDevice
from dependency.account import Account
from dependency import constants
from dependency.apk_manager import ApkManager
from muat_report import MuatReport, GenerateResult
from dependency.adb_log import AdbLog
from Tkconstants import TOP
from dependency.adb_mouse import AdbMouse
from dependency.adb_tools import AdbTools

# Init logger
logger_name = '%s-%s' % (constants.LOGGER_CLIENT_MUAT, os.getpid())
logger = logging.getLogger(logger_name)

class SettingsSystemTest(ParametrizedTestCase):
    def setUp(self):
        # check monitor running status
        if self.mon and not self.mon.running_status:
            self.skipTest('process monitor stop')

        self.d      = AutomationDevice().get_device()
        self.account = Account(self.d)
        self.mouse = AdbMouse()
        self.adb_tools = AdbTools()

#         self.account.sleep()
#         self.account.wakeup()
#         self.account.login()
        Button1=self.d(resourceId='com.yunpc.yunosloginui:id/avatar')
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if not Button1.exists:
                break
            else:
                time.sleep(1)
        
        settingcloseButton = self.d(resourceId="android:id/pc_close", packageName="com.yunpc.mpc.settings")
        if settingcloseButton.exists:
            settingcloseButton.click() 

    def tearDown(self):
#         self.account.sleep()
        
        settingcloseButton = self.d(resourceId="android:id/pc_close", packageName="com.yunpc.mpc.settings")
        if settingcloseButton.exists:
            settingcloseButton.click()
            time.sleep(1)
            if settingcloseButton.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertFalse(settingcloseButton.exists)
            logger.info('close setting window:0')

#     def test_WiFi(self):
#         logger.info('Enter -- MUAT:SettingsSystemTest:test_WiFi')
#         self.adb_tools.adb_shell('am start -n com.yunpc.mpc.settings/com.yunpc.mpc.settings.MpcSettingsMain')
#         time.sleep(3)
#         netButton = self.d(resourceId='com.yunpc.mpc.settings:id/exToggleButton1')
#         if netButton.exists:
#             netButton.click()
#             time.sleep(3)
#             wifiButton = self.d(resourceId="com.yunpc.mpc.settings:id/exToggleButton1_wifi")
#             if wifiButton.exists:
#                 wifiButton.click()
#                 time.sleep(5)
#                 wifiStatus = self.d(resourceId="com.yunpc.mpc.settings:id/myTextView")
#                 time.sleep(5)
#                 self.assertTrue(wifiStatus.exists)
#                 if wifiStatus.info['text'] == u'以太网连接期间WLAN暂不可用':
#                      self.assertEqual(wifiStatus.info['text'], u'以太网连接期间WLAN暂不可用')
#                 else:                             
#                     wifiCheckbox = self.d(resourceId="com.yunpc.mpc.settings:id/mySwitch")
#                     if wifiCheckbox.exists:
#                         #wifiCheckbox.click()
#                         #time.sleep(15)
#                         #wifiStatus = self.d(text=u"网络状态: 已打开", resourceId="com.yunpc.mpc.settings:id/myTextView")
#                         time.sleep(5)
#                         #self.assertTrue(wifiStatus.exists)
#                           
#                         #wifiCheckbox.click()
#                         #time.sleep(15)
#                         #wifiStatus = self.d(text=u"网络状态: 已关闭", resourceId="com.yunpc.mpc.settings:id/myTextView")
#                         #time.sleep(5)
#                         #self.assertTrue(wifiStatus.exists)
#                       
#         settingcloseButton = self.d(resourceId="android:id/pc_close", packageName="com.yunpc.mpc.settings")
#         if settingcloseButton.exists:
#             settingcloseButton.click()
#             time.sleep(5)           
#         logger.info('Exit -- MUAT:SettingsSystemTest:test_WiFi')
          
#     def test_TimeAndDate(self):
#         logger.info('Enter -- MUAT:SettingsSystemTest:test_TimeAndDate')
#         self.adb_tools.adb_shell('am start -n com.yunpc.mpc.settings/com.yunpc.mpc.settings.MpcSettingsMain')
#         start=time.time()
#         dateandtimeTab = self.d(resourceId='com.yunpc.mpc.settings:id/exToggleButton5')
#         while time.time()-start<constants.Time_Out:
#             if dateandtimeTab.exists:
#                 break
#             else:
#                 time.sleep(1)
#         
#         if dateandtimeTab.exists:
#             dateandtimeTab.click()
#             dateButton = self.d(resourceId="com.yunpc.mpc.settings:id/exToggleButton0_dt")
#             start=time.time()
#             while time.time()-start<constants.Time_Out:
#                 if dateandtimeTab.exists:
#                     break
#                 else:
#                     time.sleep(1)
#             
#             if dateButton.exists:
#                 dateButton.click()
#                 autotimeStatus = self.d(text=u"自动设定日期和时间", resourceId="com.yunpc.mpc.settings:id/id_toggle_auto_time")
#                 start=time.time()
#                 while time.time()-start<constants.Time_Out:
#                     if dateandtimeTab.exists:
#                         break
#                     else:
#                         time.sleep(1)
#                 
#                 if autotimeStatus.exists:
#                     timeEditbox = self.d(resourceId="com.yunpc.mpc.settings:id/id_edittext_seconds")
#                     if timeEditbox.exists:
#                         if not autotimeStatus.info['checked']:
#                             if not timeEditbox.info['enabled']:
#                                 name = sys._getframe().f_code.co_name
#                                 screen_shot.ScreenShot(self,name)
#                             self.assertTrue(timeEditbox.info['enabled'])
#                             autotimeStatus.click()
#                             
#                             start=time.time()
#                             while time.time()-start<constants.Time_Out:
#                                 if autotimeStatus.info['checked']:
#                                     break
#                                 else:
#                                     time.sleep(1)
#                             if self.d(resourceId="com.yunpc.mpc.settings:id/id_edittext_seconds").info['enabled']:
#                                 name = sys._getframe().f_code.co_name
#                                 screen_shot.ScreenShot(self,name)
#                             self.assertFalse(self.d(resourceId="com.yunpc.mpc.settings:id/id_edittext_seconds").info['enabled'])
#                         else:
#                             if timeEditbox.info['enabled']:
#                                 name = sys._getframe().f_code.co_name
#                                 screen_shot.ScreenShot(self,name)
#                             self.assertFalse(timeEditbox.info['enabled'])
#                             autotimeStatus.click()
#                             start=time.time()
#                             while time.time()-start<constants.Time_Out:
#                                 if not autotimeStatus.info['checked']:
#                                     break
#                                 else:
#                                     time.sleep(1)
#                             if not self.d(resourceId="com.yunpc.mpc.settings:id/id_edittext_seconds").info['enabled']:
#                                 name = sys._getframe().f_code.co_name
#                                 screen_shot.ScreenShot(self,name)
#                             self.assertTrue(self.d(resourceId="com.yunpc.mpc.settings:id/id_edittext_seconds").info['enabled'])
#                              
#                                      
#         settingcloseButton = self.d(resourceId="android:id/pc_close", packageName="com.yunpc.mpc.settings")
#         if settingcloseButton.exists:
#             settingcloseButton.click()
#             #time.sleep(5)           
#         logger.info('Exit -- MUAT:SettingsSystemTest:test_TimeAndDate')
          
    def test_Display(self):
        logger.info('Enter -- MUAT:SettingsSystemTest:test_Display')
        self.adb_tools.adb_shell('am start -n com.yunpc.mpc.settings/com.yunpc.mpc.settings.MpcSettingsMain')
        settingcloseButton = self.d(resourceId="android:id/pc_close", packageName="com.yunpc.mpc.settings")
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if settingcloseButton.exists:
                break
            else:
                time.sleep(1)
        displaytab = self.d(resourceId='com.yunpc.mpc.settings:id/exToggleButton4')
#         logger.debug(displaytab.info)
        if displaytab.exists:
            displaytab.click()
            resolutionSpinner = self.d(resourceId="com.yunpc.mpc.settings:id/id_disp_hdmi_spinner")
            start=time.time()
            while time.time()-start<constants.Time_Out:
                if resolutionSpinner.exists:
                    break
                else:
                    time.sleep(1)
#             if resolutionSpinner.exists:
#                 resolutionSpinner.click()
#                 time.sleep(3)
#                 label_1600_900 = self.d(text="1600x900")
#                 if label_1600_900.exists:
#                     label_1600_900.click()
#                     time.sleep(5)
#                     self.assertEqual(self.d.info['displaySizeDpX'], 1600)
#                     self.assertEqual(self.d.info['displaySizeDpY'], 900)
#                         
#                 resolutionSpinner.click()
#                 time.sleep(3)
#                 label_1280_1024 = self.d(text="1280x1024")
#                 if label_1280_1024.exists:
#                     label_1280_1024.click()
#                     time.sleep(5)
#                     self.assertEqual(self.d.info['displaySizeDpX'], 1280)
#                     self.assertEqual(self.d.info['displaySizeDpY'], 1024)
#                         
#                 resolutionSpinner.click()
#                 time.sleep(3)
#                 label_1024_768 = self.d(text="1024x768")
#                 if label_1024_768.exists:
#                     label_1024_768.click()
#                     time.sleep(5)
#                     self.assertEqual(self.d.info['displaySizeDpX'], 1024)
#                     self.assertEqual(self.d.info['displaySizeDpY'], 768)
#                         
#                 resolutionSpinner.click()
#                 time.sleep(3)
#                 label_1920_1080 = self.d(text="1920x1080")
#                 if label_1920_1080.exists:
#                     label_1920_1080.click()
#                     time.sleep(5)
            self.assertEqual(self.d.info['displaySizeDpX'], 1920)
            self.assertEqual(self.d.info['displaySizeDpY'], 1080)
                        
        settingcloseButton = self.d(resourceId="android:id/pc_close", packageName="com.yunpc.mpc.settings")
        if settingcloseButton.exists:
            settingcloseButton.click()
            #time.sleep(5)           
        logger.info('Exit -- MUAT:SettingsSystemTest:test_Display')
      
    def test_SystemInfo(self):
        logger.info('Enter -- MUAT:SettingsSystemTest:test_SystemInfo')
        self.adb_tools.adb_shell('am start -n com.yunpc.mpc.settings/com.yunpc.mpc.settings.MpcSettingsMain')
        settingcloseButton = self.d(resourceId="android:id/pc_close", packageName="com.yunpc.mpc.settings")
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if settingcloseButton.exists:
                break
            else:
                time.sleep(1)
        systeminfoTab = self.d(resourceId='com.yunpc.mpc.settings:id/exToggleButton0')
        if systeminfoTab.exists:
            systeminfoTab.click()
            moreButton = self.d(text=u"更多", packageName="com.yunpc.mpc.settings")
            if moreButton.exists:
                moreButton.click()
                lanTextview = self.d(text=u"有线MAC", packageName="com.yunpc.mpc.settings").right(className="android.widget.TextView")
                if lanTextview.exists:
                    lanmac = lanTextview.info['text']
                    self.adb_tools.adb_devices()
                    if self.adb_tools.devices:
                        tmppath = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'tmpdir')
                        os.mkdir(tmppath)
                        self.adb_tools.adb_pull("/sys/class/net/eth0/address", os.path.join(tmppath, 'address'))
                        f = open(os.path.join(tmppath, 'address'))
                        tmpmac = f.read().strip('\n')
                        f.close()
                        print tmpmac
                        self.assertEqual(lanmac, tmpmac.encode('utf-8'))
                        shutil.rmtree(tmppath)
                          
                wlanTextview = self.d(text=u"无线MAC", packageName="com.yunpc.mpc.settings").right(className="android.widget.TextView")
                if wlanTextview.exists:
                    wlanmac = wlanTextview.info['text']
                    self.adb_tools.adb_devices()
                    if self.adb_tools.devices:
                        tmppath = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'tmpdir')
                        os.mkdir(tmppath)
                        self.adb_tools.adb_pull("/sys/class/net/wlan0/address", os.path.join(tmppath, 'address'))
                        f = open(os.path.join(tmppath, 'address'))
                        tmpmac = f.read().strip('\n')
                        f.close()
                        print tmpmac
                        self.assertEqual(wlanmac, tmpmac.encode('utf-8'))
                        shutil.rmtree(tmppath)
                            
        settingcloseButton = self.d(resourceId="android:id/pc_close", packageName="com.yunpc.mpc.settings")
        if settingcloseButton.exists:
            settingcloseButton.click()
            #time.sleep(5)
        logger.info('Exit -- MUAT:SettingsSystemTest:test_SystemInfo')
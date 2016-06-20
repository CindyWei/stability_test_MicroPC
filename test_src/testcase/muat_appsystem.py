#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import logging
import unittest
import sys
from dependency import screen_shot
from dependency.parametrized_test_case import ParametrizedTestCase
from dependency.automation_device import AutomationDevice
from dependency.account import Account
from dependency import constants
from dependency.apk_manager import ApkManager
from muat_report import MuatReport, GenerateResult
from dependency.adb_log import AdbLog
from dependency.adb_mouse import AdbMouse
from dependency.adb_tools import AdbTools


# Init logger
logger_name = '%s-%s' % (constants.LOGGER_CLIENT_MUAT, os.getpid())
logger = logging.getLogger(logger_name)

class AppSystemTest(ParametrizedTestCase):
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
        start1=time.time()
        while time.time()-start1<constants.Time_Out:
            if not Button1.exists:
                break
            else:
                time.sleep(1)
        AppStoreIcon = self.d(text=u"应用商店", className="android.widget.TextView")
        if not AppStoreIcon.exists:
            #注销登陆
#             self.d.click(57,10)
#             time.sleep(1)
#             self.d.click(68,141)
#             start2=time.time()
#             while time.time()-start2<constants.Time_Out:
#                 if  Button1.exists:
#                     break
#                 else:
#                     time.sleep(1)
#             self.account.login()
#             start3=time.time()
#             while time.time()-start3<constants.Time_Out:
#                 if not Button1.exists:
#                     break
#                 else:
#                     time.sleep(1)
            self.d.click(950,562)
            time.sleep(1)
            Button1=self.d(resourceId='android:id/button1',className='android.widget.Button',packageName='android')
            if Button1.exists:
                Button1.click()
            time.sleep(1)
            if not AppStoreIcon.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(AppStoreIcon.exists)
        
        self.adb_tools.adb_shell('am force-stop com.alibaba.micropc.appstore')
        
        
    def tearDown(self):
        self.adb_tools.adb_shell('am force-stop com.alibaba.micropc.appstore')

    def test_EnterAppstore(self):
        logger.info('Enter -- MUAT:AppSystemTest:test_EnterAppstore')
        apk_manager = ApkManager()
        value = {}
        #report = MuatReport()
        if self.param and self.param.parameters and self.param.parameters.serial_number:
            serial_number = self.param.parameters.serial_number
        
        AppStoreIcon = self.d(text=u"应用商店", className="android.widget.TextView")
        click_x = AppStoreIcon.info['visibleBounds']['left'] +5
        click_y = AppStoreIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if  self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
                break
            else:
                time.sleep(1)
        if not self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists)
        if self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.alibaba.micropc.appstore")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
                #time.sleep(5)
        logger.info('Exit -- MUAT:AppSystemTest:test_EnterAppstore')
                
    def test_EnterAppstoreIndexTab(self):
        logger.info('Enter -- MUAT:AppSystemTest:test_EnterAppstoreIndexTab')
        apk_manager = ApkManager()
        value = {}
        #report = MuatReport()
        if self.param and self.param.parameters and self.param.parameters.serial_number:
            serial_number = self.param.parameters.serial_number
         
        AppStoreIcon = self.d(text=u"应用商店", className="android.widget.TextView")
        click_x = AppStoreIcon.info['visibleBounds']['left'] +5
        click_y = AppStoreIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
                break
            else:
                time.sleep(1)
        if not self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists)
        indexTab = self.d(text=u"推荐", resourceId="com.alibaba.micropc.appstore:id/indexTab")
        if not indexTab.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(indexTab.exists)
        if indexTab.exists:
            indexTab.click()
            #time.sleep(5)
        if self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.alibaba.micropc.appstore")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
                #time.sleep(5)
        logger.info('Exit -- MUAT:AppSystemTest:test_EnterAppstoreIndexTab')
                
    def test_EnterAppstoreTopicTab(self):
        logger.info('Enter -- MUAT:AppSystemTest:test_EnterAppstoreTopicTab')
        apk_manager = ApkManager()
        value = {}
        #report = MuatReport()
        if self.param and self.param.parameters and self.param.parameters.serial_number:
            serial_number = self.param.parameters.serial_number
        
        AppStoreIcon = self.d(text=u"应用商店", className="android.widget.TextView")
        click_x = AppStoreIcon.info['visibleBounds']['left'] +5
        click_y = AppStoreIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
                break
            else:
                time.sleep(1)
        if not self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists)
        topicTab = self.d(text=u"发现", resourceId="com.alibaba.micropc.appstore:id/topicTab")
        if not topicTab.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(topicTab.exists)
        if topicTab.exists:
            topicTab.click()
            #time.sleep(5)
        if self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.alibaba.micropc.appstore")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
                #time.sleep(5)
        logger.info('Exit -- MUAT:AppSystemTest:test_EnterAppstoreTopicTab')
        
    def test_EnterAppstoreMyApp(self):
        logger.info('Enter -- MUAT:AppSystemTest:test_EnterAppstoreMyApp')
        apk_manager = ApkManager()
        value = {}
        #report = MuatReport()
        if self.param and self.param.parameters and self.param.parameters.serial_number:
            serial_number = self.param.parameters.serial_number
        
        AppStoreIcon = self.d(text=u"应用商店", className="android.widget.TextView")
        click_x = AppStoreIcon.info['visibleBounds']['left'] +5
        click_y = AppStoreIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
                break
            else:
                time.sleep(1)
        if not self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists)
        topicTab = self.d(text=u"我的应用", resourceId="com.alibaba.micropc.appstore:id/myappTab")
        if not topicTab.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(topicTab.exists)
        if topicTab.exists:
            topicTab.click()
            #time.sleep(5)
        if self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.alibaba.micropc.appstore")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
                #time.sleep(5)
        logger.info('Exit -- MUAT:AppSystemTest:test_EnterAppstoreMyApp')
        
        
        
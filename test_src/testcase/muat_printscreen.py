#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import logging
import unittest
import shutil
import inspect
import sys
from dependency import screen_shot
from dependency.imagehelper import *
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

class PrintScreenTest(ParametrizedTestCase):
    def setUp(self):
        # check monitor running status
        if self.mon and not self.mon.running_status:
            self.skipTest('process monitor stop')

        self.d      = AutomationDevice().get_device()
        self.account = Account(self.d)
        self.mouse = AdbMouse()
        self.adb_tools = AdbTools()
        
        self.BaseImagePath = os.path.join(os.path.abspath(os.path.dirname("__file__")), "dependency", "BaseImage")
        self.FailureIamgePath = os.path.join(os.path.abspath(os.path.dirname("__file__")), "test-reports", "FailureImage")
        self.TmpImagePath = os.path.join(os.path.abspath(os.path.dirname("__file__")), "test-reports", "TmpImage")
        
        if not os.path.exists(self.TmpImagePath):
            os.mkdir(self.TmpImagePath)
        if not os.path.exists(os.path.join(self.TmpImagePath, "croped")):
            os.mkdir(os.path.join(self.TmpImagePath, "croped"))

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
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.ali.screenshot")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
            self.adb_tools.adb_shell('am force-stop com.ali.screenshot')
        
    def tearDown(self):
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.ali.screenshot")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
            time.sleep(1)
        if closeButton.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
            self.adb_tools.adb_shell('am force-stop com.ali.screenshot')
            self.assertFalse(closeButton.exists)
            if os.path.exists(self.TmpImagePath):
                shutil.rmtree(self.TmpImagePath)
            
    def test_OpenAndExit(self):
        logger.info('Enter -- MUAT:PrintScreenTest:test_OpenAndExit')
        ScreenIcon = self.d(text=u"截屏", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        if not ScreenIcon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(ScreenIcon.exists)
        click_x = ScreenIcon.info['visibleBounds']['left'] +5
        click_y = ScreenIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        time.sleep(1)
        ScreenTitle = self.d(resourceId="android:id/pc_titlebar", packageName="com.ali.screenshot")
        self.assertTrue(ScreenTitle.exists)
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.ali.screenshot")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
            time.sleep(1)
        logger.info('Exit -- MUAT:PrintScreenTest:test_OpenAndExit')
        
#     def test_StartByShortcut(self):
#         logger.info('Enter -- MUAT:PrintScreenTest:test_StartByShortcut')
    def test_FullScreenShot(self):
        logger.info('Enter -- MUAT:PrintScreenTest:test_FullScreenShot')
        ScreenIcon = self.d(text=u"截屏", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        if not ScreenIcon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(ScreenIcon.exists)
        click_x = ScreenIcon.info['visibleBounds']['left'] +5
        click_y = ScreenIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        time.sleep(1)
        ScreenTitle = self.d(resourceId="android:id/pc_titlebar", packageName="com.ali.screenshot")
        self.assertTrue(ScreenTitle.exists)
        full_screenshot=self.d(resourceId='com.ali.screenshot:id/m_connect_win_button',packageName='com.ali.screenshot')
        if full_screenshot.exists:
            full_screenshot.click()
            time.sleep(2)
            self.mouse.click(1690,10,constants.MouseLeftKey)
            self.mouse.click(1690,90,constants.MouseLeftKey)
            time.sleep(1)
            FileManagePic=self.d(resourceId='com.yunpc.filemanager:id/paraList_imgHead',packageName='com.yunpc.filemanager')
            self.assertTrue(FileManagePic.exists)
            self.d(resourceId='android:id/pc_close',packageName='com.yunpc.filemanager').click()
        logger.info('Exit -- MUAT:PrintScreenTest:test_FullScreenShot')
        
    def test_AreaScreenShot(self):
        logger.info('Enter -- MUAT:PrintScreenTest:test_AreaScreenShot')
        ScreenIcon = self.d(text=u"截屏", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        if not ScreenIcon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(ScreenIcon.exists)
        click_x = ScreenIcon.info['visibleBounds']['left'] +5
        click_y = ScreenIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        time.sleep(1)
        ScreenTitle = self.d(resourceId="android:id/pc_titlebar", packageName="com.ali.screenshot")
        self.assertTrue(ScreenTitle.exists)
        area_screenshot=self.d(resourceId='com.ali.screenshot:id/m_connect_rect_button',packageName='com.ali.screenshot')
        if area_screenshot.exists:
            area_screenshot.click()
            time.sleep(1)
            self.d.swipe(300,250,800,750,20)
            time.sleep(1)
            self.d(resourceId='com.ali.screenshot:id/s_crop_ok_button',packageName='com.ali.screenshot').click()
            time.sleep(1)
            self.mouse.click(1690,10,constants.MouseLeftKey)
            self.mouse.click(1690,90,constants.MouseLeftKey)
            time.sleep(1)
            self.assertTrue(self.d(resourceId='com.yunpc.filemanager:id/paraList_imgHead',packageName='com.yunpc.filemanager').exists)
            self.d(resourceId='android:id/pc_close',packageName='com.yunpc.filemanager').click()
        logger.info('Exit -- MUAT:PrintScreenTest:test_AreaScreenShot')
        
    def test_Cancle(self):
        logger.info('Enter -- MUAT:test_PrintScreen:test_Cancle')
        ScreenIcon = self.d(text=u"截屏", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        if not ScreenIcon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(ScreenIcon.exists)
        click_x = ScreenIcon.info['visibleBounds']['left'] +5
        click_y = ScreenIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        time.sleep(1)
        ScreenTitle = self.d(resourceId="android:id/pc_titlebar", packageName="com.ali.screenshot")
        self.assertTrue(ScreenTitle.exists)
        area_screenshot=self.d(resourceId='com.ali.screenshot:id/m_connect_rect_button',packageName='com.ali.screenshot')
        if area_screenshot.exists:
            area_screenshot.click()
            time.sleep(1)
            self.d.swipe(300,250,800,750,20)
            time.sleep(1)
            self.d(resourceId='com.ali.screenshot:id/s_crop_cancel_button',packageName='com.ali.screenshot').click()
            time.sleep(1)
            self.mouse.click(1690,10,constants.MouseLeftKey)
            self.mouse.click(1670,90,constants.MouseLeftKey)
            self.assertFalse(self.d(resourceId='com.yunpc.filemanager:id/paraList_imgHead',packageName='com.yunpc.filemanager').exists)
            time.sleep(1)
        logger.info('Exit -- MUAT:PrintScreenTest:test_Cancle')
        
    def test_DragScreen(self):
        logger.info('Enter -- MUAT:test_PrintScreen:test_DragScreen') 
        ScreenIcon = self.d(text=u"截屏", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        if not ScreenIcon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(ScreenIcon.exists)
        click_x = ScreenIcon.info['visibleBounds']['left'] +5
        click_y = ScreenIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        time.sleep(1)
        ScreenTitle = self.d(resourceId="android:id/pc_titlebar", packageName="com.ali.screenshot")
        self.assertTrue(ScreenTitle.exists)
        area_screenshot=self.d(resourceId='com.ali.screenshot:id/m_connect_rect_button',packageName='com.ali.screenshot')
        if area_screenshot.exists:
            area_screenshot.click()
            time.sleep(1)
            self.d.swipe(300,250,800,750,20)
            time.sleep(1)
            self.d.drag(500,400,900,700,10)
            time.sleep(1)
            self.assertTrue(self.d(resourceId='com.ali.screenshot:id/s_crop_ok_button',packageName='com.ali.screenshot').exists)
            self.d(resourceId='com.ali.screenshot:id/s_crop_ok_button',packageName='com.ali.screenshot').click()
            time.sleep(1)
            self.mouse.click(1690,10,constants.MouseLeftKey)
            self.mouse.click(1670,90,constants.MouseLeftKey)
            time.sleep(0.5)
            self.assertTrue(self.d(resourceId='com.yunpc.filemanager:id/paraList_imgHead',packageName='com.yunpc.filemanager').exists)
            time.sleep(1)
            self.d(resourceId='android:id/pc_close',packageName='com.yunpc.filemanager').click()
        
        logger.info('Exit -- MUAT:PrintScreenTest:test_DragScreen')
        
        
        
        
        
        
        
        
        
        
        
        
        
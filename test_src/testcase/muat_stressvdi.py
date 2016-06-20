#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import logging
import unittest
from dependency.parametrized_test_case import ParametrizedTestCase
from dependency.automation_device import AutomationDevice
from dependency.account import Account
from dependency import constants
from dependency.apk_manager import ApkManager
from dependency.adb_tools import AdbTools
from muat_report import MuatReport, GenerateResult
from dependency.adb_log import AdbLog
from dependency.adb_mouse import AdbMouse

# Init logger
logger_name = '%s-%s' % (constants.LOGGER_CLIENT_MUAT, os.getpid())
logger = logging.getLogger(logger_name)

class StressVdiTest(ParametrizedTestCase):
    def setUp(self):
        # check monitor running status
        if self.mon and not self.mon.running_status:
            self.skipTest('process monitor stop')

        self.d      = AutomationDevice().get_device()
        self.account = Account(self.d)
        self.adb_tools = AdbTools()
        self.mouse = AdbMouse()

        self.account.sleep()
        self.account.wakeup()
        self.account.login()
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.yunos.acdp")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()

    def tearDown(self):
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.yunos.acdp")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
        self.account.sleep()

    def test_LoginWin7(self):
        logger.info('Enter -- MUAT:StressVdiTest:test_LoginWin7')
   
        # open yunpc application
        YunPCIcon = self.d(text=u"云PC", className="android.widget.TextView")
        click_x = YunPCIcon.info['visibleBounds']['left'] +5
        click_y = YunPCIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        logger.info('StressVdiTest:test_LoginWin7: open yunpc application')
        time.sleep(2)
         
        YunPCWindow = self.d(className="android.widget.FrameLayout", packageName="com.yunos.acdp")
        self.assertTrue(YunPCWindow.exists)
        
        for cnt in range(2):
            if YunPCWindow.exists:
                # click the bg image enter Win7 login page
                VMWindow= self.d(resourceId="com.yunos.acdp:id/yunpc_bg", className="android.widget.LinearLayout", packageName="com.yunos.acdp")
                click_x= (VMWindow.info['visibleBounds']['left'] + VMWindow.info['visibleBounds']['right']) / 2
                click_y= (VMWindow.info['visibleBounds']['top'] + VMWindow.info['visibleBounds']['bottom']) / 2
                self.mouse.click(click_x, click_y, constants.MouseLeftKey)
                time.sleep(4)
                 
#                 # login Win7
#                 CanvasPage= self.d(resourceId="com.yunos.acdp:id/vnc_canvas", className="android.view.View", packageName="com.yunos.acdp")
#                 # enter passws
#                 CanvasPage.set_text(constants.TEST_PASSWD)
#                 time.sleep(1)
                
    
#                 # click login, enter button offset (930, 560)
#                 click_x= CanvasPage.info['visibleBounds']['left'] + 930
#                 click_y= CanvasPage.info['visibleBounds']['top'] + 560
#                 self.mouse.click(click_x, click_y, constants.MouseLeftKey)
#                 time.sleep(4)
                # screenshot for check
                name = '%s-%s.png' % (time.strftime('%Y%m%d%H%M%S', time.localtime()), cnt)
                logger.info('StressVdiTest:test_LoginWin7: screen shot name: (%s)' % (name))
                self.d.screenshot('%s-%s.png' % (time.strftime('%Y%m%d%H%M%S', time.localtime()), cnt))
                
                self.d.press(0x84, 0x1000|0x02)
                time.sleep(1)

        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.yunos.acdp")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()

        logger.info('Exit -- MUAT:StressVdiTest:test_LoginWin7')

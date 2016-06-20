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

class CunTaoTest(ParametrizedTestCase):
    def setUp(self):
        # check monitor running status
        if self.mon and not self.mon.running_status:
            self.skipTest('process monitor refresh_button')

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
        start1=time.time()
        while time.time()-start1<constants.Time_Out:
            if not Button1.exists:
                break
            else:
                time.sleep(1)
        #time.sleep(5)
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
        #self.adb_tools.adb_shell('am force-refresh_button org.chromium.chrome')
        #time.sleep(3)
       
        Browser_Icon = self.d(text=u"浏览器",resourceId='com.aliyun.lightdesk:id/tag_name', className="android.widget.TextView")
        if not Browser_Icon.exists:
            pass
            #self.adb_tools.adb_shell('adb shell am force-stop com.kingsoft.moffice_pro')
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
#             if self.mon and not self.mon.running_status:
#                 self.skipTest('process monitor refresh_button')
# 
#             self.d      = AutomationDevice().get_device()
#             self.account = Account(self.d)
#             self.mouse = AdbMouse()
#             self.adb_tools = AdbTools()
#         
#             self.BaseImagePath = os.path.join(os.path.abspath(os.path.dirname("__file__")), "dependency", "BaseImage")
#             self.FailureIamgePath = os.path.join(os.path.abspath(os.path.dirname("__file__")), "test-reports", "FailureImage")
#             self.TmpImagePath = os.path.join(os.path.abspath(os.path.dirname("__file__")), "test-reports", "TmpImage")
#         
#             if not os.path.exists(self.TmpImagePath):
#                 os.mkdir(self.TmpImagePath)
#             if not os.path.exists(os.path.join(self.TmpImagePath, "croped")):
#                 os.mkdir(os.path.join(self.TmpImagePath, "croped"))
# 
#             self.account.wakeup()
#             self.account.login()
#             Button1=self.d(resourceId='com.yunpc.yunosloginui:id/avatar')
#             start=time.time()
#             while time.time()-start<constants.Time_Out:
#                 if not Button1.exists:
#                     break
#                 else:
#                     time.sleep(1)
#             self.d.click(950,562)
#             #time.sleep(2)
#             Button1=self.d(resourceId='android:id/button1',className='android.widget.Button',packageName='android')
#             if Button1.exists:
#                 Button1.click()
#             time.sleep(1)
            if not Browser_Icon.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(Browser_Icon.exists)

    def tearDown(self):
        Button1=self.d(resourceId='android:id/button1',className='android.widget.Button',packageName='android')
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
        if Button1.exists:
            Button1.click()
            self.adb_tools.adb_shell('am start -n org.chromium.chrome/.browser.ChromeTabbedActivity')
            start=time.time()
            while time.time()-start <  constants.Time_Out:
                if closeButton.exists:
                    break
                else:
                    time.sleep(1)
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
            time.sleep(1)
        if closeButton.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertFalse(closeButton.exists)
        self.adb_tools.adb_shell('am force-stop org.chromium.chrome')    
        time.sleep(1)
        
    def test_Login(self):
        logger.info('Enter -- MUAT:CuntaoTest:test_login')
        BrowserIcon = self.d(text=u"浏览器", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        refresh_buttonButton=self.d(description=u'停止网页加载',resourceId='org.chromium.chrome:id/refresh_button')
        if not BrowserIcon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserIcon.exists)
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if  self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome").exists:
                break
            else:
                time.sleep(1)
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            maxButton = self.d(resourceId="android:id/pc_max", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if maxButton.exists:
                logger.debug('click max button: (%s)' % (maxButton.info['packageName']))
                maxButton.click()
#             blankpage = self.d(resourceId="org.chromium.chrome:id/title")
#             if blankpage.exists:
#                 self.assertEqual(blankpage.info['text'], u"搜索或输入网址")
            address = self.d(resourceId="org.chromium.chrome:id/url_bar")
            if address.exists:
                self.assertEqual(address.info['text'], u"搜索或输入网址")
                address.clear_text()
                address.set_text("cun.taobao.com")
                self.d.press(0x42)
                #sleep
                start=time.time()
                while time.time()-start<constants.TIME_OUT:
                    if not refresh_buttonButton.exists:
                        break
                    else:
                        time.sleep(1)
                time.sleep(5)
                #关闭广告
                self.d.click(1545,182)
                time.sleep(5)
                #点击请登陆
                self.d.click(409,177)
                #sleep
                time.sleep(20)
                self.d.press(61)
#                 self.d.press(113,1)
                time.sleep(0.5)
                self.d.press(48)
                self.d.press(33)
                self.d.press(47)
                self.d.press(48)
                self.d.press(33)
                self.d.press(46)
                self.d.press(69,1)
                self.d.press(8)
                self.d.press(61)
#                 self.d.press(113,1)
                time.sleep(0.5)
                self.d.press(48)
                self.d.press(33)
                self.d.press(47)
                self.d.press(48)
                self.d.press(8)
                self.d.press(9)
                self.d.press(10)
                self.d.press(11)
                self.d.press(66)
                #sleep
                time.sleep(25)
                self.d.click(425,180)
                time.sleep(3)
                self.d.click(393,251)
                time.sleep(5)
                  
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:CuntaoTest:test_login')
  		 
    def test_Shopping(self):
        logger.info('Enter -- MUAT:CuntaoTest:test_Shopping')
        BrowserIcon = self.d(text=u"浏览器", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        refresh_buttonButton=self.d(description=u'停止网页加载',resourceId='org.chromium.chrome:id/refresh_button')
        if not BrowserIcon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserIcon.exists)
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if  self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome").exists:
                break
            else:
                time.sleep(1)
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            maxButton = self.d(resourceId="android:id/pc_max", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if maxButton.exists:
                logger.debug('click max button: (%s)' % (maxButton.info['packageName']))
                maxButton.click()
#             blankpage = self.d(resourceId="org.chromium.chrome:id/title")
#             if blankpage.exists:
#                 self.assertEqual(blankpage.info['text'], u"搜索或输入网址")
            address = self.d(resourceId="org.chromium.chrome:id/url_bar")
            #addButton = self.d(resourceId="org.chromium.chrome:id/newtab")
            if address.exists:
                self.assertEqual(address.info['text'], u"搜索或输入网址")
                address.clear_text()
                address.set_text("cun.taobao.com")
                self.d.press(0x42)
                #sleep
                time.sleep(20)
                self.d.click(1545,182)
                time.sleep(5)
                self.d.click(409,177)
                #sleep
                time.sleep(20)
                self.d.press(61)
#                 self.d.press(113,1)
                time.sleep(0.5)
                self.d.press(48)
                self.d.press(33)
                self.d.press(47)
                self.d.press(48)
                self.d.press(33)
                self.d.press(46)
                self.d.press(69,1)
                self.d.press(8)
                self.d.press(61)
#                 self.d.press(113,1)
                time.sleep(0.5)
                self.d.press(48)
                self.d.press(33)
                self.d.press(47)
                self.d.press(48)
                self.d.press(8)
                self.d.press(9)
                self.d.press(10)
                self.d.press(11)
                self.d.press(66)
                #sleep
                start=time.time()
                while time.time()-start<constants.TIME_OUT:
                    if not refresh_buttonButton.exists:
                        break
                    else:
                        time.sleep(1)
                #通过输入网址找耳机
                #addButton.click()
                address.clear_text()
                address.set_text("https://detail.tmall.com/item.htm?id=18936252543&ali_trackid=2:mm_33231723_0_0:1437708324_2k3_1993164502&spm=5759.1411664.1111.4.xBX2i5&skuId=63591272480")
                self.d.press(0x42)
                #sleep
                time.sleep(20)
                self.d.click(1172,985)
                time.sleep(10)
                self.d.click(1209,176)
                start=time.time()
                while time.time()-start<constants.TIME_OUT:
                    if not refresh_buttonButton.exists:
                        break
                    else:
                        time.sleep(1)
                self.d.click(384,361)
                time.sleep(5)
                self.d.click(454,587)
                time.sleep(5)
                self.d.click(832,633)
                time.sleep(5)
                self.d.click(470,182)
                time.sleep(5) 
                self.d.click(678,219)
                time.sleep(5)
                  
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:CuntaoTest:test_Shopping')   
 							
 
    def test_AddAddress(self):
        logger.info('Enter -- MUAT:CuntaoTest:test_AddAddress')
        BrowserIcon = self.d(text=u"浏览器", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        refresh_buttonButton=self.d(description=u'停止网页加载',resourceId='org.chromium.chrome:id/refresh_button')
        if not BrowserIcon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserIcon.exists)
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if  self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome").exists:
                break
            else:
                time.sleep(1)
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            maxButton = self.d(resourceId="android:id/pc_max", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if maxButton.exists:
                logger.debug('click max button: (%s)' % (maxButton.info['packageName']))
                maxButton.click()
#             blankpage = self.d(resourceId="org.chromium.chrome:id/title")
#             if blankpage.exists:
#                 self.assertEqual(blankpage.info['text'], u"搜索或输入网址")
            address = self.d(resourceId="org.chromium.chrome:id/url_bar")
            if address.exists:
                self.assertEqual(address.info['text'], u"搜索或输入网址")
                address.clear_text()
                address.set_text("cun.taobao.com")
                self.d.press(0x42)
                #sleep
                start=time.time()
                while time.time()-start<constants.TIME_OUT:
                    if not refresh_buttonButton.exists:
                        break
                    else:
                        time.sleep(1)
                time.sleep(5)
                #关闭广告
                self.d.click(1545,182)
                time.sleep(5)
                #点击请登陆
                self.d.click(409,177)
                #sleep
                time.sleep(20)
                self.d.press(61)
#                 self.d.press(113,1)
                time.sleep(0.5)
                self.d.press(48)
                self.d.press(33)
                self.d.press(47)
                self.d.press(48)
                self.d.press(33)
                self.d.press(46)
                self.d.press(69,1)
                self.d.press(8)
                self.d.press(61)
#                 self.d.press(113,1)
                time.sleep(0.5)
                self.d.press(48)
                self.d.press(33)
                self.d.press(47)
                self.d.press(48)
                self.d.press(8)
                self.d.press(9)
                self.d.press(10)
                self.d.press(11)
                self.d.press(66)
                #sleep
                start=time.time()
                while time.time()-start<constants.TIME_OUT:
                    if not refresh_buttonButton.exists:
                        break
                    else:
                        time.sleep(1)
                time.sleep(5)
                self.d.click(1545,182)
                time.sleep(5)
                self.d.click(413,177)
                time.sleep(2)
                self.d.click(392,221)
                time.sleep(15)
                #点击收货地址
                self.d.click(512,656)
                time.sleep(10)
                self.d.click(921,384)
                time.sleep(2)
                self.d.click(882,454)
                time.sleep(2)
                self.d.click(882,454)
                time.sleep(2)
                self.d.click(882,454)
                time.sleep(2)
                self.d.click(882,454)
                time.sleep(2)
                self.d.click(882,454)
                self.d.press(35)
                time.sleep(1)
                button1=self.d(text=u'继续',resourceId='android:id/button1',packageName='org.chromium.chrome')
                if button1.exists:
                    button1.click()
                self.d.press(61)
                self.d.press(35)
                self.d.press(35)
                self.d.press(35)
                self.d.press(35)
                self.d.press(61)
                self.d.press(8)
                self.d.press(61)
                self.d.press(35)
                self.d.press(35)
                self.d.press(61)
                self.d.press(61)
                self.d.press(8)
                self.d.press(8)
                self.d.press(8)
                self.d.press(8)
                self.d.press(8)
                self.d.press(8)
                self.d.press(66)
                time.sleep(5)
                self.d.click(1280,825)    
                time.sleep(3)
                self.d.click(886,644)
                time.sleep(5)
                #登出
                self.d.click(573,180)
                time.sleep(2) 
                self.d.click(781,219)
                time.sleep(3)
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:CunTaoTest:test_AddAddress')
        
    def test_Search(self):
        logger.info('Enter -- MUAT:CuntaoTest:test_Search')
        BrowserIcon = self.d(text=u"浏览器", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        refresh_buttonButton=self.d(description=u'停止网页加载',resourceId='org.chromium.chrome:id/refresh_button')
        if not BrowserIcon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserIcon.exists)
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if  self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome").exists:
                break
            else:
                time.sleep(1)
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            maxButton = self.d(resourceId="android:id/pc_max", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if maxButton.exists:
                logger.debug('click max button: (%s)' % (maxButton.info['packageName']))
                maxButton.click()
#             blankpage = self.d(resourceId="org.chromium.chrome:id/title")
#             if blankpage.exists:
#                 self.assertEqual(blankpage.info['text'], u"搜索或输入网址")
            address = self.d(resourceId="org.chromium.chrome:id/url_bar")
            if address.exists:
                self.assertEqual(address.info['text'], u"搜索或输入网址")
                address.clear_text()
                address.set_text("cun.taobao.com")
                self.d.press(0x42)
                time.sleep(20)
                #关闭广告
                self.d.click(1545,182)
                time.sleep(5)
                self.d.click(731,246)
                self.d.press(29)
                self.d.press(32)
                self.d.press(37)
                self.d.press(32)
                self.d.press(29)
                self.d.press(47)
                self.d.press(66)
                time.sleep(15)
                 
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
                self.assertFalse(closeButton.exists)
        logger.info('Exit -- MUAT:CunTaoTest:test_Search')
                
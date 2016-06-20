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

class BrowserTest(ParametrizedTestCase):
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
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
        self.adb_tools.adb_shell('am force-stop org.chromium.chrome')
        #time.sleep(3)
        
        Browser_Icon = self.d(text=u"浏览器",resourceId='com.aliyun.lightdesk:id/tag_name', className="android.widget.TextView")
        if not Browser_Icon.exists:
#             self.d.click(57,10)
#             time.sleep(1)
#             self.d.click(68,141)
#             start=time.time()
#             while time.time()-start<constants.Time_Out:
#                 if  Button1.exists:
#                     break
#                 else:
#                     time.sleep(1)

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

            self.account.wakeup()
            self.account.login()
            Button1=self.d(resourceId='com.yunpc.yunosloginui:id/avatar')
            start=time.time()
            while time.time()-start<constants.Time_Out:
                if not Button1.exists:
                    break
                else:
                    time.sleep(1)
            #time.sleep(5)
            self.d.click(950,562)
            time.sleep(1)
            Button1=self.d(resourceId='android:id/button1',className='android.widget.Button',packageName='android')
            if Button1.exists:
                Button1.click()
            time.sleep(1)
            if not Browser_Icon.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(Browser_Icon.exists)

    def tearDown(self):
        Button1=self.d(resourceId='android:id/button1',className='android.widget.Button',packageName='android')
        if Button1.exists:
            Button1.click()
            self.adb_tools.adb_shell('am start -n org.chromium.chrome/.browser.ChromeTabbedActivity')
            start=time.time()
            while time.time()-start<constants.Time_Out:
                if  self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome").exists:
                    break
                else:
                    time.sleep(1)
        
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
            time.sleep(1)
        if closeButton.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertFalse(closeButton.exists)
        self.adb_tools.adb_shell('am force-stop org.chromium.chrome')
        if os.path.exists(self.TmpImagePath):
            shutil.rmtree(self.TmpImagePath)
            
    def test_OpenAndExit(self):
        logger.info('Enter -- MUAT:BrowserTest:test_OpenAndExit')
        BrowserIcon = self.d(text=u"浏览器", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        if not BrowserIcon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserIcon.exists)
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if  BrowserWindow.exists:
                break
            else:
                time.sleep(1)
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:BrowserTest:test_OpenAndExit')
         
    def test_BlankPage(self):
        logger.info('Enter -- MUAT:BrowserTest:test_BlankPage')
        BrowserIcon = self.d(text=u"浏览器", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        self.assertTrue(BrowserIcon.exists)
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if  BrowserWindow.exists:
                break
            else:
                time.sleep(1)
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            #blankpage title cannot find
            # blankpage = self.d(resourceId="org.chromium.chrome:id/url_bar")
            # if blankpage.exists:
            #     logger.info(blankpage.info)
            #     self.assertEqual(blankpage.info['text'], u'搜索或输入网址')
            address = self.d(resourceId="org.chromium.chrome:id/url_bar")
            if address.exists:
                self.assertEqual(address.info['text'], u"搜索或输入网址")
                 
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:BrowserTest:test_BlankPage')
        
    def test_InputAddr(self):
        logger.info('Enter -- MUAT:BrowserTest:test_InputAddr')
        BrowserIcon = self.d(text=u"浏览器",resourceId='com.aliyun.lightdesk:id/tag_name', className="android.widget.TextView")
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
            screen_shot.ScreenShot(self, name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            blankpage = self.d(resourceId="org.chromium.chrome:id/ntp_scrollview")
            if blankpage.exists:
                self.assertEqual(blankpage.info['contentDescription'], u"打开新的标签页")
            address = self.d(resourceId="org.chromium.chrome:id/url_bar")
            if address.exists:
                self.assertEqual(address.info['text'], u"搜索或输入网址")
                address.clear_text()
                address.set_text("www.baidu.com")
                self.d.press(0x42)
                StopButton=self.d(description=u'停止加载网页',resourceId='org.chromium.chrome:id/refresh_button')
                start=time.time()
                while time.time()-start<constants.TIME_OUT:
                    if not StopButton.exists:
                        break
                    else:
                        time.sleep(1)
                   
                baiduPage = self.d(className="android.webkit.WebView", packageName="org.chromium.chrome")
                if baiduPage.exists:
                    self.assertEqual(baiduPage.info['contentDescription'], u'百度一下，你就知道')
                                
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:BrowserTest:test_InputAddr')
        
    def test_RefreshPage(self):
        logger.info('Enter -- MUAT:BrowserTest:test_RefreshPage')
        BrowserIcon = self.d(text=u"浏览器", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
   
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
            screen_shot.ScreenShot(self, name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            self.assertTrue(self.d.press(0x8d))
            time.sleep(2)
            blankpage = self.d(resourceId="org.chromium.chrome:id/ntp_scrollview")
            if blankpage.exists:
                self.assertEqual(blankpage.info['contentDescription'], u"打开新的标签页")
            address = self.d(resourceId="org.chromium.chrome:id/url_bar")
            if address.exists:
                self.assertEqual(address.info['text'], u"搜索或输入网址")
                address.clear_text()
                address.set_text("time")
                self.d.press(0x42)
                time.sleep(5)
                StopButton=self.d(description=u'停止加载网页',resourceId='org.chromium.chrome:id/refresh_button')
                start=time.time()
                while time.time()-start<constants.TIME_OUT:
                    if not StopButton.exists:
                        break
                    else:
                        time.sleep(1)
                timebaiduPage = self.d(resourceId="org.chromium.chrome:id/url_bar")
                if timebaiduPage.exists:
                    if timebaiduPage.info['text'] == 'https://www.baidu.com/s?ie=UTF-8&wd=time':
                        name1 = "test_RefreshPage_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
                        img = os.path.join(self.TmpImagePath, name1)
                        self.d.screenshot(img)
                        cropedImgPath1 = os.path.join(self.TmpImagePath, "croped", name1.replace(".jpg", "_croped.jpg"))
                        CropImage(img, cropedImgPath1, 125, 266, 470, 366)
     
                        refreshButton = self.d(resourceId="org.chromium.chrome:id/refresh_button", className="android.widget.ImageButton", packageName="org.chromium.chrome")
                        if refreshButton.exists:
                            refreshButton.click()
                            start=time.time()
                            while time.time()-start<constants.TIME_OUT:
                                if not StopButton.exists:
                                    break
                                else:
                                    time.sleep(1)
                             
                            name2 = "test_RefreshPage_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
                            img = os.path.join(self.TmpImagePath, name2)
                            self.d.screenshot(img)
                            cropedImgPath2 = os.path.join(self.TmpImagePath, "croped", name2.replace(".jpg", "_croped.jpg"))
                            CropImage(img, cropedImgPath2, 125, 266, 470, 366)
                                 
                            if  CompareImage(cropedImgPath1, cropedImgPath2, 0.99):
                                shutil.copy(cropedImgPath1, os.path.join(self.FailureIamgePath, name1.replace(".jpg", "_failure.jpg")))
                                shutil.copy(cropedImgPath2, os.path.join(self.FailureIamgePath, name2.replace(".jpg", "_failure.jpg")))
                                path = os.path.join(self.FailureIamgePath, name1.replace(".jpg", "_failure.jpg"))
                                self.fail("The failure file path is %s" % path)
            # pageCloseBt = self.d(resourceId="com.android.browser:id/close")
            # if pageCloseBt.exists:
            #     pageCloseBt.click()
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:BrowserTest:test_RefreshPage')
            
    def test_ForwardOrBackwrad(self):
        logger.info('Enter -- MUAT:BrowserTest:test_ForwardOrBackwrad')
        BrowserIcon = self.d(text=u"浏览器", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        if not BrowserIcon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserIcon.exists)
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome").exists:
                break
            else:
                time.sleep(1)
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            # blankpage = self.d(resourceId="com.android.browser:id/title")
            # if blankpage.exists:
            #     self.assertEqual(blankpage.info['text'], "about:blank")
            address = self.d(resourceId="org.chromium.chrome:id/url_bar")
            if address.exists:
                self.assertEqual(address.info['text'], u"搜索或输入网址")
                address.clear_text()
                address.set_text("www.baidu.com")
                self.d.press(0x42)
                time.sleep(5)
   
            baiduPage = self.d(className='android.webkit.WebView', packageName='org.chromium.chrome')
            logger.info('assert baidu title....................................')
            if baiduPage.exists:
                if baiduPage.info['contentDescription'] == u'百度一下，你就知道':
   
                    address = self.d(resourceId="org.chromium.chrome:id/url_bar")
                    if address.exists:
                        address.click()
                        address.clear_text()
                        address.set_text("www.taobao.com")
                        self.d.press(0x42)
                        time.sleep(5)
                                
                taobaoPage = self.d(className='android.webkit.WebView', packageName='org.chromium.chrome')
                if taobaoPage.exists:
                    self.assertEqual(taobaoPage.info['contentDescription'], u'淘宝网 - 淘！我喜欢')
                    backButton = self.d(resourceId="org.chromium.chrome:id/back_button", className="android.widget.ImageButton", packageName="org.chromium.chrome")
                    if backButton.exists:
                        backButton.click()
                        time.sleep(5)
                        baiduPage = self.d(className='android.webkit.WebView', packageName='org.chromium.chrome')
                        if baiduPage.exists:
                            self.assertEqual(baiduPage.info['contentDescription'], u'百度一下，你就知道')
                    forwardButton = self.d(resourceId="org.chromium.chrome:id/forward_button", className="android.widget.ImageButton", packageName="org.chromium.chrome")
                    if forwardButton.exists:
                        forwardButton.click()
                        time.sleep(5)
                taobaoPage = self.d(className='android.webkit.WebView', packageName='org.chromium.chrome')
                if taobaoPage.exists:
                    self.assertEqual(taobaoPage.info['contentDescription'], u'淘宝网 - 淘！我喜欢')
                                                
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:BrowserTest:test_ForwardOrBackwrad')
            
        
    def test_BaiduSearch(self):
        logger.info('Enter -- MUAT:BrowserTest:test_BaiduSearch')
        BrowserIcon = self.d(text=u"浏览器", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
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
        # StopButton=self.d(description=u'停止网页加载',resourceId='com.android.browser:id/stop')
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            blankpage = self.d(resourceId="org.chromium.chrome:id/ntp_scrollview")
            if blankpage.exists:
                self.assertEqual(blankpage.info['contentDescription'], u"打开新的标签页")
            address = self.d(resourceId="org.chromium.chrome:id/url_bar")
            if address.exists:
                self.assertEqual(address.info['text'], u"搜索或输入网址")
                address.clear_text()
                address.set_text("time")
                self.d.press(0x42)
                StopButton=self.d(description=u'停止加载网页',resourceId='org.chromium.chrome:id/refresh_button')
                start=time.time()
                while time.time()-start<constants.TIME_OUT:
                    if not StopButton.exists:
                        break
                    else:
                        time.sleep(1)
                timebaiduPage = self.d(className="android.webkit.WebView", packageName="org.chromium.chrome")
                if timebaiduPage.exists:
                    self.assertEqual(timebaiduPage.info['contentDescription'], u'time_百度搜索')
                         
            # pageCloseBt = self.d(resourceId="com.android.browser:id/close")
            # if pageCloseBt.exists:
            #     pageCloseBt.click()
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:BrowserTest:test_BaiduSearch')
         
    def test_EmptyBookmark(self):
        logger.info('Enter -- MUAT:BrowserTest:test_EmptyBookmark')
        BrowserIcon = self.d(text=u"浏览器", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
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
            menuButton = self.d(resourceId="org.chromium.chrome:id/menu_button", className="android.widget.ImageButton", packageName="org.chromium.chrome")
            if menuButton.exists:
                menuButton.click()
                time.sleep(2)
                bookmarkbtn = self.d(resourceId="org.chromium.chrome:id/menu_item_text")
                if bookmarkbtn.exists:
                    bookmarkbtn.click()
                    time.sleep(1)
   
                bookmarkLabel = self.d(resourceId="org.chromium.chrome:id/eb_empty_view")
                if not bookmarkLabel.exists:
                    name = sys._getframe().f_code.co_name
                    screen_shot.ScreenShot(self, name)
                self.assertTrue(bookmarkLabel.exists)
                     
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:BrowserTest:test_EmptyBookmark')
           
    def test_SearchWebPage(self):
        #调用logger模块进行log信息输出，此处是info级别，使用debug级别请使用：logger.debug("AAA")
        logger.info('Enter -- MUAT:BrowserTest:test_SearchWebPage')
        #调用py-uiautomator进行查找标题为“浏览器”，类名为“android.widget.TextView”的浏览器图标
        BrowserIcon = self.d(text=u"浏览器", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        if not BrowserIcon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserIcon.exists)
 
        #通过上一步获得浏览器图标的位置信息，计算出需要鼠标双击的位置，及图标的左坐标+5， 上坐标+5，这个坐标正好位于图标可单击范围之中
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        #调用mouse模块的双击函数，对上面计算到的坐标进行双击操作，打开浏览器窗口
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if  self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome").exists:
                break
            else:
                time.sleep(1)
        #调用py-uiautomator进行查找类名为"android.widget.FrameLayout"，包名"com.android.browser"的浏览器窗口
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        #断言检查浏览器窗口是否存在，若存在，BrowserWindow.exists会返回true，反之false
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertTrue(BrowserWindow.exists)
        #当浏览器窗口存在时
        if BrowserWindow.exists:
            #按下0x8d的键值，此键值在android中的含义是F11按键，具体的keycode请参考：http://developer.android.com/reference/android/view/KeyEvent.html
            self.assertTrue(self.d.press(0x8d))
            #断言检查是否存在资源ID为"com.android.browser:id/title"的浏览器页面
            blankpage = self.d(resourceId="org.chromium.chrome:id/ntp_scrollview")
            if blankpage.exists:
                #断言检查上面存在的浏览器页面的标题是否为“about:blank”
                self.assertEqual(blankpage.info['contentDescription'], u"打开新的标签页")
            #查找浏览器地址栏
            address = self.d(resourceId="org.chromium.chrome:id/url_bar")
            if address.exists:
                self.assertEqual(address.info['text'], u"搜索或输入网址")
                #清空地址栏
                address.clear_text()
                #地址栏输入“www.baidu.com”
                address.set_text("www.baidu.com")
                #按键0x24，即回车键
                self.d.press(0x42)
                StopButton=self.d(description=u'停止加载网页',resourceId='org.chromium.chrome:id/refresh_button')
#                 time.sleep(5)
                start=time.time()
                while time.time()-start<constants.TIME_OUT:
                    if not StopButton.exists:
                        break
                    else:
                        time.sleep(1)
                baiduPage = self.d(className="android.webkit.WebView", packageName="org.chromium.chrome")
                if baiduPage.exists:
                    #断言检查浏览器页面标题是否为：“百度一下，你就知道”，注意中文要用u修饰，表示此为utf8编码中文
                    self.assertEqual(baiduPage.info['contentDescription'], u'百度一下，你就知道')
                    #在浏览器中查找选项按钮
                    # menubtn = self.d(resourceId="org.chromium.chrome:id/menu_button")
                    # self.assertEqual(menubtn.info['contentDescription'], u'更多选项')
                    # if menubtn.exists:
                    #     menubtn.click()
                    #     time.sleep(1)
                    for button in self.d(resourceId="org.chromium.chrome:id/menu_button"):
                        if button.info['contentDescription'] == u'更多选项':
                            #按下“更多选项”按钮
                            button.click()
                            searchButton = self.d(text=u"在网页中查找", resourceId="org.chromium.chrome:id/menu_item_text")
                            if searchButton.exists:
                                #按下“在网页上查找”按钮
                                searchButton.click()
                                editView = self.d(text=u"在网页中查找", resourceId="org.chromium.chrome:id/find_query")
                                if editView.exists:
                                    #清空查找框
                                    editView.clear_text()
                                    # self.d.press(0x36, 0x71)
                                    #查找"About"字符
                                    editView.set_text(u"baidu")
                                    self.d.press(0x42)
                                    time.sleep(3)
                                    #截图，命名为test_SearchWebPage_%时间戳.jpg，此时截图是整个屏幕
                                    BaseImg = os.path.join(self.BaseImagePath, "test_SearchWebPage.jpg")
                                    name = "test_SearchWebPage_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
                                    img = os.path.join(self.TmpImagePath, name)
                                    self.d.screenshot(img)
                                    #裁剪图片，与基准图大小一致，位置一致
                                    cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
                                    # CropImage(img, cropedImgPath, 1000, 945, 1090, 970)
                                    CropImage(img, cropedImgPath, 1200,950,1290,975)
                                    #比较上一步裁剪后的图片与基准图片
                                    if not CompareImage(cropedImgPath, BaseImg, 0.99):
                                        shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
                                        path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
                                        self.fail("The failure file path is %s" % path)
                            break
            #点击关闭按钮，关闭浏览器
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        #输出测试用例退出log信息        
        logger.info('Exit -- MUAT:BrowserTest:test_SearchWebPage')
        
#     def test_CostTime(self):
#         logger.info('Enter -- MUAT:BrowserTest:test_CostTime')
#         BrowserIcon = self.d(text=u"浏览器", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
#         if not BrowserIcon.exists:
#             name = sys._getframe().f_code.co_name
#             screen_shot.ScreenShot(self,name)
#         self.assertTrue(BrowserIcon.exists)
#         click_x = BrowserIcon.info['visibleBounds']['left'] +5
#         click_y = BrowserIcon.info['visibleBounds']['top'] +5
#         self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
#         start=time.time()
#         while time.time()-start<constants.Time_Out:
#             if  self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome").exists:
#                 break
#             else:
#                 time.sleep(1)
#         BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
#         if not BrowserWindow.exists:
#             name = sys._getframe().f_code.co_name
#             screen_shot.ScreenShot(self,name)
#         self.assertTrue(BrowserWindow.exists)
#         if BrowserWindow.exists:
#             blankpage = self.d(resourceId="org.chromium.chrome:id/ntp_scrollview")
#             if blankpage.exists:
#                 self.assertEqual(blankpage.info['contentDescription'], u"打开新的标签页")
#             address = self.d(resourceId="org.chromium.chrome:id/url_bar")
#             if address.exists:
#                 self.assertEqual(address.info['text'], u"搜索或输入网址")
#                 address.clear_text()
#                 address.set_text("www.taobao.com")
#                 self.d.press(0x42)
#                 StopButton=self.d(description=u'停止加载网页',resourceId='org.chromium.chrome:id/refresh_button')
#                 start=time.time()
#                 while time.time()-start<constants.TIME_OUT:
#                     if not StopButton.exists:
#                         break
#                     else:
#                         time.sleep(0.5)
#                 logger.info( time.time()-start)
#                 detect_re = None #re.compile(r'D.UIAutomatorStub.*%s.*dragTo' % (apk_info.package_name))
#                 wanted_re = re.compile(r'MPT: sf post one frame at (.*)$')
#                 adb_log = AdbLog(mode=AdbLog.MODE_RE | AdbLog.MODE_NEED_DETECT | AdbLog.MODE_NEED_CONTINUE, wanted_re=wanted_re, detect_re=detect_re, logger=logger)
#                 adb_log.clear()
#                 adb_log.start()
#                 logger.info("动作之前")
#                 
#                 self.mouse.wheel(860,500,constants.MouseWheelDown,60,5)
#                 self.mouse.wheel(860,500,constants.MouseWheelUp,50,5)
#                 logger.info("动作之后")
#                 # check the log and get the data
#                 while True:
#                     if adb_log.result and len(adb_log.result) >= 3:
#                         break
#                     else:
#                         time.sleep(1)
#                 logger.info("循环之后")
#                 adb_log.stop_log()
#                 adb_log.join()
# 
#                 # store the result
#                 start_time = 0
#                 end_time = 0
#                 fps = 0
#                 try:
#                     length = len(adb_log.result)
#                     if length >=3:
#                         start_time      = int(adb_log.result[1][0])
#                         end_time        = int(adb_log.result[-1][0])
# #                                                 logger.info(adb_log.result)
# #                                                 logger.info(length)
#                         fps             = (length - 1) * 1000 / (end_time - start_time)
#                     else:
#                         logger.error('not enough data for calc fps: (%s)' % (adb_log.result))
#                 except:
#                     logger.error('retrieve time from (%s) error' % (adb_log.result))
# 
#                 logger.info('drag %s fps: %s' % (2000, fps))
# #                 baiduPage = self.d(className="android.webkit.WebView", packageName="org.chromium.chrome")
# #                 if baiduPage.exists:
# #                     self.assertEqual(baiduPage.info['contentDescription'], u'百度一下，你就知道')
#                                
#             closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
#             if closeButton.exists:
#                 logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
#                 closeButton.click()
#         logger.info('Exit -- MUAT:BrowserTest:test_CostTime')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

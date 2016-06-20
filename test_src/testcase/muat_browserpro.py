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
from dependency.getcpuinfo import getcpuinfo


# Init logger
logger_name = '%s-%s' % (constants.LOGGER_CLIENT_MUAT, os.getpid())
logger = logging.getLogger(logger_name)

class BrowserProTest(ParametrizedTestCase):
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

        self.account.sleep()
        self.account.wakeup()
        self.account.login()
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
            
    def test_CostTime(self):
        logger.info('Enter -- MUAT:BrowserTest:test_CostTime')
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
            maxButton = self.d(resourceId="android:id/pc_max", className="android.widget.ImageView", packageName="org.chromium.chrome")
            logger.debug('click max button: (%s)' % (maxButton.info['packageName']))
            maxButton.click()
            blankpage = self.d(resourceId="org.chromium.chrome:id/ntp_scrollview")
            if blankpage.exists:
                self.assertEqual(blankpage.info['contentDescription'], u"打开新的标签页")
            address = self.d(resourceId="org.chromium.chrome:id/url_bar")
            if address.exists:
                self.assertEqual(address.info['text'], u"搜索或输入网址")
#                 address.clear_text()
#                 address.set_text("www.taobao.com")
#                 self.d.press(0x42)
                MenuButton=self.d(resourceId='org.chromium.chrome:id/menu_button',packageName='org.chromium.chrome')
                if MenuButton.exists:
                    MenuButton.click()
                    time.sleep(1)
                    self.d(resourceId='org.chromium.chrome:id/menu_item_text',packageName='org.chromium.chrome').click()
                    BookMark=self.d(resourceId='org.chromium.chrome:id/highlight')
                    if BookMark.exists:
                        BookMark.click()
                        time.sleep(1)
                StopButton=self.d(description=u'停止加载网页',resourceId='org.chromium.chrome:id/refresh_button')
                start=time.time()
                while time.time()-start<constants.TIME_OUT:
                    if not StopButton.exists:
                        break
                    else:
                        time.sleep(0.5)
                logger.info( time.time()-start)
                 
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:BrowserTest:test_CostTime')
         
        
    def test_Fps(self):
        logger.info('Enter -- MUAT:BrowserTest:test_Fps')
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
            maxButton = self.d(resourceId="android:id/pc_max", className="android.widget.ImageView", packageName="org.chromium.chrome")
            logger.debug('click max button: (%s)' % (maxButton.info['packageName']))
            maxButton.click()
            blankpage = self.d(resourceId="org.chromium.chrome:id/ntp_scrollview")
            if blankpage.exists:
                self.assertEqual(blankpage.info['contentDescription'], u"打开新的标签页")
            address = self.d(resourceId="org.chromium.chrome:id/url_bar")
            if address.exists:
                self.assertEqual(address.info['text'], u"搜索或输入网址")
                MenuButton=self.d(resourceId='org.chromium.chrome:id/menu_button',packageName='org.chromium.chrome')
                if MenuButton.exists:
                    MenuButton.click()
                    time.sleep(1)
                    self.d(resourceId='org.chromium.chrome:id/menu_item_text',packageName='org.chromium.chrome').click()
                    BookMark=self.d(resourceId='org.chromium.chrome:id/highlight')
                    if BookMark.exists:
                        BookMark.click()
                        time.sleep(1)
                StopButton=self.d(description=u'停止加载网页',resourceId='org.chromium.chrome:id/refresh_button')
                start=time.time()
                while time.time()-start<constants.TIME_OUT:
                    if not StopButton.exists:
                        break
                    else:
                        time.sleep(0.5)
                detect_re = re.compile(r'D.UIAutomatorStub.*swipe')
                wanted_re = re.compile(r'MPT: sf post one frame at (.*)$')
                adb_log = AdbLog(mode=AdbLog.MODE_RE | AdbLog.MODE_NEED_DETECT | AdbLog.MODE_NEED_CONTINUE, wanted_re=wanted_re, detect_re=detect_re, logger=logger)
                adb_log.clear()
                adb_log.start()
                self.d.swipe(200,900,200,500)
                 
                self.mouse.wheel(860,500,constants.MouseWheelDown,70,5)
                self.mouse.wheel(860,500,constants.MouseWheelUp,60,5)
                # check the log and get the data
                while True:
                    if adb_log.result and len(adb_log.result) >= 3:
                        break
                    else:
                        time.sleep(1)
                adb_log.stop_log()
                adb_log.join()
 
                # store the result
                start_time = 0
                end_time = 0
                fps = 0
                try:
                    length = len(adb_log.result)
                    if length >=3:
                        start_time      = int(adb_log.result[1][0])
                        end_time        = int(adb_log.result[-1][0])
                        fps             = (length - 1) * 1000 / (end_time - start_time)
                    else:
                        logger.error('not enough data for calc fps: (%s)' % (adb_log.result))
                except:
                    logger.error('retrieve time from (%s) error' % (adb_log.result))
 
                logger.info('wheel taobao page fps: %s' % ( fps))
#                 baiduPage = self.d(className="android.webkit.WebView", packageName="org.chromium.chrome")
#                 if baiduPage.exists:
#                     self.assertEqual(baiduPage.info['contentDescription'], u'百度一下，你就知道')
                                
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:BrowserTest:test_Fps')
        
    def test_Open16Tab(self):
        logger.info('Enter -- MUAT:ChromeTest:test_Open16Tab')
        
        #open chrome
        self.adb_tools.adb_shell("am start -n org.chromium.chrome/com.google.android.apps.chrome.Main")
        time.sleep(3)
        pc_max = self.d(resourceId='android:id/pc_max', className='android.widget.ImageView', packageName='org.chromium.chrome')
        pc_max.click()
        time.sleep(2)
        menuButton=self.d(resourceId='org.chromium.chrome:id/menu_button',packageName='org.chromium.chrome')
        menuButton.click()
        records=self.d(text=u"历史记录",packageName='org.chromium.chrome')
        records.click()
       
        for i in range(16):
            self.mouse.click(830,430,constants.MouseRightKey)
            self.mouse.click(890,460,constants.MouseLeftKey)
            time.sleep(1)
        str ='after open chrome 16 tab...\n' 
        getcpuinfo(str)
        #close chrome
        closebtn = self.d(resourceId='android:id/pc_close', className='android.widget.ImageView', packageName='org.chromium.chrome')
        closebtn.click()

        logger.info('Exit -- MUAT:ChromeTest:test_OpenChromeTab')
        
    def test_LanchTask(self):
        logger.info('Enter -- MUAT:ChromeTest:test_LanchTask')
        serial_number = None
        if self.param and self.param.parameters and self.param.parameters.serial_number:
            serial_number = self.param.parameters.serial_number
        #open chrome
        self.adb_tools.adb_shell("am start -n org.chromium.chrome/com.google.android.apps.chrome.Main")
        time.sleep(3)
        pc_max = self.d(resourceId='android:id/pc_max', className='android.widget.ImageView', packageName='org.chromium.chrome')
        self.assertTrue(pc_max.exists)
        pc_max.click()
        time.sleep(2)
        menuButton=self.d(resourceId='org.chromium.chrome:id/menu_button',packageName='org.chromium.chrome')
        menuButton.click()
        records=self.d(text=u"历史记录",packageName='org.chromium.chrome')
        records.click()
       
        for i in range(16):
            self.mouse.click(830,430,constants.MouseRightKey)
            self.mouse.click(890,460,constants.MouseLeftKey)
            time.sleep(1)
        str ='lanch taskmgr after open chrome 16 tab...\n' 
        getcpuinfo(str)
            
        wanted_re = re.compile(r'I.ActivityManager.*com.aliyun.mpc.taskmgr.*\+(.*)ms' )
        adb_log = AdbLog(mode=AdbLog.MODE_RE, wanted_re=wanted_re, logger=logger, serial_number=serial_number)
        adb_log.clear()
        adb_log.start()

        # start apk
        self.adb_tools.adb_shell('am start -n  com.aliyun.mpc.taskmgr/.TaskMgr')
        
        # check the log and get the data
        while True:
            if adb_log.result:
                break
            else:
                time.sleep(1)
        # store the result
        cost_time = 0
        try:
            if 's' in adb_log.result[0][0]:
                composit = adb_log.result[0][0].split('s')
                cost_time = int(composit[0]) * 1000 + int(composit[1])
            else:
                cost_time = int(adb_log.result[0][0])
        except:
            logger.error('retrieve cost time from (%s) error' % (adb_log.result))
        
        logger.info('start TaskMgr cost: %s' % (cost_time))
        # close apk
        self.adb_tools.adb_shell('am force-stop com.aliyun.mpc.taskmgr')
        #close chrome
        closebtn = self.d(resourceId='android:id/pc_close', className='android.widget.ImageView', packageName='org.chromium.chrome')
        closebtn.click()

        logger.info('Exit -- MUAT:ChromeTest:test_LanchTask')
        
    def test_LanchApplist(self):
        logger.info('Enter -- MUAT:ChromeTest:test_LanchApplist')
        serial_number = None
        if self.param and self.param.parameters and self.param.parameters.serial_number:
            serial_number = self.param.parameters.serial_number
        #open chrome
        self.adb_tools.adb_shell("am start -n org.chromium.chrome/com.google.android.apps.chrome.Main")
        time.sleep(3)
        pc_max = self.d(resourceId='android:id/pc_max', className='android.widget.ImageView', packageName='org.chromium.chrome')
        pc_max.click()
        time.sleep(2)
        menuButton=self.d(resourceId='org.chromium.chrome:id/menu_button',packageName='org.chromium.chrome')
        menuButton.click()
        records=self.d(text=u"历史记录",packageName='org.chromium.chrome')
        records.click()
        # 从历史记录中打开网页
        for i in range(16):
            self.mouse.click(830,430,constants.MouseRightKey)
            self.mouse.click(890,460,constants.MouseLeftKey)
            time.sleep(1)
        str ='lanch applist after open chrome 16 tab...\n' 
        getcpuinfo(str)
            
        # click blank region to disappear applist
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(1)

        # start adb log capture thread
        detect_re = re.compile(r'MPT click .(%s), (%s). at (.*)$' % (constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y))
        wanted_re = re.compile(r'MPT: sf post one frame at (.*)$')

        adb_log = AdbLog(mode=AdbLog.MODE_RE | AdbLog.MODE_NEED_DETECT, wanted_re=wanted_re, detect_re=detect_re, logger=logger, serial_number=serial_number)
        adb_log.clear()
        adb_log.start()

        # click app list
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        logger.debug('click applist point (%s,%s)' % (constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y))
        time.sleep(2)

        # check the log and get the data
        while True:
            if len(adb_log.result) == 2:
                break
            else:
                time.sleep(1)

        # store the result
        click_point_x = 0
        click_point_y = 0
        start_time = 0
        end_time = 0
        cost_time = 0
        try:
            click_point_x   = int(adb_log.result[0][0])
            click_point_y   = int(adb_log.result[0][1])
            start_time      = int(adb_log.result[0][2])
            end_time        = int(adb_log.result[1][0])
            if click_point_x == constants.MUAT_APP_LIST_POINT_X and click_point_y == constants.MUAT_APP_LIST_POINT_Y:
                cost_time = end_time - start_time
            else:
                logger.error('detect_re detect the wrong point: (%s)' % (adb_log.result[0]))
        except:
            logger.error('retrieve time from (%s) error' % (adb_log.result))

        logger.info('start applist cost: %s' % (cost_time))
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(1)
        #close chrome
        closebtn = self.d(resourceId='android:id/pc_close', className='android.widget.ImageView', packageName='org.chromium.chrome')
        closebtn.click()
        logger.info('Exit -- MUAT:ChromeTest:test_LanchApplist')
        
    def test_Open10AppTab(self):
        logger.info('Enter -- MUAT:ChromeTest:test_Open10AppTab')
        serial_number = None
        if self.param and self.param.parameters and self.param.parameters.serial_number:
            serial_number = self.param.parameters.serial_number
        
        #open youku
        self.adb_tools.adb_shell('am start -n com.youku.phone.x86/com.youku.phone.x86.ActivityWelcome')
        time.sleep(3)
        #open ttpod
        logger.info('open the ttpod application................')
        self.adb_tools.adb_shell("am start -n com.sds.android.ttpod/.EntryActivity")
        time.sleep(3)
        #open QQ
        logger.info('open QQ application.......................')
        self.adb_tools.adb_shell("am start -n com.tencent.mobileqq/.activity.SplashActivity")
        time.sleep(3)
        #open xiami
        logger.info('open xiami application.......................')
        self.adb_tools.adb_shell("am start -n fm.xiami.main/fm.xiami.bmamba.activity.StartMainActivity")
        time.sleep(3)
        #open qianniu
        logger.info('open qianniiu application.......................')
        self.adb_tools.adb_shell('am start -n com.taobao.qianniu/.ui.InitActivity')
        time.sleep(3)
        #open weibo
        logger.info('open weibo application.......................')
        self.adb_tools.adb_shell('am start -n com.sina.weibotab/.ui.ActivitySplash')
        time.sleep(3)
        #open wps_pro
        logger.info('open wps application.......................')
        self.adb_tools.adb_shell("am start -n com.kingsoft.moffice_pro/cn.wps.moffice.documentmanager.PreStartActivity")
        time.sleep(3)
        #open gaode map
        logger.info('open minimap application.......................')
        self.adb_tools.adb_shell("am start -n com.autonavi.minimap/.Splashy")
        time.sleep(3)
        #open wangxin
        logger.info('open mobileim application.......................')
        self.adb_tools.adb_shell("am start -n com.alibaba.mobileim/.SplashActivity")
        time.sleep(3)
        #open taobao
        logger.info('open taobaoHD application.......................')
        self.adb_tools.adb_shell("am start -n com.taobao.apad/.activity.MainActivity")
        time.sleep(3)
        #open chrome
        self.adb_tools.adb_shell("am start -n org.chromium.chrome/com.google.android.apps.chrome.Main")
        time.sleep(3)
        pc_max = self.d(resourceId='android:id/pc_max', className='android.widget.ImageView', packageName='org.chromium.chrome')
        self.assertTrue(pc_max.exists)
        pc_max.click()
        time.sleep(2)
        menuButton=self.d(resourceId='org.chromium.chrome:id/menu_button',packageName='org.chromium.chrome')
        menuButton.click()
        records=self.d(text=u"历史记录",packageName='org.chromium.chrome')
        records.click()
        for i in range(16):
            self.mouse.click(830,430,constants.MouseRightKey)
            self.mouse.click(890,460,constants.MouseLeftKey)
            time.sleep(1)
        str ='after 10Apps open chrome 16 tab...\n' 
        getcpuinfo(str)
        #记录打开applist的时间
         # click blank region to disappear applist
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(1)
        # start adb log capture thread
        detect_re = re.compile(r'MPT click .(%s), (%s). at (.*)$' % (constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y))
        wanted_re = re.compile(r'MPT: sf post one frame at (.*)$')

        adb_log = AdbLog(mode=AdbLog.MODE_RE | AdbLog.MODE_NEED_DETECT, wanted_re=wanted_re, detect_re=detect_re, logger=logger, serial_number=serial_number)
        adb_log.clear()
        adb_log.start()

        # click app list
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        logger.debug('click applist point (%s,%s)' % (constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y))
        time.sleep(2)

        # check the log and get the data
        while True:
            if len(adb_log.result) == 2:
                break
            else:
                time.sleep(1)

        # store the result
        click_point_x = 0
        click_point_y = 0
        start_time = 0
        end_time = 0
        cost_time = 0
        try:
            click_point_x   = int(adb_log.result[0][0])
            click_point_y   = int(adb_log.result[0][1])
            start_time      = int(adb_log.result[0][2])
            end_time        = int(adb_log.result[1][0])
            if click_point_x == constants.MUAT_APP_LIST_POINT_X and click_point_y == constants.MUAT_APP_LIST_POINT_Y:
                cost_time = end_time - start_time
            else:
                logger.error('detect_re detect the wrong point: (%s)' % (adb_log.result[0]))
        except:
            logger.error('retrieve time from (%s) error' % (adb_log.result))

        logger.info('after 10Apps start applist cost: %s' % (cost_time))
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        wanted_re = re.compile(r'I.ActivityManager.*com.aliyun.mpc.taskmgr.*\+(.*)ms' )
        adb_log = AdbLog(mode=AdbLog.MODE_RE, wanted_re=wanted_re, logger=logger, serial_number=serial_number)
        adb_log.clear()
        adb_log.start()
        
        #记录打开任务管理器的时间
        # start apk
        self.adb_tools.adb_shell('am start -n  com.aliyun.mpc.taskmgr/.TaskMgr')
        
        # check the log and get the data
        while True:
            if adb_log.result:
                break
            else:
                time.sleep(1)
        # store the result
        cost_time = 0
        try:
            if 's' in adb_log.result[0][0]:
                composit = adb_log.result[0][0].split('s')
                cost_time = int(composit[0]) * 1000 + int(composit[1])
            else:
                cost_time = int(adb_log.result[0][0])
        except:
            logger.error('retrieve cost time from (%s) error' % (adb_log.result))
        
        logger.info('after 10Apps start TaskMgr cost: %s' % (cost_time))
        # close apk
        self.adb_tools.adb_shell('am force-stop com.aliyun.mpc.taskmgr')
        
        #close youku
        logger.info('close the youku application................')
        self.adb_tools.adb_shell('am force-stop com.youku.phone.x86')
        time.sleep(2)
        #close ttpod
        logger.info('close the ttpod application................')
        self.adb_tools.adb_shell("am force-stop com.sds.android.ttpod")
        time.sleep(2)
        #close QQ
        logger.info('close QQ application.......................')
        self.adb_tools.adb_shell("am force-stop com.tencent.mobileqq")
        time.sleep(2)
        #close xiami
        logger.info('close xiami application.......................')
        self.adb_tools.adb_shell("am force-stop fm.xiami.main")
        time.sleep(2)
        #close qianniu
        logger.info('close qianniiu application.......................')
        self.adb_tools.adb_shell('am force-stop com.taobao.qianniu')
        time.sleep(2)
        #close weibo
        logger.info('close weibo application.......................')
        self.adb_tools.adb_shell('am force-stop com.sina.weibotab')
        time.sleep(2)
        #open wps_pro
        logger.info('close wps application.......................')
        self.adb_tools.adb_shell("am force-stop com.kingsoft.moffice_pro")
        time.sleep(2)
        #close gaode map
        logger.info('close minimap application.......................')
        self.adb_tools.adb_shell("am force-stop com.autonavi.minimap")
        time.sleep(2)
        #close wangxin
        logger.info('close mobileim application.......................')
        self.adb_tools.adb_shell("am force-stop com.alibaba.mobileim")
        time.sleep(2)
        #close taobao
        logger.info('close taobaoHD application.......................')
        self.adb_tools.adb_shell("am force-stop com.taobao.apad")
        time.sleep(2)
        #close chrome
        closebtn = self.d(resourceId='android:id/pc_close', className='android.widget.ImageView', packageName='org.chromium.chrome')
        closebtn.click()
        
        logger.info('Exit -- MUAT:ChromeTest:test_Open10AppTab')
        
        
        
        
        
        
        
        
        
        
        
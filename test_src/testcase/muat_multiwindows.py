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
from dependency.adb_tools import AdbTools
from muat_report import MuatReport, GenerateResult
from dependency.adb_log import AdbLog
from dependency.adb_mouse import AdbMouse

# Init logger
logger_name = '%s-%s' % (constants.LOGGER_CLIENT_MUAT, os.getpid())
logger = logging.getLogger(logger_name)

class MultiWindowsTest(ParametrizedTestCase):
    def setUp(self):
        # check monitor running status
        if self.mon and not self.mon.running_status:
            self.skipTest('process monitor stop')

        self.d      = AutomationDevice().get_device()
        self.account = Account(self.d)
        self.adb_tools = AdbTools()
        self.mouse = AdbMouse()

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
        Browser_Icon = self.d(text=u"浏览器",resourceId='com.aliyun.lightdesk:id/tag_name', className="android.widget.TextView")
        if not Browser_Icon.exists:
            self.d.click(57,10)
            time.sleep(2)
            self.d.click(68,141)
            start2=time.time()
            while time.time()-start2<constants.Time_Out:
                if  Button1.exists:
                    break
                else:
                    time.sleep(1)
            if self.mon and not self.mon.running_status:
                self.skipTest('process monitor stop')

            self.d      = AutomationDevice().get_device()
            self.account = Account(self.d)
            self.mouse = AdbMouse()
            self.adb_tools = AdbTools()
        

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
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="org.chromium.chrome")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
        self.adb_tools.adb_shell('am force-stop org.chromium.chrome')

#     def test_DragWindow(self):
#         logger.info('Enter -- MUAT:MultiWindowsTest:test_DragWindow')
#       
#         BrowserIcon = self.d(text=u"浏览器", className="android.widget.TextView")
#         click_x = BrowserIcon.info['visibleBounds']['left'] +5
#         click_y = BrowserIcon.info['visibleBounds']['top'] +5
#         self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
#             
#         BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="com.android.browser")
#         self.assertTrue(BrowserWindow.exists)
#         if BrowserWindow.exists:
#             #BrowserWindow = self.d(text=u"浏览器", resourceId="android:id/pc_title", className="android.widget.TextView", packageName="com.android.browser")
#             LowerRightCoordinate_X = BrowserWindow.info['visibleBounds']['right'] - 1
#             LowerRightCoordinate_Y = BrowserWindow.info['visibleBounds']['bottom'] - 1
#             Target_X = LowerRightCoordinate_X + 100
#             Target_Y = LowerRightCoordinate_Y + 100
#                 
#             # drag
#             self.assertTrue(self.d.drag(LowerRightCoordinate_X, LowerRightCoordinate_Y, Target_X, Target_Y))
#             time.sleep(2)
#             # new coordinate
#             #EndBrowserWindow = self.d(text=u"浏览器", resourceId="android:id/pc_title", className="android.widget.TextView", packageName="com.android.browser")
#             EndBrowserWindow = self.d(className="android.widget.FrameLayout", packageName="com.android.browser")
#             End_X = EndBrowserWindow.info['visibleBounds']['right'] -1 
#             End_Y = EndBrowserWindow.info['visibleBounds']['bottom'] -1
#     
#             # assert the math abs < 5 
#             self.assertTrue(abs(Target_X - End_X) < 5)
#             self.assertTrue(abs(Target_Y - End_Y) < 5)
#                 
#             self.assertTrue(self.d.drag(End_X, End_Y, LowerRightCoordinate_X, LowerRightCoordinate_Y))
#                             
#         logger.info('Exit -- MUAT:MultiWindowsTest:test_DragWindow')
          
          
    def test_ZoomInWindows(self):
        logger.info('Enter -- MUAT:MultiWindowsTest:test_ZoomInWindows')
             
        BrowserIcon = self.d(text=u"浏览器",resourceId='com.aliyun.lightdesk:id/tag_name', className="android.widget.TextView")
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
             
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            LowerRightCoordinate_X = BrowserWindow.info['visibleBounds']['right'] - 1
            LowerRightCoordinate_Y = BrowserWindow.info['visibleBounds']['bottom'] - 1
            Target_X = LowerRightCoordinate_X + 100
            Target_Y = LowerRightCoordinate_Y + 100
                 
            # drag
            self.assertTrue(self.d.drag(LowerRightCoordinate_X, LowerRightCoordinate_Y, Target_X, Target_Y))
            time.sleep(2)
            # new coordinate
            EndBrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            End_X = EndBrowserWindow.info['visibleBounds']['right'] -1 
            End_Y = EndBrowserWindow.info['visibleBounds']['bottom'] -1
     
            # assert the math abs < 5 
            #self.assertTrue(abs(Target_X - End_X) < 5)
            #self.assertTrue(abs(Target_Y - End_Y) < 5)
                 
            self.assertTrue(self.d.drag(End_X, End_Y, LowerRightCoordinate_X, LowerRightCoordinate_Y))
        logger.info('Exit -- MUAT:MultiWindowsTest:test_ZoomInWindows')
                 
    def test_ZoomOutWindows(self):
        logger.info('Enter -- MUAT:MultiWindowsTest:test_ZoomOutWindows')
        BrowserIcon = self.d(text=u"浏览器",resourceId='com.aliyun.lightdesk:id/tag_name', className="android.widget.TextView")
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
             
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            LowerRightCoordinate_X = BrowserWindow.info['visibleBounds']['right'] - 1
            LowerRightCoordinate_Y = BrowserWindow.info['visibleBounds']['bottom'] - 1
            Target_X = LowerRightCoordinate_X - 100
            Target_Y = LowerRightCoordinate_Y - 100
                 
            # drag
            self.assertTrue(self.d.drag(LowerRightCoordinate_X, LowerRightCoordinate_Y, Target_X, Target_Y))
            time.sleep(2)
            # new coordinate
            EndBrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            End_X = EndBrowserWindow.info['visibleBounds']['right'] -1 
            End_Y = EndBrowserWindow.info['visibleBounds']['bottom'] -1
     
            # assert the math abs < 5 
            #self.assertTrue(abs(Target_X - End_X) < 5)
            #self.assertTrue(abs(Target_Y - End_Y) < 5)
                  
            self.assertTrue(self.d.drag(End_X, End_Y, LowerRightCoordinate_X, LowerRightCoordinate_Y))
                                  
        logger.info('Exit -- MUAT:MultiWindowsTest:test_ZoomOutWindows')
          
    def test_ElongateWindow(self):
        logger.info('Enter -- MUAT:MultiWindowsTest:test_ElongateWindow')
        BrowserIcon = self.d(text=u"浏览器",resourceId='com.aliyun.lightdesk:id/tag_name', className="android.widget.TextView")
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
              
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            LowerRightCoordinate_X = BrowserWindow.info['visibleBounds']['right'] - 100
            LowerRightCoordinate_Y = BrowserWindow.info['visibleBounds']['bottom'] - 1
            Target_X = LowerRightCoordinate_X
            Target_Y = LowerRightCoordinate_Y + 100
      
            # drag
            self.assertTrue(self.d.drag(LowerRightCoordinate_X, LowerRightCoordinate_Y, Target_X, Target_Y))
      
            time.sleep(2)
      
            # new coordinate
            EndBrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            End_X = EndBrowserWindow.info['visibleBounds']['right'] -1 
            End_Y = EndBrowserWindow.info['visibleBounds']['bottom'] -1
      
            # assert the math abs < 5 
            self.assertTrue(abs(Target_Y - End_Y) < 5)
                  
            self.assertTrue(self.d.drag(End_X-100, End_Y, LowerRightCoordinate_X, LowerRightCoordinate_Y))
        logger.info('Exit -- MUAT:MultiWindowsTest:test_ElongateWindow')                
                  
    def test_WidenWindow(self):
        logger.info('Enter -- MUAT:MultiWindowsTest:test_WidenWindow')
        BrowserIcon = self.d(text=u"浏览器",resourceId='com.aliyun.lightdesk:id/tag_name', className="android.widget.TextView")
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
              
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            LowerRightCoordinate_X = BrowserWindow.info['visibleBounds']['right'] - 1
            LowerRightCoordinate_Y = BrowserWindow.info['visibleBounds']['bottom'] - 100
            Target_X = LowerRightCoordinate_X + 100
            Target_Y = LowerRightCoordinate_Y
      
            # drag
            self.assertTrue(self.d.drag(LowerRightCoordinate_X, LowerRightCoordinate_Y, Target_X, Target_Y))
      
            time.sleep(2)
      
            # new coordinate
            EndBrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            End_X = EndBrowserWindow.info['visibleBounds']['right'] -1 
            End_Y = EndBrowserWindow.info['visibleBounds']['bottom'] -1
      
            # assert the math abs < 5 
            self.assertTrue(abs(Target_X - End_X) < 5)
      
            self.assertTrue(self.d.drag(End_X, End_Y-100, LowerRightCoordinate_X, LowerRightCoordinate_Y))
                                  
        logger.info('Exit -- MUAT:MultiWindowsTest:test_WidenWindow')
      
    def test_F11ToFullScreen(self):
        logger.info('Enter -- MUAT:MultiWindowsTest:test_F11ToFullScreen')
        BrowserIcon = self.d(text=u"浏览器",resourceId='com.aliyun.lightdesk:id/tag_name', className="android.widget.TextView")
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
              
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            WindowTop = BrowserWindow.info['visibleBounds']['top']
            WindowLeft = BrowserWindow.info['visibleBounds']['left']
            WindowRight = BrowserWindow.info['visibleBounds']['right']
            WindowBottom = BrowserWindow.info['visibleBounds']['bottom']
                  
            # not full screen
            self.assertNotEqual(WindowTop, 0)
            self.assertNotEqual(WindowLeft, 0)
            self.assertNotEqual(WindowRight, 1920)
            self.assertNotEqual(WindowBottom, 1080)
                  
            # press F11 key
            self.assertTrue(self.d.press(0x8d))
      
            time.sleep(2)
      
            # new coordinate
            EndBrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            NewWindowTop = EndBrowserWindow.info['visibleBounds']['top']
            NewWindowLeft = EndBrowserWindow.info['visibleBounds']['left']
            NewWindowRight = EndBrowserWindow.info['visibleBounds']['right']
            NewWindowBottom = EndBrowserWindow.info['visibleBounds']['bottom']
                  
            # full screen
            self.assertEqual(NewWindowTop, 0)
            self.assertEqual(NewWindowLeft, 0)
            self.assertEqual(NewWindowRight, 1920)
            self.assertEqual(NewWindowBottom, 1080)
            if not self.d.press(0x8d):
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(self.d.press(0x8d))
                  
        logger.info('Exit -- MUAT:MultiWindowsTest:test_F11ToFullScreen')
             
             
    def test_maximization(self):
        logger.info('Enter -- MUAT:MultiWindowsTest:test_maximization')
        BrowserIcon = self.d(text=u"浏览器", resourceId='com.aliyun.lightdesk:id/tag_name',className="android.widget.TextView")
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
            
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            oldWindowTop = BrowserWindow.info['visibleBounds']['top']
            oldWindowLeft = BrowserWindow.info['visibleBounds']['left']
            oldWindowLeft1 = BrowserWindow.info['visibleBounds']['left']
            oldWindowRight = BrowserWindow.info['visibleBounds']['right']
            oldWindowRight1 = BrowserWindow.info['visibleBounds']['right']
            oldWindowBottom = BrowserWindow.info['visibleBounds']['bottom']
                
            # not maximization
            self.assertNotEqual(oldWindowTop, 0)
            self.assertNotEqual(oldWindowLeft, 0)
            self.assertNotEqual(oldWindowRight, 1920)
            self.assertNotEqual(oldWindowBottom, 1080)
                
            # maxmiun the window
            max_button = self.d(packageName="org.chromium.chrome", resourceId='android:id/pc_max')
            if max_button.exists:
                max_button.click()
                start=time.time()
                while time.time()-start<constants.Time_Out:
                    if oldWindowLeft1==0 and oldWindowRight1==1920:
                        break
                    else:
                        time.sleep(1)
                        oldWindowLeft1 = BrowserWindow.info['visibleBounds']['left']
                        oldWindowRight1 = BrowserWindow.info['visibleBounds']['right']
    
            # new coordinate
            EndBrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            NewWindowTop = EndBrowserWindow.info['visibleBounds']['top']
            NewWindowLeft = EndBrowserWindow.info['visibleBounds']['left']
            NewWindowRight = EndBrowserWindow.info['visibleBounds']['right']
            NewWindowBottom = EndBrowserWindow.info['visibleBounds']['bottom']
                
            # full screen
            # the topbar height 22px
            # the taskbar height 42px (1080-42=1038) 
            self.assertTrue(abs(NewWindowTop - 18) < 5)
            self.assertEqual(NewWindowLeft, 0)
            self.assertEqual(NewWindowRight, 1920)
            self.assertTrue(abs(NewWindowBottom- 1048) < 5)
                
            # reclick the max button
            if max_button.exists:
                max_button.click()
                start=time.time()
                while time.time()-start<constants.Time_Out:
                    if not NewWindowLeft==0:
                        break
                    else:
                        time.sleep(1)
                        NewWindowLeft = EndBrowserWindow.info['visibleBounds']['left']
                        
            # restore the window
            EndBrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            NewWindowTop = EndBrowserWindow.info['visibleBounds']['top']
            NewWindowLeft = EndBrowserWindow.info['visibleBounds']['left']
            NewWindowRight = EndBrowserWindow.info['visibleBounds']['right']
            NewWindowBottom = EndBrowserWindow.info['visibleBounds']['bottom']
            self.assertEqual(NewWindowTop, oldWindowTop)
            self.assertEqual(NewWindowLeft, oldWindowLeft)
            self.assertEqual(NewWindowRight, oldWindowRight)
            self.assertEqual(NewWindowBottom, oldWindowBottom)
                            
        logger.info('Exit -- MUAT:MultiWindowsTest:test_maximization')
            
    def test_minimization(self):
        logger.info('Enter -- MUAT:MultiWindowsTest:test_minimization')
        BrowserIcon = self.d(text=u"浏览器",resourceId='com.aliyun.lightdesk:id/tag_name', className="android.widget.TextView")
        click_x = BrowserIcon.info['visibleBounds']['left'] +5
        click_y = BrowserIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
           
        BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
        if not BrowserWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertTrue(BrowserWindow.exists)
        if BrowserWindow.exists:
            BrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            oldWindowTop = BrowserWindow.info['visibleBounds']['top']
            oldWindowLeft = BrowserWindow.info['visibleBounds']['left']
            oldWindowRight = BrowserWindow.info['visibleBounds']['right']
            oldWindowBottom = BrowserWindow.info['visibleBounds']['bottom']
               
            # not maximization
            self.assertNotEqual(oldWindowTop, 0)
            self.assertNotEqual(oldWindowLeft, 0)
            self.assertNotEqual(oldWindowRight, 1920)
            self.assertNotEqual(oldWindowBottom, 1080)
               
            # hide the window
            hide_button = self.d(packageName="org.chromium.chrome", resourceId='android:id/pc_hide')
            if hide_button.exists:
                hide_button.click()
                start=time.time()
                while time.time()-start<constants.Time_Out:
                    if not hide_button.exists:
                        break
                    else:
                        time.sleep(1)
   
            # check hide window
            if self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome").exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertFalse(self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome").exists)
                                               
            # click the browser in the taskbar
            self.mouse.click(100, 1080-25, constants.MouseLeftKey)
            start=time.time()
            while time.time()-start<constants.Time_Out:
                if  hide_button.exists:
                    break
                else:
                    time.sleep(1)
   
            # restore the window
            EndBrowserWindow = self.d(className="android.widget.FrameLayout", packageName="org.chromium.chrome")
            NewWindowTop = EndBrowserWindow.info['visibleBounds']['top']
            NewWindowLeft = EndBrowserWindow.info['visibleBounds']['left']
            NewWindowRight = EndBrowserWindow.info['visibleBounds']['right']
            NewWindowBottom = EndBrowserWindow.info['visibleBounds']['bottom']
            self.assertEqual(NewWindowTop, oldWindowTop)
            self.assertEqual(NewWindowLeft, oldWindowLeft)
            self.assertEqual(NewWindowRight, oldWindowRight)
            self.assertEqual(NewWindowBottom, oldWindowBottom)
                                      
        logger.info('Exit -- MUAT:MultiWindowsTest:test_minimization')



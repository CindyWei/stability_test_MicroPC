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

class DesktopSystemTest(ParametrizedTestCase):
    def setUp(self):
        # check monitor running status
        if self.mon and not self.mon.running_status:
            self.skipTest('process monitor stop')

        self.d      = AutomationDevice().get_device()
        self.account = Account(self.d)
        self.mouse = AdbMouse()
        self.mouse.move(1920, 1080)
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
        self.adb_tools.adb_shell('am force-stop com.alibaba.micropc.appstore')  
        AppStoreIcon = self.d(text=u"应用商店", className="android.widget.TextView")   
        if not AppStoreIcon.exists:
            start2=time.time()
            while time.time()-start2<constants.Time_Out:
                if  Button1.exists:
                    break
                else:
                    time.sleep(1)
            if not AppStoreIcon.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)

    def tearDown(self):
        self.adb_tools.adb_shell('am force-stop com.alibaba.micropc.appstore')    
        if os.path.exists(self.TmpImagePath):
            shutil.rmtree(self.TmpImagePath)
        time.sleep(1)
        
    def test_StatusBar(self):
        logger.info('Enter -- MUAT:DesktopSystemTest:test_StatusBar')
        BaseImg = os.path.join(self.BaseImagePath, "test_StatusBar.jpg")
        name = "test_StatusBar_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
        img = os.path.join(self.TmpImagePath, name)
        self.d.screenshot(img)
        cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
        CropImage(img, cropedImgPath, 0, 0, 1810, 25)
        if not CompareImage(cropedImgPath, BaseImg, 0.9):
            shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
            path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
            self.fail("The failure file path is %s") % path
        
        logger.info('Exit -- MUAT:DesktopSystemTest:test_StatusBar')
    
    def test_TaskBar(self):
        logger.info('Enter -- MUAT:DesktopSystemTest:test_TaskBar')
        
        AppStoreIcon = self.d(text=u"应用商店", className="android.widget.TextView")
        click_x = AppStoreIcon.info['visibleBounds']['left'] +5
        click_y = AppStoreIcon.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        appstoreWindow = self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore")
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if  appstoreWindow.exists:
                break
            else:
                time.sleep(1)
        if not appstoreWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        
        self.assertTrue(appstoreWindow.exists)
        self.mouse.click(appstoreWindow.info['visibleBounds']['left'] +10, appstoreWindow.info['visibleBounds']['top'] +10, constants.MouseLeftKey)
        
        hideButton = self.d(packageName="com.alibaba.micropc.appstore", resourceId='android:id/pc_hide')
        if hideButton.exists:
            hideButton.click()
            start=time.time()
            while time.time()-start<constants.Time_Out:
                if not hideButton.exists:
                    break
                else:
                    time.sleep(1)
            if self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            
            self.assertFalse(self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists)
            BaseImg = os.path.join(self.BaseImagePath, "test_TaskBar.jpg")
            name = "test_TaskBar_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
            img = os.path.join(self.TmpImagePath, name)
            self.d.screenshot(img)
            cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
            CropImage(img, cropedImgPath, 0, 1035, 70, 1080)
            if not CompareImage(cropedImgPath, BaseImg, 0.9):
                shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
                self.fail("The failure file path is %s") % os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
            self.mouse.click(35, 1050, constants.MouseLeftKey)
            start=time.time()
            while time.time()-start<constants.Time_Out:
                if  hideButton.exists:
                    break
                else:
                    time.sleep(1)
            if not self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore").exists)
            
        closeButton = self.d(packageName="com.alibaba.micropc.appstore", resourceId='android:id/pc_close')
        if closeButton.exists:
            closeButton.click()
        else:
            self.mouse.click(35, 1050, constants.MouseLeftKey)
            start=time.time()
            while time.time()-start<constants.Time_Out:
                if  hideButton.exists:
                    break
                else:
                    time.sleep(1)
            closeButton = self.d(packageName="com.alibaba.micropc.appstore", resourceId='android:id/pc_close')
            closeButton.click()
        logger.info('Exit -- MUAT:DesktopSystemTest:test_TaskBar')
    
    def test_DragIcon(self):
        logger.info('Enter -- MUAT:DesktopSystemTest:test_DragIcon')
        AppStoreIcon = self.d(text=u"应用商店", className="android.widget.TextView")
        if AppStoreIcon.exists:
            oldX = AppStoreIcon.info['visibleBounds']['left']
            oldY = AppStoreIcon.info['visibleBounds']['top']
            self.mouse.pressmove(AppStoreIcon.info['visibleBounds']['left'] + 5, AppStoreIcon.info['visibleBounds']['top'] + 5, 300, 300, constants.MouseLeftKey)
            time.sleep(5)
            newAppStoreIcon = self.d(text=u"应用商店", className="android.widget.TextView")
            if not newAppStoreIcon.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(newAppStoreIcon.exists)
            if newAppStoreIcon.exists:
                self.assertNotEqual(oldX, newAppStoreIcon.info['visibleBounds']['left'])
                self.assertNotEqual(oldY, newAppStoreIcon.info['visibleBounds']['top'])
                self.mouse.pressmove(newAppStoreIcon.info['visibleBounds']['left'] + 5, newAppStoreIcon.info['visibleBounds']['top'] + 5, -300, -300, constants.MouseLeftKey)
        logger.info('Exit -- MUAT:DesktopSystemTest:test_DragIcon')
    
    def test_DoubleClickIcon(self):
        logger.info('Enter -- MUAT:DesktopSystemTest:test_DoubleClickIcon')
        AppStoreIcon = self.d(text=u"应用商店", className="android.widget.TextView")
        if AppStoreIcon.exists:
            self.mouse.doubleclick(AppStoreIcon.info['visibleBounds']['left'] + 5, AppStoreIcon.info['visibleBounds']['top'] + 5, constants.MouseLeftKey)
            AppStoreWindow = self.d(className="android.widget.FrameLayout", packageName="com.alibaba.micropc.appstore")
            start=time.time()
            while time.time()-start<constants.Time_Out:
                if  AppStoreWindow.exists:
                    break
                else:
                    time.sleep(1)
            if not AppStoreWindow.exists:
               name = sys._getframe().f_code.co_name
               screen_shot.ScreenShot(self,name) 
            self.assertTrue(AppStoreWindow.exists)
            if AppStoreWindow.exists:
                closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.alibaba.micropc.appstore")
                if closeButton.exists:
                    logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                    closeButton.click()
                    #time.sleep(5)
        logger.info('Exit -- MUAT:DesktopSystemTest:test_DoubleClickIcon')
        
    def test_StartAppFromLMClick(self):
        logger.info('Enter -- MUAT:DesktopSystemTest:test_StartAppFromLMClick')

        # click the applist
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)

        # get applist picture
        BaseImg = os.path.join(self.BaseImagePath, "applist_browser.jpg")
        name = "test_StartAppFromLMClick_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
        img = os.path.join(self.TmpImagePath, name)
        self.d.screenshot(img)
        cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
        # (1292, 315) = 1920 - 120 * 5 - 18 - 10; 1080 - 136 * 5 - 18 - 25 - 42
        # (1892, 995) = 1920 - 18 - 10; 1080 - 18 - 25 - 42
        # region = array(5,5), with each 120 * 136
        CropImage(img, cropedImgPath, 1292, 315, 1892, 995)

        # find required image
        # compare pic rect of base image, it is 64*64 pix
        ret = FindImage(cropedImgPath, BaseImg, (28, 24, 92, 88), 50)
        if not ret:
            shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
            path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
            self.fail("The failure file path is %s" % path)
        else:
            # mouse left click the item
            self.mouse.click(1292 + ret[0], 315 + ret[1], constants.MouseLeftKey)

        # verify the item
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
        logger.info('Exit -- MUAT:DesktopSystemTest:test_StartAppFromLMClick')

    def test_StartAppFromRMClick(self):
        logger.info('Enter -- MUAT:DesktopSystemTest:test_StartAppFromRMClick')

        # click the applist
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)

        # get applist picture
        BaseImg = os.path.join(self.BaseImagePath, "applist_browser.jpg")
        name = "test_StartAppFromRMClick_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
        img = os.path.join(self.TmpImagePath, name)
        self.d.screenshot(img)
        cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
        # (1292, 315) = 1920 - 120 * 5 - 18 - 10; 1080 - 136 * 5 - 18 - 25 - 42
        # (1892, 995) = 1920 - 18 - 10; 1080 - 18 - 25 - 42
        # region = array(5,5), with each 120 * 136
        CropImage(img, cropedImgPath, 1292, 315, 1892, 995)

        # find required image
        # compare pic rect of base image, it is 64*64 pix
        ret = FindImage(cropedImgPath, BaseImg, (28, 24, 92, 88), 50)
        if not ret:
            shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
            path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
            self.fail("The failure file path is %s" % path)
        else:
            # mouse right click the item
            self.mouse.click(1292 + ret[0], 315 + ret[1], constants.MouseRightKey)
            time.sleep(1)
            # mouse left click start item
            self.mouse.click(1292 + ret[0] + 20, 315 + ret[1] + 20, constants.MouseLeftKey)

        # verify the item
        #time.sleep(2)
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
        logger.info('Exit -- MUAT:DesktopSystemTest:test_StartAppFromRMClick')

    def test_AddAPPIconToDesktop(self):
        logger.info('Enter -- MUAT:DesktopSystemTest:test_AddAPPIconToDesktop')

        # remove the shortcut from Desktop first
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        BrowserIcon = self.d(text=u"浏览器", className="android.widget.TextView")
        if BrowserIcon.exists:
            BrowserIcon_bounds = BrowserIcon.info['bounds']
            self.mouse.click((BrowserIcon_bounds['left'] + BrowserIcon_bounds['right']) / 2, (BrowserIcon_bounds['top'] + BrowserIcon_bounds['bottom']) / 2, constants.MouseRightKey)
            time.sleep(0.2)
            self.mouse.click((BrowserIcon_bounds['left'] + BrowserIcon_bounds['right']) / 2 + 50, (BrowserIcon_bounds['top'] + BrowserIcon_bounds['bottom']) / 2 + 50, constants.MouseLeftKey)
            time.sleep(0.2)
            deleteButton = self.d(text=u"删除", className="android.widget.Button")
            if deleteButton.exists:
                deleteButton.click()
                time.sleep(0.2)

        # click the applist
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)

        # get applist picture
        BaseImg = os.path.join(self.BaseImagePath, "applist_browser.jpg")
        name = "test_AddAPPIconToDesktop_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
        img = os.path.join(self.TmpImagePath, name)
        self.d.screenshot(img)
        cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
        # (1292, 315) = 1920 - 120 * 5 - 18 - 10; 1080 - 136 * 5 - 18 - 25 - 42
        # (1892, 995) = 1920 - 18 - 10; 1080 - 18 - 25 - 42
        # region = array(5,5), with each 120 * 136
        CropImage(img, cropedImgPath, 1292, 315, 1892, 995)

        # find required image
        # compare pic rect of base image, it is 64*64 pix
        ret = FindImage(cropedImgPath, BaseImg, (28, 24, 92, 88), 50)
        if not ret:
            shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
            path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
            self.fail("The failure file path is %s" % path)
        else:
            # mouse click and move the item to desktop
            self.mouse.pressmove(1292 + ret[0], 315 + ret[1], 0, -315 - ret[1], constants.MouseLeftKey)
            time.sleep(0.2)

        # verify the item
        time.sleep(2)
        BrowserIcon = self.d(text=u"浏览器", className="android.widget.TextView")
        if not BrowserIcon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(BrowserIcon.exists)
        logger.info('Exit -- MUAT:DesktopSystemTest:test_APPAddShortcutToDesktop')

#     def test_UninstallAPP(self):
#         logger.info('Enter -- MUAT:DesktopSystemTest:test_UninstallAPP')
# 
#         apk_manager = ApkManager()
#         apk = 'appstore.apk'
# 
#         # install app first
#         if apk in apk_manager.local_apks_info:
#             # stop appstore if the apk already started
#             apk_manager.close_apk(apk)
#  
#             # start appstore 
#             apk_manager.start_apk(apk)
#             time.sleep(1)
#              
#             myapp = self.d(text=u"我的应用", packageName="com.alibaba.micropc.appstore")
#             self.assertTrue(myapp.exists)
#             if myapp.exists:
#                 myapp.click()
#                 time.sleep(2)
#                 etao = self.d(text=u"一淘", packageName="com.alibaba.micropc.appstore").sibling(text=u"已安装", packageName="com.alibaba.micropc.appstore")
#                 if etao.exists:
#                     print 'found etao installed'
#                     pass
#                 else:
#                     print 'not found etao installed'
#                     # 分类，娱乐，一淘，安装
#                     category = self.d(text=u"分类", packageName="com.alibaba.micropc.appstore")
#                     self.assertTrue(category.exists)
#                     if category.exists:
#                         category.click()
#                         time.sleep(1)
#                         fun = self.d(description=u"娱乐 Link", packageName="com.alibaba.micropc.appstore")
#                         self.assertTrue(fun.exists)
#                         if fun.exists:
#                             fun.click()
#                             time.sleep(1)
#                             fun_etao = self.d(description=u"一淘", packageName="com.alibaba.micropc.appstore").sibling(className="android.widget.Image")
#                             self.assertTrue(fun_etao.exists)
#                             if fun_etao.exists:
#                                 fun_etao.click()
#                                 time.sleep(1)
#                                 etao_install = self.d(description=u"安 装", packageName="com.alibaba.micropc.appstore")
#                                 etao_installed = self.d(description=u"已安装", packageName="com.alibaba.micropc.appstore")
#                                 #self.assertTrue(etao_install.exists)
#                                 if etao_install.exists:
#                                     etao_install.click()
#                                     # wait until install complete
#                                     while True:
#                                         etao_complete = self.d(description=u"已安装", packageName="com.alibaba.micropc.appstore")
#                                         if etao_complete.exists:
#                                             break
#                                         else:
#                                             time.sleep(5)
#                                 else:
#                                     self.assertTrue(etao_installed.exists)
# 
#             apk_manager.close_apk(apk)
#             time.sleep(0.2)
# 
#         # click the applist
#         self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
#         time.sleep(0.2)
#         self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
#         time.sleep(1)
# 
#         # get applist picture
#         BaseImg = os.path.join(self.BaseImagePath, "applist_etao.jpg")
#         name = "test_StartAppFromRMClick_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
#         img = os.path.join(self.TmpImagePath, name)
#         self.d.screenshot(img)
#         cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
#         # (980, 404)   = 1920 - 152 * 6 - 12 - 16; 1080 - 152 * 4 - 16 - 52
#         # (1892, 1012) = 1920 - 12 - 16; 1080 - 16 - 52
#         # region = array(6,4), with each 152 *152
#         CropImage(img, cropedImgPath, 980, 404, 1892, 1012)
# 
#         # find required image
#         ret = FindImage(cropedImgPath, BaseImg, (40, 20, 112, 92), 60)
#         if not ret:
#             shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
#             path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
#             self.fail("The failure file path is %s" % path)
#         else:
#             # uninstall app
#             self.mouse.click(980 + ret[0], 404 + ret[1], constants.MouseRightKey)
#             time.sleep(0.2)
#             self.mouse.click(980 + ret[0] + 50, 404 + ret[1] + 80, constants.MouseLeftKey)
#             time.sleep(0.2)
#             deleteButton = self.d(text=u"确定", className="android.widget.Button")
#             if deleteButton.exists:
#                 deleteButton.click()
#                 time.sleep(0.2)
# 
#         # verify the app status
#         if apk in apk_manager.local_apks_info:
#             # start appstore 
#             apk_manager.start_apk(apk)
#             time.sleep(1)
#              
#             myapp = self.d(text=u"我的应用", packageName="com.alibaba.micropc.appstore")
#             self.assertTrue(myapp.exists)
#             if myapp.exists:
#                 myapp.click()
#                 time.sleep(1)
#                 etao_after_delete = self.d(text=u"一淘", packageName="com.alibaba.micropc.appstore").sibling(text=u"已安装", packageName="com.alibaba.micropc.appstore")
#                 self.assertFalse(etao_after_delete.exists)
#             apk_manager.close_apk(apk)
#             time.sleep(0.2)
# 
#         logger.info('Exit -- MUAT:DesktopSystemTest:test_UninstallAPP')

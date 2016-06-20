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
class WPSTest(ParametrizedTestCase):
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
        while time.time()-start < constants.Time_Out:
            if not Button1.exists:
                break
            else:
                time.sleep(1)
        closeButton=self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.kingsoft.moffice_pro")
        #self.adb_tools.adb_shell('adb shell am force-stop com.kingsoft.moffice_pro')
        if closeButton.exists:
            closeButton.click()
            time.sleep(1)

    def tearDown(self):
        closeButton=self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.kingsoft.moffice_pro")
        if closeButton.exists:
            closeButton.click()
            time.sleep(1)
            if closeButton.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertFalse(closeButton.exists)
            
        #self.adb_tools.adb_shell('adb shell am force-stop com.kingsoft.moffice_pro')
        time.sleep(1)
#         self.account.sleep()
    
             
    def test_OpenAndExit(self):
        logger.info('Enter -- MUAT:WPSTest:test_OpenAndExit')
        #self.adb_tools.adb_shell('am start -n com.kingsoft.moffice_pro/cn.wps.moffice.documentmanager.DocumentManager')
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        wps=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text='WPS Office')
        click_x = wps.info['visibleBounds']['left'] +5
        click_y = wps.info['visibleBounds']['top'] +5
        self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
#         click_x = WPSIcon.info['visibleBounds']['left'] +5
#         click_y = WPSIcon.info['visibleBounds']['top'] +5
#         self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        WPS_Title=self.d(text='WPS Office',resourceId='android:id/pc_title',packageName='com.kingsoft.moffice_pro')
        start = time.time()
        while time.time() - start < constants.Time_Out:
            if WPS_Title.exists:
                break
            else:
                time.sleep(1)
        if not WPS_Title.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(WPS_Title.exists)
        closeButton=self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.kingsoft.moffice_pro")
        if closeButton.exists:
            closeButton.click()
        logger.info('Exit -- MUAT:WPSTest:test_OpenAndExit')
              
    def test_OpenFile(self):
        logger.info('Enter -- MUAT:WPSTest:test_OpenFile')
        #self.adb_tools.adb_shell('am start -n com.kingsoft.moffice_pro/cn.wps.moffice.documentmanager.DocumentManager')
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        wps=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text='WPS Office')
        if wps.exists:
            click_x = wps.info['visibleBounds']['left'] +5
            click_y = wps.info['visibleBounds']['top'] +5
            self.mouse.click(click_x, click_y, constants.MouseLeftKey)
            WPS_Title=self.d(text='WPS Office',resourceId='android:id/pc_title',packageName='com.kingsoft.moffice_pro')
            start = time.time()
            while time.time() - start < constants.Time_Out:
                if WPS_Title.exists:
                    break
                else:
                    time.sleep(1)
            if not WPS_Title.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(WPS_Title.exists)    
        profile_layout=self.d(resourceId='com.kingsoft.moffice_pro:id/left_nav_profile_layout')
        click_x=profile_layout.info['visibleBounds']['right'] - 10
        click_y=profile_layout.info['visibleBounds']['bottom'] + 10
        self.mouse.click(click_x,click_y,constants.MouseLeftKey)
        #DOC
        doc_file=self.d(text=u'文档' , resourceId='com.kingsoft.moffice_pro:id/text')
        if doc_file.exists:
            doc_file.click()
            start = time.time()
            backButton=self.d(resourceId='com.kingsoft.moffice_pro:id/writer_maintoolbar_backBtn')
            while time.time() - start < constants.Time_Out:
                if backButton.exists:
                    break
                else:
                    time.sleep(1)
            if not self.d(resourceId='com.kingsoft.moffice_pro:id/writer_maintoolbar_logo').exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(self.d(resourceId='com.kingsoft.moffice_pro:id/writer_maintoolbar_logo').exists)
            self.d.press(48)
            self.d.press(62)
            saveIcon=self.d(resourceId='com.kingsoft.moffice_pro:id/image_save')
            if saveIcon.exists:
                saveIcon.click()
                myfile=self.d(text=u'我的文档',resourceId='com.kingsoft.moffice_pro:id/fb_filename_text')
                if myfile.exists:
                    myfile.click()
                    saveButton=self.d(resourceId='com.kingsoft.moffice_pro:id/btn_save')
                    if saveButton.exists:
                        saveButton.click()
                        replaceButton=self.d(resourceId='com.kingsoft.moffice_pro:id/dialog_button_positive')
                        if replaceButton.exists:
                            replaceButton.click()
                        time.sleep(3)
                        if backButton.exists:
                            backButton.click()
                            time.sleep(1)
        #TXT
        txt_file=self.d(text=u'便笺',resourceId='com.kingsoft.moffice_pro:id/text')
        if txt_file.exists:
            txt_file.click()
            start = time.time()
            backButton=self.d(resourceId='com.kingsoft.moffice_pro:id/writer_maintoolbar_backBtn')
            while time.time() - start < constants.Time_Out:
                if backButton.exists:
                    break
                else:
                    time.sleep(1)
            if not self.d(resourceId='com.kingsoft.moffice_pro:id/writer_maintoolbar_logo').exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(self.d(resourceId='com.kingsoft.moffice_pro:id/writer_maintoolbar_logo').exists)
            self.d.press(48)
            self.d.press(62)
            saveIcon=self.d(resourceId='com.kingsoft.moffice_pro:id/image_save')
            if saveIcon.exists:
                saveIcon.click()
                myfile=self.d(text=u'我的文档',resourceId='com.kingsoft.moffice_pro:id/fb_filename_text')
                if myfile.exists:
                    myfile.click()
                    saveButton=self.d(resourceId='com.kingsoft.moffice_pro:id/btn_save')
                    if saveButton.exists:
                        saveButton.click()
                        replaceButton=self.d(resourceId='com.kingsoft.moffice_pro:id/dialog_button_positive')
                        if replaceButton.exists:
                            replaceButton.click()
                            replaceButton.click()
                        time.sleep(3)
                        if backButton.exists:
                            backButton.click()
                            time.sleep(1)
                               
        #XLS
        xls_file=self.d(text=u'表格',resourceId='com.kingsoft.moffice_pro:id/text')
        if xls_file.exists:
            xls_file.click()
            start = time.time()
            backButton=self.d(resourceId='com.kingsoft.moffice_pro:id/ss_titlebar_close')
            while time.time() - start < constants.Time_Out:
                if self.d(resourceId='com.kingsoft.moffice_pro:id/image_save').exists:
                    break
                else:
                    time.sleep(1)
            #time.sleep(1)
            if not self.d(resourceId='com.kingsoft.moffice_pro:id/ss_titlebar_logo').exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(self.d(resourceId='com.kingsoft.moffice_pro:id/ss_titlebar_logo').exists)
            self.d.press(48)
            self.d.press(62)
            self.d.press(66)
            saveIcon=self.d(resourceId='com.kingsoft.moffice_pro:id/image_save')
            if saveIcon.exists:
                saveIcon.click()
                myfile=self.d(text=u'我的文档',resourceId='com.kingsoft.moffice_pro:id/fb_filename_text')
                if myfile.exists:
                    myfile.click()
                    saveButton=self.d(resourceId='com.kingsoft.moffice_pro:id/btn_save')
                    if saveButton.exists:
                        saveButton.click()
                        replaceButton=self.d(resourceId='com.kingsoft.moffice_pro:id/dialog_button_positive')
                        if replaceButton.exists:
                            replaceButton.click()
                            time.sleep(3)
                        backButton=self.d(resourceId='com.kingsoft.moffice_pro:id/ss_titlebar_close')
                        if backButton.exists:
                            backButton.click()
                            time.sleep(1)
        #PPT
#         ppt_file=self.d(text=u'演示',resourceId='com.kingsoft.moffice_pro:id/text')
#         if ppt_file.exists:
#             ppt_file.click()
#             start = time.time()
#             #backButton=self.d(resourceId='com.kingsoft.moffice_pro:id/writer_maintoolbar_backBtn')
#             saveIcon=self.d(resourceId='com.kingsoft.moffice_pro:id/image_save')
#             while time.time() - start < constants.Time_Out:
#                 if saveIcon.exists:
#                     break
#                 else:
#                     time.sleep(1)
#             #self.d.press(48)
#             wps_content = self.d(resourceId='com.kingsoft.moffice_pro:id/content')
#             write_x = wps_content.info['visibleBounds']['left']+700
#             write_y = wps_content.info['visibleBounds']['top']+300
#             self.mouse.doubleclick(write_x,write_y,constants.MouseLeftKey)
#             self.d.press(48)
#             self.d.press(62)
#             #saveIcon=self.d(resourceId='com.kingsoft.moffice_pro:id/image_save')
#             if saveIcon.exists:
#                 saveIcon.click()
#                 myfile=self.d(text=u'我的文档',resourceId='com.kingsoft.moffice_pro:id/fb_filename_text')
#                 if myfile.exists:
#                     myfile.click()
#                     saveButton=self.d(resourceId='com.kingsoft.moffice_pro:id/btn_save')
#                     if saveButton.exists:
#                         saveButton.click()
#                         replaceButton=self.d(resourceId='com.kingsoft.moffice_pro:id/dialog_button_positive')
#                         if replaceButton.exists:
#                             replaceButton.click()
#                             time.sleep(3)
#                             self.d(resourceId='com.kingsoft.moffice_pro:id/ppt_titlebar_close').click()
#                         backButton=self.d(resourceId='com.kingsoft.moffice_pro:id/ss_titlebar_close')
#                         if backButton.exists:
#                             backButton.click()
        
        closeButton=self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.kingsoft.moffice_pro")
        if closeButton.exists:
            closeButton.click()
        logger.info('Exit -- MUAT:WPSTest:test_OpenFile')
             
    def test_RecentFile(self):
        logger.info('Enter -- MUAT:WPSTest:test_RecentFile')
        #self.adb_tools.adb_shell('am start -n com.kingsoft.moffice_pro/cn.wps.moffice.documentmanager.DocumentManager')
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        wps=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text='WPS Office')
        click_x = wps.info['visibleBounds']['left'] +5
        click_y = wps.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
#         click_x = WPSIcon.info['visibleBounds']['left'] +5
#         click_y = WPSIcon.info['visibleBounds']['top'] +5
#         self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        WPS_Title=self.d(text='WPS Office',resourceId='android:id/pc_title',packageName='com.kingsoft.moffice_pro')
        start = time.time()
        while time.time() - start < constants.Time_Out:
            if WPS_Title.exists:
                break
            else:
                time.sleep(1)
        if not WPS_Title.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(WPS_Title.exists)
        profile_layout=self.d(resourceId='com.kingsoft.moffice_pro:id/left_nav_profile_layout')
        click_x=profile_layout.info['visibleBounds']['right'] - 10
        click_y=profile_layout.info['visibleBounds']['bottom'] + 58
        self.mouse.click(click_x,click_y,constants.MouseLeftKey)
        history_icon=self.d(resourceId='com.kingsoft.moffice_pro:id/history_record_item_icon')
        if not history_icon.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(history_icon.exists)
           
        closeButton=self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.kingsoft.moffice_pro")
        if closeButton.exists:
            closeButton.click()
        logger.info('Exit -- MUAT:WPSTest:test_RecentFile')
          
    def test_BackHome(self):
        logger.info('Enter -- MUAT:WPSTest:test_BackHome')
        #self.adb_tools.adb_shell('am start -n com.kingsoft.moffice_pro/cn.wps.moffice.documentmanager.DocumentManager')
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        wps=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text='WPS Office')
        click_x = wps.info['visibleBounds']['left'] +5
        click_y = wps.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        
#         click_x = WPSIcon.info['visibleBounds']['left'] +5
#         click_y = WPSIcon.info['visibleBounds']['top'] +5
#         self.mouse.doubleclick(click_x, click_y, constants.MouseLeftKey)
        WPS_Title=self.d(text='WPS Office',resourceId='android:id/pc_title',packageName='com.kingsoft.moffice_pro')
        start = time.time()
        while time.time() - start < constants.Time_Out:
            if WPS_Title.exists:
                break
            else:
                time.sleep(1)
        if not WPS_Title.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(WPS_Title.exists)
        profile_layout=self.d(resourceId='com.kingsoft.moffice_pro:id/left_nav_profile_layout')
        click_x=profile_layout.info['visibleBounds']['right'] - 10
        click_y=profile_layout.info['visibleBounds']['bottom'] + 10
        self.mouse.click(click_x,click_y,constants.MouseLeftKey)
        #DOC
        doc_file=self.d(text=u'文档' , resourceId='com.kingsoft.moffice_pro:id/text')
        if doc_file.exists:
            doc_file.click()
            start = time.time()
            backButton=self.d(resourceId='com.kingsoft.moffice_pro:id/writer_maintoolbar_backBtn')
            while time.time() - start < constants.Time_Out:
                if backButton.exists:
                    break
                else:
                    time.sleep(1)
            WLogo=self.d(resourceId='com.kingsoft.moffice_pro:id/writer_maintoolbar_logo',packageName='com.kingsoft.moffice_pro')
            if WLogo.exists:
                WLogo.click()
                time.sleep(1)
            if not self.d(text=u'新建',resourceId='com.kingsoft.moffice_pro:id/nav_item_title').exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(self.d(text=u'新建',resourceId='com.kingsoft.moffice_pro:id/nav_item_title').exists)
            self.assertTrue(self.d(text=u'最近',resourceId='com.kingsoft.moffice_pro:id/nav_item_title').exists)
            self.assertTrue(self.d(text=u'星标',resourceId='com.kingsoft.moffice_pro:id/nav_item_title').exists)
            self.d(resourceId='android:id/pc_max').click()
            self.d.click(960,540)
            time.sleep(2)
            backButton=self.d(resourceId='com.kingsoft.moffice_pro:id/writer_maintoolbar_backBtn')
            if backButton.exists:
                backButton.click()
              
        closeButton=self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.kingsoft.moffice_pro")
        if closeButton.exists:
            closeButton.click()
        logger.info('Exit -- MUAT:WPSTest:test_BackHome')
            
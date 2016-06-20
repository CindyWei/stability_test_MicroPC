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

class PaintTest(ParametrizedTestCase):
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
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.paint.board")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
            self.adb_tools.adb_shell('am force-stop com.paint.board')
        
    def tearDown(self):
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.paint.board")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
            time.sleep(1)
        if closeButton.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
            self.adb_tools.adb_shell('am force-stop com.paint.board')
            self.assertFalse(closeButton.exists)
        if os.path.exists(self.TmpImagePath):
            shutil.rmtree(self.TmpImagePath)
        self.account.sleep()
            
    def test_OpenAndExit(self):
        logger.info('Enter -- MUAT:PaintTest:test_OpenAndExit')
        # click the applist
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        paint=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text=u'画图')
        click_x = paint.info['visibleBounds']['left'] +5
        click_y = paint.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        time.sleep(2)
        PaintWindow = self.d(className="android.widget.FrameLayout", packageName="com.paint.board")
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if  PaintWindow.exists:
                break
            else:
                time.sleep(1)
        if not PaintWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(PaintWindow.exists)
        if PaintWindow.exists:
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.paint.board")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:PaintTest:test_OpenAndExit')
         
    def test_OpenPic(self):
        logger.info('Enter -- MUAT:PaintTest:test_OpenPic')
        # click the applist
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        paint=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text=u'画图')
        click_x = paint.info['visibleBounds']['left'] +5
        click_y = paint.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        time.sleep(2)
        PaintWindow=self.d(resourceId='android:id/pc_title',packageName='com.paint.board')
        if not PaintWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertTrue(PaintWindow.exists)
        #max window
        self.d(resourceId='android:id/pc_max',packageName='com.paint.board').click()
        fileButton=self.d(resourceId='com.paint.board:id/b_file',text=u'文件')
        editButton=self.d(resourceId='com.paint.board:id/b_edit',text=u'编辑')
        if fileButton.exists:
            #open jpg
            fileButton.click()
            click_x = editButton.info['visibleBounds']['left']
            click_y = editButton.info['visibleBounds']['bottom'] +40
            self.d.click(click_x,click_y)
            time.sleep(1)
            customer=self.d(resourceId='android:id/custom',className='android.widget.FrameLayout')
            self.d.drag(customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['bottom']-170,customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['top']+10,10)
            self.d.drag(customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['bottom']-170,customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['top']+10,10)
            fileName=self.d(resourceId='com.paint.board:id/filedialogitem_name',text='jpg.jpg')
            self.assertTrue(fileName.exists)
            file_x=fileName.info['visibleBounds']['left']+5
            file_y=fileName.info['visibleBounds']['top']+5
            self.d.click(file_x,file_y)
            #self.mouse.doubleclick(file_x, file_y, constants.MouseLeftKey)
            time.sleep(1)
            #self.d(resourceId='com.paint.board:id/filedialogitem_img',packageName='com.paint.board').click()
            self.d(text=u'打开',resourceId='com.paint.board:id/dia_postive').click()
            time.sleep(1)
            self.assertTrue(self.d(resourceId='com.paint.board:id/t_tab',text='jpg.jpg').exists)
            #open png
            fileButton.click()
            click_x = editButton.info['visibleBounds']['left']
            click_y = editButton.info['visibleBounds']['bottom'] +40
            self.d.click(click_x,click_y)
            time.sleep(1)
            customer=self.d(resourceId='android:id/custom',className='android.widget.FrameLayout')
            self.d.drag(customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['bottom']-170,customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['top']+10,20)
            self.d.drag(customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['bottom']-170,customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['top']+10,20)
            fileName=self.d(resourceId='com.paint.board:id/filedialogitem_name',text='png.png')
            self.assertTrue(fileName.exists)
            file_x=fileName.info['visibleBounds']['left']+5
            file_y=fileName.info['visibleBounds']['top']+5
            self.d.click(file_x,file_y)
            time.sleep(1)
            self.d(text=u'打开',resourceId='com.paint.board:id/dia_postive').click()
            time.sleep(1)
            self.assertTrue(self.d(resourceId='com.paint.board:id/t_tab',text='png.png').exists)
            
        if PaintWindow.exists:
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.paint.board")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:PaintTest:test_OpenPic')
 
    def test_NewFile(self):
        logger.info('Enter -- MUAT:PaintTest:test_NewFile')
        # click the applist
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        paint=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text=u'画图')
        click_x = paint.info['visibleBounds']['left'] +5
        click_y = paint.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        time.sleep(2)
        PaintWindow=self.d(resourceId='android:id/pc_title',packageName='com.paint.board')
        if not PaintWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertTrue(PaintWindow.exists)
        fileButton=self.d(resourceId='com.paint.board:id/b_file',text=u'文件')
        editButton=self.d(resourceId='com.paint.board:id/b_edit',text=u'编辑')
        if fileButton.exists:
            fileButton.click()
            click_x = editButton.info['visibleBounds']['left']
            click_y = editButton.info['visibleBounds']['bottom'] +10
            self.d.click(click_x,click_y)
            time.sleep(1)
            self.assertTrue(self.d(resourceId='com.paint.board:id/paint_view').exists)
        if PaintWindow.exists:
            closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.paint.board")
            if closeButton.exists:
                logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
                closeButton.click()
        logger.info('Exit -- MUAT:PaintTest:test_NewFile')
         
    def test_CloseFile(self):
        logger.info('Enter -- MUAT:PaintTest:test_CloseFile')
        # click the applist
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        paint=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text=u'画图')
        click_x = paint.info['visibleBounds']['left'] +5
        click_y = paint.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        time.sleep(2)
        PaintWindow=self.d(resourceId='android:id/pc_title',packageName='com.paint.board')
        if not PaintWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertTrue(PaintWindow.exists)
        fileButton=self.d(resourceId='com.paint.board:id/b_file',text=u'文件')
        editButton=self.d(resourceId='com.paint.board:id/b_edit',text=u'编辑')
        if fileButton.exists:
            fileButton.click()
            click_x = editButton.info['visibleBounds']['left']
            click_y = editButton.info['visibleBounds']['bottom'] +10
            self.d.click(click_x,click_y)
            time.sleep(1)
            self.assertTrue(self.d(resourceId='com.paint.board:id/paint_view').exists)
            paint_board=self.d(resourceId='com.paint.board:id/paint_view')
            swipe_start_x=paint_board.info['visibleBounds']['left']+50
            swipe_start_y=paint_board.info['visibleBounds']['top']+50
            swipe_end_x=swipe_start_x + 200
            swipe_end_y=swipe_start_y + 200
            self.d.swipe(swipe_start_x,swipe_start_y,swipe_end_x,swipe_end_y,10)
            closeButton=self.d(resourceId='com.paint.board:id/b_tab')
            if closeButton.exists:
                closeButton.click()
                time.sleep(2)
                self.assertTrue(self.d(resourceId='android:id/message',text=u'是否保存？').exists)
                self.d(resourceId='android:id/button2',text=u'是').click()
                time.sleep(1)
                saveButton=self.d(resourceId='com.paint.board:id/dia_postive')
                if saveButton.exists:
                    saveButton.click()
                    time.sleep(1)
                    ok=self.d(resourceId='android:id/button1',text=u'确认')
                    if ok.exists:
                        ok.click()
                        time.sleep(1)
                        self.assertFalse(self.d(resourceId='com.paint.board:id/paint_view').exists)
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.paint.board")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
        logger.info('Exit -- MUAT:PaintTest:test_CloseFile')
              
    def test_SaveFile(self):
        logger.info('Enter -- MUAT:PaintTest:test_SaveFile')
        # click the applist
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        paint=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text=u'画图')
        click_x = paint.info['visibleBounds']['left'] +5
        click_y = paint.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        time.sleep(2)
        PaintWindow=self.d(resourceId='android:id/pc_title',packageName='com.paint.board')
        if not PaintWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertTrue(PaintWindow.exists)
        fileButton=self.d(resourceId='com.paint.board:id/b_file',text=u'文件')
        editButton=self.d(resourceId='com.paint.board:id/b_edit',text=u'编辑')
        if fileButton.exists:
            fileButton.click()
            time.sleep(1)
            click_new_x = fileButton.info['visibleBounds']['right']
            click_new_y = fileButton.info['visibleBounds']['bottom'] +10
            self.d.click(click_new_x, click_new_y)
            time.sleep(2)
            self.assertTrue(self.d(resourceId='com.paint.board:id/paint_view').exists)
            paint_board=self.d(resourceId='com.paint.board:id/paint_view')
            swipe_start_x=paint_board.info['visibleBounds']['left']+50
            swipe_start_y=paint_board.info['visibleBounds']['top']+50
            swipe_end_x=swipe_start_x + 200
            swipe_end_y=swipe_start_y + 300
            self.d.swipe(swipe_start_x,swipe_start_y,swipe_end_x,swipe_end_y,10)
            time.sleep(1)
            fileButton.click()
            time.sleep(1)
            click_save_x = fileButton.info['visibleBounds']['right']
            click_save_y = fileButton.info['visibleBounds']['bottom'] +60
            self.d.click(click_save_x,click_save_y)
            time.sleep(1)
            saveButton=self.d(resourceId='com.paint.board:id/dia_postive')
            if saveButton.exists:
                saveButton.click()
                time.sleep(1)
                ok=self.d(resourceId='android:id/button1',text=u'确认')
                if ok.exists:
                    ok.click()
                    time.sleep(1)
            closeButton=self.d(resourceId='com.paint.board:id/b_tab')
            if closeButton.exists:
                closeButton.click()
                time.sleep(2)
                self.assertFalse(self.d(resourceId='android:id/message',text=u'是否保存？').exists)
                self.assertFalse(self.d(resourceId='com.paint.board:id/paint_view').exists)
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.paint.board")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
        logger.info('Exit -- MUAT:PaintTest:test_SaveFile')
         
    def test_CopyPic(self):
        logger.info('Enter -- MUAT:PaintTest:test_CopyPic')
        # click the applist
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        paint=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text=u'画图')
        click_x = paint.info['visibleBounds']['left'] +5
        click_y = paint.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        time.sleep(2)
        PaintWindow=self.d(resourceId='android:id/pc_title',packageName='com.paint.board')
        if not PaintWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertTrue(PaintWindow.exists)
        self.assertTrue(self.d.press(0x8d))
        time.sleep(1)
        fileButton=self.d(resourceId='com.paint.board:id/b_file',text=u'文件')
        editButton=self.d(resourceId='com.paint.board:id/b_edit',text=u'编辑')
        if fileButton.exists:
            fileButton.click()
            click_open_x = fileButton.info['visibleBounds']['right']
            click_open_y = fileButton.info['visibleBounds']['bottom'] +35
            self.d.click(click_open_x,click_open_y)
            time.sleep(1)
            customer=self.d(resourceId='android:id/custom',className='android.widget.FrameLayout')
            self.d.drag(customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['bottom']-170,customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['top']+10,10)
            self.d.drag(customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['bottom']-170,customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['top']+10,10)
            fileName=self.d(resourceId='com.paint.board:id/filedialogitem_name',text='jpg.jpg')
            self.assertTrue(fileName.exists)
            file_x=fileName.info['visibleBounds']['left']+5
            file_y=fileName.info['visibleBounds']['top']+5
            self.d.click(file_x,file_y)
            #self.mouse.doubleclick(file_x, file_y, constants.MouseLeftKey)
            time.sleep(1)
            #self.d(resourceId='com.paint.board:id/filedialogitem_img',packageName='com.paint.board').click()
            self.d(text=u'打开',resourceId='com.paint.board:id/dia_postive').click()
            time.sleep(1)
            self.assertTrue(self.d(resourceId='com.paint.board:id/t_tab',text='jpg.jpg').exists)
            self.assertTrue(self.d(resourceId='com.paint.board:id/paint_view').exists)
            paint_board=self.d(resourceId='com.paint.board:id/paint_view')
            choose_button=self.d(resourceId='com.paint.board:id/b_choose',packageName='com.paint.board')
            choose_button.click()
            self.d.click(choose_button.info['visibleBounds']['right'],choose_button.info['visibleBounds']['bottom']+10)
            time.sleep(1)
#             swipe_start_x=paint_board.info['visibleBounds']['left']+50
#             swipe_start_y=paint_board.info['visibleBounds']['top']+50
#             swipe_end_x=swipe_start_x + 200
#             swipe_end_y=swipe_start_y + 200
            self.d.swipe(500,500,750,750,10)
            time.sleep(1)
            editButton.click()
            self.d.click(editButton.info['visibleBounds']['right'],editButton.info['visibleBounds']['bottom']+40)
            fileButton.click()
            time.sleep(1)
            self.d.click(fileButton.info['visibleBounds']['right'],fileButton.info['visibleBounds']['bottom']+10)
            editButton.click()
            time.sleep(1)
            self.d.click(editButton.info['visibleBounds']['right'],editButton.info['visibleBounds']['bottom']+60)
            time.sleep(1)
            BaseImg = os.path.join(self.BaseImagePath, "test_CopyPic.jpg")
            name = "test_CopyPic_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
            img = os.path.join(self.TmpImagePath, name)
            self.d.screenshot(img)
            cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
            CropImage(img, cropedImgPath, 360,147,1560,1047)
            #比较上一步裁剪后的图片与基准图片
            if not CompareImage(cropedImgPath, BaseImg, 0.5):
                shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
                path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
                self.fail("The failure file path is %s" % path)
            self.assertTrue(self.d.press(0x8d))
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.paint.board")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
        logger.info('Exit -- MUAT:PaintTest:test_CopyPic')
         
    def test_CutPic(self):
        logger.info('Enter -- MUAT:PaintTest:test_CutPic')
        # click the applist
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        paint=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text=u'画图')
        click_x = paint.info['visibleBounds']['left'] +5
        click_y = paint.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        time.sleep(2)
        PaintWindow=self.d(resourceId='android:id/pc_title',packageName='com.paint.board')
        if not PaintWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertTrue(PaintWindow.exists)
        self.assertTrue(self.d.press(0x8d))
        time.sleep(1)
        fileButton=self.d(resourceId='com.paint.board:id/b_file',text=u'文件')
        editButton=self.d(resourceId='com.paint.board:id/b_edit',text=u'编辑')
        if fileButton.exists:
            fileButton.click()
            click_new_x = fileButton.info['visibleBounds']['right']
            click_new_y = fileButton.info['visibleBounds']['bottom'] +35
            self.d.click(click_new_x,click_new_y)
            time.sleep(1)
            customer=self.d(resourceId='android:id/custom',className='android.widget.FrameLayout')
            self.d.drag(customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['bottom']-170,customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['top']+10,10)
            self.d.drag(customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['bottom']-170,customer.info['visibleBounds']['right']-100,customer.info['visibleBounds']['top']+10,10)
            fileName=self.d(resourceId='com.paint.board:id/filedialogitem_name',text='jpg.jpg')
            self.assertTrue(fileName.exists)
            file_x=fileName.info['visibleBounds']['left']+5
            file_y=fileName.info['visibleBounds']['top']+5
            self.d.click(file_x,file_y)
            #self.mouse.doubleclick(file_x, file_y, constants.MouseLeftKey)
            time.sleep(1)
            #self.d(resourceId='com.paint.board:id/filedialogitem_img',packageName='com.paint.board').click()
            self.d(text=u'打开',resourceId='com.paint.board:id/dia_postive').click()
            time.sleep(1)
            self.assertTrue(self.d(resourceId='com.paint.board:id/t_tab',text='jpg.jpg').exists)
            self.assertTrue(self.d(resourceId='com.paint.board:id/paint_view').exists)
            paint_board=self.d(resourceId='com.paint.board:id/paint_view')
            choose_button=self.d(resourceId='com.paint.board:id/b_choose',packageName='com.paint.board')
            choose_button.click()
            self.d.click(choose_button.info['visibleBounds']['right'],choose_button.info['visibleBounds']['bottom']+10)
            time.sleep(1)
#             swipe_start_x=paint_board.info['visibleBounds']['left']+50
#             swipe_start_y=paint_board.info['visibleBounds']['top']+50
#             swipe_end_x=swipe_start_x + 200
#             swipe_end_y=swipe_start_y + 200
            self.d.swipe(500,500,750,750,10)
            time.sleep(1)
            editButton.click()
            self.d.click(editButton.info['visibleBounds']['right'],editButton.info['visibleBounds']['bottom']+10)
            time.sleep(1)
            BaseImg = os.path.join(self.BaseImagePath, "test_CutPic.jpg")
            name = "test_CutPic_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
            img = os.path.join(self.TmpImagePath, name)
            self.d.screenshot(img)
            cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
            CropImage(img, cropedImgPath, 360,147,1560,1047)
            #比较上一步裁剪后的图片与基准图片
            if not CompareImage(cropedImgPath, BaseImg, 0.5):
                shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
                path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
                self.fail("The failure file path is %s" % path)
            self.assertTrue(self.d.press(0x8d))
                 
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.paint.board")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
        logger.info('Exit -- MUAT:PaintTest:test_CutPic')
        
    def test_Pen(self):
        logger.info('Enter -- MUAT:PaintTest:test_Pen')
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        paint=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text=u'画图')
        click_x = paint.info['visibleBounds']['left'] +5
        click_y = paint.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        time.sleep(2)
        PaintWindow=self.d(resourceId='android:id/pc_title',packageName='com.paint.board')
        if not PaintWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertTrue(PaintWindow.exists)
        fileButton=self.d(resourceId='com.paint.board:id/b_file',text=u'文件')
        editButton=self.d(resourceId='com.paint.board:id/b_edit',text=u'编辑')
        if fileButton.exists:
            fileButton.click()
            click_new_x = editButton.info['visibleBounds']['left']
            click_new_y = editButton.info['visibleBounds']['bottom'] +10
            self.d.click(click_new_x,click_new_y)
            #time.sleep(1)
            self.assertTrue(self.d(resourceId='com.paint.board:id/paint_view').exists)
            pencil=self.d(resourceId='com.paint.board:id/b_status',packageName='com.paint.board')
            pencil.click()
            time.sleep(1)
            #choose pencil
            choose_pencil_x=pencil.info['visibleBounds']['right']
            choose_pencil_y=pencil.info['visibleBounds']['bottom']+74
            self.d.click(choose_pencil_x,choose_pencil_y)
            time.sleep(1)
            paint_board=self.d(resourceId='com.paint.board:id/paint_view')
            swipe_start_x=paint_board.info['visibleBounds']['left']+50
            swipe_start_y=paint_board.info['visibleBounds']['top']+50
            swipe_end_x=swipe_start_x + 200
            swipe_end_y=swipe_start_y + 200
            self.d.swipe(swipe_start_x,swipe_start_y,swipe_end_x,swipe_end_y,20)
            time.sleep(0.5)
            #compare cutpic with baseimage
            BaseImg = os.path.join(self.BaseImagePath, "test_Pencil.jpg")
            name = "test_Pencil_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
            img = os.path.join(self.TmpImagePath, name)
            self.d.screenshot(img)
            cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
            CropImage(img, cropedImgPath, paint_board.info['visibleBounds']['left'],paint_board.info['visibleBounds']['top'],paint_board.info['visibleBounds']['right'],paint_board.info['visibleBounds']['bottom'])
            if not CompareImage(cropedImgPath, BaseImg, 0.9):
                shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
                path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
                self.fail("The failure file path is %s" % path)
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.paint.board")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
        logger.info('Exit -- MUAT:PaintTest:test_Pen')
        
    def test_FullScreen(self):
        logger.info('Enter -- MUAT:PaintTest:test_FullScreen')
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        paint=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text=u'画图')
        click_x = paint.info['visibleBounds']['left'] +5
        click_y = paint.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        time.sleep(2)
        PaintWindow=self.d(resourceId='android:id/pc_title',packageName='com.paint.board')
        if not PaintWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertTrue(PaintWindow.exists)
        self.assertTrue(self.d.press(0x8d))
        fileButton=self.d(resourceId='com.paint.board:id/b_file',text=u'文件')
        editButton=self.d(resourceId='com.paint.board:id/b_edit',text=u'编辑')
        if fileButton.exists:
            fileButton.click()
            click_new_x = editButton.info['visibleBounds']['left']
            click_new_y = editButton.info['visibleBounds']['bottom'] +10
            self.d.click(click_new_x,click_new_y)
            #time.sleep(1)
            self.assertTrue(self.d(resourceId='com.paint.board:id/paint_view').exists)
        self.assertTrue(self.d.press(0x8d))
        self.assertTrue(PaintWindow.exists)
        
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.paint.board")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
        logger.info('Exit -- MUAT:PaintTest:test_FullScreen')
        
    def test_InsertText(self):
        logger.info('Enter -- MUAT:PaintTest:test_InsertText')
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        paint=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text=u'画图')
        click_x = paint.info['visibleBounds']['left'] +5
        click_y = paint.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        time.sleep(2)
        PaintWindow=self.d(resourceId='android:id/pc_title',packageName='com.paint.board')
        if not PaintWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertTrue(PaintWindow.exists)
        fileButton=self.d(resourceId='com.paint.board:id/b_file',text=u'文件')
        editButton=self.d(resourceId='com.paint.board:id/b_edit',text=u'编辑')
        if fileButton.exists:
            fileButton.click()
            click_new_x = editButton.info['visibleBounds']['left']
            click_new_y = editButton.info['visibleBounds']['bottom'] +10
            self.d.click(click_new_x,click_new_y)
            #time.sleep(1)
            self.assertTrue(self.d(resourceId='com.paint.board:id/paint_view').exists)
            self.d(resourceId='com.paint.board:id/b_7',packageName='com.paint.board').click()
            paint_board=self.d(resourceId='com.paint.board:id/paint_view')
            drag_start_x=paint_board.info['visibleBounds']['left']+50
            drag_start_y=paint_board.info['visibleBounds']['top']+50
            drag_end_x=drag_start_x + 200
            drag_end_y=drag_start_y + 200
            self.d.drag(drag_start_x,drag_start_y,drag_end_x,drag_end_y,20)
            time.sleep(0.5)
            self.d.click(drag_start_x + 5,drag_start_y + 5)
            time.sleep(1)
            self.d.press(48)
            self.d.press(48)
            self.d.press(62)
            self.d.click(drag_end_x,drag_end_y)
            time.sleep(1)
            #compare cutpic with baseimage
            BaseImg = os.path.join(self.BaseImagePath, "test_Paint_Text.jpg")
            name = "test_Paint_Text_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
            img = os.path.join(self.TmpImagePath, name)
            self.d.screenshot(img)
            cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
            CropImage(img, cropedImgPath, paint_board.info['visibleBounds']['left'],paint_board.info['visibleBounds']['top'],paint_board.info['visibleBounds']['right'],paint_board.info['visibleBounds']['bottom'])
            if not CompareImage(cropedImgPath, BaseImg, 0.9):
                shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
                path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
                self.fail("The failure file path is %s" % path)
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.paint.board")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
            logger.info('Exit -- MUAT:PaintTest:test_InsertText')
            
    def test_DrawCircle(self):
        logger.info('Enter -- MUAT:PaintTest:test_DrawCircle')
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        paint=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text=u'画图')
        click_x = paint.info['visibleBounds']['left'] +5
        click_y = paint.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        time.sleep(2)
        PaintWindow=self.d(resourceId='android:id/pc_title',packageName='com.paint.board')
        if not PaintWindow.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
        self.assertTrue(PaintWindow.exists)
        fileButton=self.d(resourceId='com.paint.board:id/b_file',text=u'文件')
        editButton=self.d(resourceId='com.paint.board:id/b_edit',text=u'编辑')
        if fileButton.exists:
            fileButton.click()
            click_new_x = editButton.info['visibleBounds']['left']
            click_new_y = editButton.info['visibleBounds']['bottom'] +10
            self.d.click(click_new_x,click_new_y)
            #time.sleep(1)
            self.assertTrue(self.d(resourceId='com.paint.board:id/paint_view').exists)
            circle_button=self.d(resourceId='com.paint.board:id/b_shape',packageName='com.paint.board')
            circle_button.click()
            self.d.click(circle_button.info['visibleBounds']['right']+10,circle_button.info['visibleBounds']['bottom']+10)
            time.sleep(0.5)
            paint_board=self.d(resourceId='com.paint.board:id/paint_view')
            swipe_start_x=paint_board.info['visibleBounds']['left']+50
            swipe_start_y=paint_board.info['visibleBounds']['top']+50
            swipe_end_x=swipe_start_x + 200
            swipe_end_y=swipe_start_y + 200
            self.d.swipe(swipe_start_x,swipe_start_y,swipe_end_x,swipe_end_y,20)
            time.sleep(0.5)
            #compare cutpic with baseimage
            BaseImg = os.path.join(self.BaseImagePath, "test_Circle.jpg")
            name = "test_Circle_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
            img = os.path.join(self.TmpImagePath, name)
            self.d.screenshot(img)
            cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
            CropImage(img, cropedImgPath, paint_board.info['visibleBounds']['left'],paint_board.info['visibleBounds']['top'],paint_board.info['visibleBounds']['right'],paint_board.info['visibleBounds']['bottom'])
            if not CompareImage(cropedImgPath, BaseImg, 0.9):
                shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
                path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
                self.fail("The failure file path is %s" % path)
        
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.paint.board")
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
            logger.info('Exit -- MUAT:PaintTest:test_DrawCircle')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
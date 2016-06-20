#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015年11月5日

@author: liudongjie
'''
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

class InputTest(ParametrizedTestCase):
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

        Button1=self.d(resourceId='com.yunpc.yunosloginui:id/avatar')
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if not Button1.exists:
                break
            else:
                time.sleep(1)
        self.adb_tools.adb_shell('am force-stop com.yunpc.note')  
        
    def tearDown(self):
        self.adb_tools.adb_shell('am force-stop com.yunpc.note')    
        if os.path.exists(self.TmpImagePath):
            shutil.rmtree(self.TmpImagePath)
        self.mouse.click(1724, 10, constants.MouseLeftKey)
#         time.sleep(1)
        self.mouse.click(1744, 100, constants.MouseLeftKey)
        

    def test_PressNum(self):
        logger.info('Enter -- MUAT:InputTest:test_PressNumTest')
        self.adb_tools.adb_shell('am start -n com.yunpc.note/.app.ui.activity.MainActivityNew')
        time.sleep(2)
        self.d(resourceId='android:id/pc_max',packageName='com.yunpc.note').click()
        edit_text=self.d(resourceId='com.yunpc.note:id/et',packageName='com.yunpc.note')
        self.assertTrue(edit_text.exists)
        self.mouse.click(1724, 10, constants.MouseLeftKey)
        time.sleep(1)
        self.mouse.click(1744, 45, constants.MouseLeftKey)
        time.sleep(5)
#         self.d.press(59)
#         time.sleep(3)
        self.d.press(43)
        self.d.press(43)
        time.sleep(0.5)
        self.d.press(8)
        time.sleep(1)
        BaseImg = os.path.join(self.BaseImagePath, "test_note_sgn.jpg")
        name = "test_note_sgn_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
        img = os.path.join(self.TmpImagePath, name)
        self.d.screenshot(img)
        cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
        CropImage(img, cropedImgPath, 0, 0, 1759, 200)
        if not CompareImage(cropedImgPath, BaseImg, 0.9):
            shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
            self.adb_tools.adb_shell('am force-stop com.yunpc.note')  
            self.adb_tools.adb_shell('am start -n com.yunpc.note/.app.ui.activity.MainActivityNew')
            time.sleep(2)
            self.d(resourceId='android:id/pc_max',packageName='com.yunpc.note').click()
            edit_text=self.d(resourceId='com.yunpc.note:id/et',packageName='com.yunpc.note')
            self.assertTrue(edit_text.exists)
            self.d.press(59)
            time.sleep(2)
            self.d.press(43)
            self.d.press(43)
            time.sleep(0.5)
            self.d.press(8)
            self.d.screenshot(img)
            time.sleep(1)
            cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
            CropImage(img, cropedImgPath, 0, 0, 1759, 200)
            if not CompareImage(cropedImgPath, BaseImg, 0.9):
                shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
                path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
                self.fail("The failure file path is %s") % path
        CloseButton=self.d(resourceId='android:id/pc_close',packageName='com.yunpc.note')
        if CloseButton.exists:
            CloseButton.click()
            self.d(resourceId='android:id/button3',packageName='com.yunpc.note').click()
        time.sleep(1)
        logger.info("Exit -- MUAT:InputTest:test_PressNumTest")
              
    def test_PressSpace(self):
        logger.info('Enter -- MUAT:InputTest:test_PressSpaceTest')
        self.adb_tools.adb_shell('am start -n com.yunpc.note/.app.ui.activity.MainActivityNew')
        time.sleep(2)
        self.d(resourceId='android:id/pc_max',packageName='com.yunpc.note').click()
        edit_text=self.d(resourceId='com.yunpc.note:id/et',packageName='com.yunpc.note')
        self.assertTrue(edit_text.exists)
        self.mouse.click(1724, 10, constants.MouseLeftKey)
        time.sleep(1)
        self.mouse.click(1744, 45, constants.MouseLeftKey)  
        time.sleep(5)
#         self.d.press(59)
#         time.sleep(3)       
        self.d.press(42)
        self.d.press(37)
        self.d.press(42)
        self.d.press(37)
        time.sleep(0.5)
        self.d.press(62)
        time.sleep(1)
        BaseImg = os.path.join(self.BaseImagePath, "test_note_sgs.jpg")
        name = "test_note_sgs%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
        img = os.path.join(self.TmpImagePath, name)
        self.d.screenshot(img)
        cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
        CropImage(img, cropedImgPath,  0, 0, 1759, 200)
        if not CompareImage(cropedImgPath, BaseImg, 0.9):
            shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
            self.adb_tools.adb_shell('am force-stop com.yunpc.note')  
            self.adb_tools.adb_shell('am start -n com.yunpc.note/.app.ui.activity.MainActivityNew')
            time.sleep(2)
            self.d(resourceId='android:id/pc_max',packageName='com.yunpc.note').click()
            edit_text=self.d(resourceId='com.yunpc.note:id/et',packageName='com.yunpc.note')
            self.assertTrue(edit_text.exists)
            self.d.press(59)
            time.sleep(2)
            self.d.press(42)
            self.d.press(37)
            self.d.press(42)
            self.d.press(37)
            time.sleep(0.5)
            self.d.press(62)
            time.sleep(1)
            self.d.screenshot(img)
            cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
            CropImage(img, cropedImgPath, 0, 0, 1759, 200)
            if not CompareImage(cropedImgPath, BaseImg, 0.9):
                shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
                path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
                self.fail("The failure file path is %s") % path
        CloseButton=self.d(resourceId='android:id/pc_close',packageName='com.yunpc.note')
        if CloseButton.exists:
            CloseButton.click()
            time.sleep(1)
            self.d(resourceId='android:id/button3',packageName='com.yunpc.note').click()
        time.sleep(1)
        logger.info("Exit -- MUAT:InputTest:test_PressSpaceTest")
        
    def test_ConvertTest(self):
        logger.info('Enter -- MUAT:InputTest:test_ConvertTest')
        self.adb_tools.adb_shell('am start -n com.yunpc.note/.app.ui.activity.MainActivityNew')
        time.sleep(2)
        self.d(resourceId='android:id/pc_max',packageName='com.yunpc.note').click()
        edit_text=self.d(resourceId='com.yunpc.note:id/et',packageName='com.yunpc.note')
        self.assertTrue(edit_text.exists)
        self.mouse.click(1724, 10, constants.MouseLeftKey)
        time.sleep(1)
        self.mouse.click(1744, 45, constants.MouseLeftKey)
        time.sleep(5)
        self.d.press(42)
        self.d.press(37)
        self.d.press(42)
        self.d.press(37)
        time.sleep(0.5)
        self.d.press(62)
        BaseImg = os.path.join(self.BaseImagePath, "test_note_sgc.jpg")
        name = "test_note_sgc_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
        img = os.path.join(self.TmpImagePath, name)
        self.d.screenshot(img)
        cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
        CropImage(img, cropedImgPath, 0, 0, 1759, 200)
        if not CompareImage(cropedImgPath, BaseImg, 0.9):
            shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
            self.adb_tools.adb_shell('am force-stop com.yunpc.note')  
            self.adb_tools.adb_shell('am start -n com.yunpc.note/.app.ui.activity.MainActivityNew')
            time.sleep(2)
            self.d(resourceId='android:id/pc_max',packageName='com.yunpc.note').click()
            edit_text=self.d(resourceId='com.yunpc.note:id/et',packageName='com.yunpc.note')
            self.assertTrue(edit_text.exists)
            self.d.press(59)
            time.sleep(2)
            self.d.press(42)
            self.d.press(37)
            self.d.press(42)
            self.d.press(37)
            time.sleep(0.5)
            self.d.press(62)
            time.sleep(1)
            self.d.screenshot(img)
            cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
            CropImage(img, cropedImgPath, 0, 0, 1759, 200)
            if not CompareImage(cropedImgPath, BaseImg, 0.9):
                shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
                path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
                self.fail("The failure file path is %s") % path
        CloseButton=self.d(resourceId='android:id/pc_close',packageName='com.yunpc.note')
        if CloseButton.exists:
            CloseButton.click()
            time.sleep(1)
            self.d(resourceId='android:id/button3',packageName='com.yunpc.note').click()
        time.sleep(3)
        logger.info("Exit -- MUAT:InputTest:test_ConvertTest")
               
    def test_CapsLockTest(self):
        logger.info('Enter -- MUAT:InputTest:test_CapsLockTest')
        self.adb_tools.adb_shell('am start -n com.yunpc.note/.app.ui.activity.MainActivityNew')
        time.sleep(2)
        self.d(resourceId='android:id/pc_max',packageName='com.yunpc.note').click()
        edit_text=self.d(resourceId='com.yunpc.note:id/et',packageName='com.yunpc.note')
        self.assertTrue(edit_text.exists)
        self.mouse.click(1724, 10, constants.MouseLeftKey)
        self.mouse.click(1724, 43, constants.MouseLeftKey)
        time.sleep(5)
        self.d.press(32,1)
        self.d.press(32,1)
        self.d.press(32,1)
        self.d.press(32,1)
        time.sleep(1)
        BaseImg = os.path.join(self.BaseImagePath, "test_note_sgcl.jpg")
        name = "test_note_sgcl_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
        img = os.path.join(self.TmpImagePath, name)
        self.d.screenshot(img)
        cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
        CropImage(img, cropedImgPath, 0, 0, 1759, 200)
        if not CompareImage(cropedImgPath, BaseImg, 0.9):
            shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
            self.adb_tools.adb_shell('am force-stop com.yunpc.note')  
            self.adb_tools.adb_shell('am start -n com.yunpc.note/.app.ui.activity.MainActivityNew')
            time.sleep(2)
            self.d(resourceId='android:id/pc_max',packageName='com.yunpc.note').click()
            edit_text=self.d(resourceId='com.yunpc.note:id/et',packageName='com.yunpc.note')
            self.assertTrue(edit_text.exists)
            self.d.press(59)
            time.sleep(2)
            self.d.press(32,1)
            self.d.press(32,1)
            self.d.press(32,1)
            self.d.press(32,1)
            time.sleep(1)
            self.d.screenshot(img)
            cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
            CropImage(img, cropedImgPath, 0, 0, 1759, 200)
            if not CompareImage(cropedImgPath, BaseImg, 0.9):
                shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
                path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
                self.fail("The failure file path is %s") % path
          
        CloseButton=self.d(resourceId='android:id/pc_close',packageName='com.yunpc.note')
        if CloseButton.exists:
            CloseButton.click()
            time.sleep(1)
            self.d(resourceId='android:id/button3',packageName='com.yunpc.note').click()
        time.sleep(1)
        logger.info("Exit -- MUAT:InputTest:test_CapsLockTest")      

#     def test_ConvertZYTest(self):
#         logger.info('Enter -- MUAT:InputTest:test_ConvertZYTest')
#         self.adb_tools.adb_shell('am start -n com.yunpc.note/.app.ui.activity.MainActivityNew')
#         time.sleep(2)
#         self.d(resourceId='android:id/pc_max',packageName='com.yunpc.note').click()
#         edit_text=self.d(resourceId='com.yunpc.note:id/et',packageName='com.yunpc.note')
#         self.assertTrue(edit_text.exists)
#         self.mouse.click(1724, 10, constants.MouseLeftKey)
#         time.sleep(1)
#         self.mouse.click(1744, 45, constants.MouseLeftKey) 
#         time.sleep(5)
#         self.d.press(42)
#         self.d.press(37)
#         self.d.press(62)
#         time.sleep(1)
#         self.d.press(59)
#         time.sleep(3)
#         self.d.press(42)
#         self.d.press(37)
#         time.sleep(0.5)
#         self.d.press(62)
#         BaseImgshift = os.path.join(self.BaseImagePath, "test_note_czy.jpg")
# #         BaseImgshift1 = os.path.join(self.BaseImagePath, "test_note_choicebar_1.jpg")
#         name = "test_note_czy_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
#         img = os.path.join(self.TmpImagePath, name)
#         self.d.screenshot(img)
#         cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
#         CropImage(img, cropedImgPath, 0, 0, 1780, 200)
#         if not CompareImage(cropedImgPath, BaseImgshift, 0.9):
#             shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
#             path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
#             self.fail("The failure file path is %s") % path
#         CloseButton=self.d(resourceId='android:id/pc_close',packageName='com.yunpc.note')
#         if CloseButton.exists:
#             CloseButton.click()
#         self.mouse.click(1724, 10, constants.MouseLeftKey)
#         time.sleep(1)
#         self.mouse.click(1744, 45, constants.MouseLeftKey)
#         time.sleep(5)
#         self.d.press(59)
#         time.sleep(3)
#         logger.info("Exit -- MUAT:InputTest:test_ConvertZYTest")
 
#     def test_ChoiceBarTest(self):
#         logger.info('Enter -- MUAT:InputTest:test_ChoiceBarTest')
#         self.adb_tools.adb_shell('am start -n com.yunpc.note/.app.ui.activity.MainActivityNew')
#         time.sleep(2)
#         self.d(resourceId='android:id/pc_max',packageName='com.yunpc.note').click()
#         self.mouse.click(1724, 10, constants.MouseLeftKey)
#         time.sleep(1)
#         self.mouse.click(1744, 45, constants.MouseLeftKey)
#         time.sleep(5)
#         self.d.press(43)
#         time.sleep(1)
#         BaseImgChoiceBar = os.path.join(self.BaseImagePath, "test_note_choicebar.jpg")
# #         BaseImgChoiceBar1 = os.path.join(self.BaseImagePath, "test_note_choicebar_1.jpg")
#         name = "test_note_choicebar_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
#         img = os.path.join(self.TmpImagePath, name)
#         self.d.screenshot(img)
#         cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
#         CropImage(img, cropedImgPath, 96,149,1904,260)
#         if not CompareImage(cropedImgPath, BaseImgChoiceBar, 0.9):
#             logger.info('after compare')
#             path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
#             self.fail("The failure file path is %s") % path
#             shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
#             self.adb_tools.adb_shell('am force-stop com.yunpc.note')
#             self.adb_tools.adb_shell('am start -n com.yunpc.note/.app.ui.activity.MainActivityNew')
#             time.sleep(2)
#             self.d(resourceId='android:id/pc_max',packageName='com.yunpc.note').click()
#             edit_text=self.d(resourceId='com.yunpc.note:id/et',packageName='com.yunpc.note')
#             self.assertTrue(edit_text.exists)
#             self.d.press(59)
#             self.d.press(43)
#             time.sleep(1)
#             self.d.screenshot(img)
#             if not CompareImage(cropedImgPath, BaseImgChoiceBar, 0.9):
#                 shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
#                 path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
#                 self.fail("The failure file path is %s") % path
#         CloseButton=self.d(resourceId='android:id/pc_close',packageName='com.yunpc.note')
#         if CloseButton.exists:
#             CloseButton.click()
#             time.sleep(1)
#             self.d(resourceId='android:id/button3',packageName='com.yunpc.note').click()
#             time.sleep(1)
#         logger.info("Exit -- MUAT:InputTest:test_ChoiceBarTest")
        
#     def test_MoveMouseTest(self):
#         logger.info('Enter -- MUAT:InputTest:test_MoveMouseTest')
#         self.adb_tools.adb_shell('am start -n com.android.browser/.app.ui.activity.MainActivityNew')
#         time.sleep(2)
#         self.d(resourceId='android:id/pc_max',packageName='com.yunpc.note').click()
#         self.mouse.click(200, 170, constants.MouseLeftKey)
#         BaseImgMove = os.path.join(self.BaseImagePath, "test_note_movemouse.jpg")
#         BaseImgMove1 = os.path.join(self.BaseImagePath, "test_note_movemouse_1.jpg")
#         name = "test_note_movemouse_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
#         img = os.path.join(self.TmpImagePath, name)
#         self.d.screenshot(img)
#         cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
#         CropImage(img, cropedImgPath, 96,149,1904,189)
#         if not (CompareImage(cropedImgPath, BaseImgMove, 0.9) or CompareImage(cropedImgPath, BaseImgMove1, 0.9)):
#             shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
#             path = os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
#             self.fail("The failure file path is %s") % path
#         else:
#             self.assertTrue(CompareImage(cropedImgPath, BaseImgMove, 0.9) or CompareImage(cropedImgPath, BaseImgMove1, 0.9))
#             logger.info("鼠标移动I")
#         CloseButton=self.d(resourceId='android:id/pc_close',packageName='com.yunpc.note')
#         if CloseButton.exists:
#             CloseButton.click()
#         self.mouse.click(1724, 10, constants.MouseLeftKey)
#         time.sleep(1)
#         self.mouse.click(1744, 45, constants.MouseLeftKey) 
#         logger.info("Exit -- MUAT:InputTest:test_MoveMouseTest")
     
     

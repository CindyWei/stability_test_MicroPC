#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import logging
import unittest
import shutil
from dependency.parametrized_test_case import ParametrizedTestCase
from dependency.automation_device import AutomationDevice
from dependency.account import Account
from dependency import constants
from dependency.apk_manager import ApkManager
from muat_report import MuatReport, GenerateResult
from dependency.adb_log import AdbLog
from dependency.adb_mouse import AdbMouse
from dependency.adb_tools import AdbTools
from win32con import BACKUP_ALTERNATE_DATA

# Init logger
logger_name = '%s-%s' % (constants.LOGGER_CLIENT_MUAT, os.getpid())
logger = logging.getLogger(logger_name)

class FileSystemTest(ParametrizedTestCase):
    def setUp(self):
        # check monitor running status
        if self.mon and not self.mon.running_status:
            self.skipTest('process monitor stop')

        self.d      = AutomationDevice().get_device()
        self.account = Account(self.d)
        self.mouse = AdbMouse()
        self.adb_tools = AdbTools()

        self.account.sleep()
        self.account.wakeup()
        self.account.login()      
        
        self.adb_tools.adb_shell('am force-stop com.alibaba.micropc.fileexplorer')

    def tearDown(self):
        self.adb_tools.adb_shell('am force-stop com.alibaba.micropc.fileexplorer')
        self.account.sleep()
    
    def test_BackupParentDir(self):
        logger.info('Enter -- MUAT:FileSystemTest:test_BackupParentDir')
        apk_manager = ApkManager()
        apk = 'FileExplorer.apk'
        if apk in apk_manager.local_apks_info:
            # stop apk if the apk already started
            apk_manager.close_apk(apk)
 
            # start apk
            apk_manager.start_apk(apk)
            time.sleep(1)
             
            fileexplorer = self.d(text=u"文件管理器", packageName="com.alibaba.micropc.fileexplorer")
            self.assertTrue(fileexplorer.exists)
            if fileexplorer.exists:
                InternalSD = self.d(text=u"内置SD卡", resourceId="com.alibaba.micropc.fileexplorer:id/textView_device_text")
                self.assertTrue(InternalSD.exists)
                if InternalSD.exists:
                    InternalSD.click()
                    InternalSD.click()
                    AndroidDir = self.d(text="Android", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                    if AndroidDir.exists:
                        AndroidDir.click()
                        AndroidDir.click()
                        BackToInternalSD = self.d(text=u"内置SD卡> ", resourceId="com.alibaba.micropc.fileexplorer:id/middlePath")
                        self.assertTrue(BackToInternalSD.exists)
                        if BackToInternalSD.exists:
                            BackToInternalSD.click()
                            time.sleep(5)
                            NewAndroidDir = self.d(text="Android", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                            self.assertTrue(NewAndroidDir.exists)
             
            apk_manager.close_apk(apk)
        logger.info('Exit -- MUAT:FileSystemTest:test_BackupParentDir')
        
    def test_DeleteFileorDir(self):
        logger.info('Enter -- MUAT:FileSystemTest:test_DeleteFileorDir')
        apk_manager = ApkManager()
        apk = 'FileExplorer.apk'
        
        ret = self.adb_tools.adb_shell("mkdir /sdcard/test_DeleteFileorDir", need_ret=True)
        if ret[0].find("failed") == -1:
            self.adb_tools.adb_shell("dd if=/dev/zero of=/sdcard/test_DeleteFileorDir/hello.txt bs=1M count=1")
        else:
            self.skipTest('mkdir failed, errstr: %s') % ret[0]
        
        
        if apk in apk_manager.local_apks_info:
            # stop apk if the apk already started
            apk_manager.close_apk(apk)

            # start apk
            apk_manager.start_apk(apk)
            time.sleep(1)
            
            fileexplorer = self.d(text=u"文件管理器", packageName="com.alibaba.micropc.fileexplorer")
            self.assertTrue(fileexplorer.exists)
            if fileexplorer.exists:
                InternalSD = self.d(text=u"内置SD卡", resourceId="com.alibaba.micropc.fileexplorer:id/textView_device_text")
                self.assertTrue(InternalSD.exists)
                if InternalSD.exists:
                    InternalSD.click()
                    InternalSD.click()
                    testDir = self.d(text="test_DeleteFileorDir", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                    if testDir.exists:
                        testDir.click()
                        testDir.click()
                        toDelFile = self.d(text="hello", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")

                        self.assertTrue(toDelFile.exists)
                        if toDelFile.exists:
                            toDelFile.click()
                            operationButton = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/imageButton_operation")
                            if operationButton.exists:
                                operationButton.click()
                                delOperation = self.d(text=u"删除", className="android.widget.TextView", packageName="com.alibaba.micropc.fileexplorer")
                                if delOperation.exists:
                                    delOperation.click()
                                    time.sleep(2)
                                    newToDelFile = self.d(text="hello", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                    self.assertNotTrue(newToDelFile.exists)
                                    
                                    BackToInternalSD = self.d(text=u"内置SD卡> ", resourceId="com.alibaba.micropc.fileexplorer:id/middlePath")
                                    if BackToInternalSD.exists:
                                        BackToInternalSD.click()
                                        testDir.click()
                                        operationButton = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/imageButton_operation")
                                        if operationButton.exists:
                                            operationButton.click()
                                            delOperation = self.d(text=u"删除", className="android.widget.TextView", packageName="com.alibaba.micropc.fileexplorer")
                                            time.sleep(2)
                                            newTestDir = self.d(text="test_DeleteFileorDir", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                            self.assertNotTrue(newTestDir.exists)
                                            
                            
                        
            self.adb_tools.adb_shell("rm -R /sdcard/test_DeleteFileorDir")
            apk_manager.close_apk(apk)
            
        logger.info('Exit -- MUAT:FileSystemTest:test_DeleteFileorDir')    
    
    def test_CutAndPasteFileorDir(self):
        logger.info('Enter -- MUAT:FileSystemTest:test_CutAndPasteFileorDir')
        apk_manager = ApkManager()
        apk = 'FileExplorer.apk'
        
        ret = self.adb_tools.adb_shell("mkdir /sdcard/test_CutAndPasteFileorDir", need_ret=True)
        if ret[0].find("failed") == -1:
            ret = self.adb_tools.adb_shell("mkdir /sdcard/test_CutAndPasteFileorDir/dest", need_ret=True)
            if ret[0].find("failed") == -1:
                self.adb_tools.adb_shell("dd if=/dev/zero of=/sdcard/test_CutAndPasteFileorDir/dest/hello1.txt bs=1M count=1")
                self.adb_tools.adb_shell("dd if=/dev/zero of=/sdcard/test_CutAndPasteFileorDir/dest/hello2.txt bs=1M count=1")
            else:
                self.skipTest('mkdir dest failed, errstr: %s') % ret[0]
        else:
            self.skipTest('mkdir test_CutAndPasteFileorDir failed, errstr: %s') % ret[0]
        
        
        if apk in apk_manager.local_apks_info:
            # stop apk if the apk already started
            apk_manager.close_apk(apk)

            # start apk
            apk_manager.start_apk(apk)
            time.sleep(1)
            
            fileexplorer = self.d(text=u"文件管理器", packageName="com.alibaba.micropc.fileexplorer")
            self.assertTrue(fileexplorer.exists)
            if fileexplorer.exists:
                InternalSD = self.d(text=u"内置SD卡", resourceId="com.alibaba.micropc.fileexplorer:id/textView_device_text")
                self.assertTrue(InternalSD.exists)
                if InternalSD.exists:
                    InternalSD.click()
                    InternalSD.click()
                    testDir = self.d(text="test_CutAndPasteFileorDir", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                    if testDir.exists:
                        testDir.click()
                        testDir.click()
                        
                        destDir = self.d(text="dest", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                        if destDir.exists:
                            destDir.click()
                            destDir.click()
                            # now path is /sdcard/test_CutAndPasteFileorDir/dest
                            # cut the file to patent path
                            toCutFile = self.d(text="hello1", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                            self.assertTrue(toCutFile.exists)
                            if toCutFile.exists:
                                toCutFile.click()
                                operationButton = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/imageButton_operation")
                                if operationButton.exists:
                                    operationButton.click()
                                    cutOperation = self.d(text=u"剪切", className="android.widget.TextView", packageName="com.alibaba.micropc.fileexplorer")
                                    if cutOperation.exists:
                                    	# cut 
                                        cutOperation.click()
                                        time.sleep(2)
                                        
                                        # back to parent path. now path is /sdcard/test_CutAndPasteFileorDir                                 
                                        BackToParentPath = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/middlePath")
                                        if BackToParentPath.exists:
                                            BackToParentPath.click()
                                            
                                            operationButton = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/imageButton_operation")
                                            if operationButton.exists:
                                                operationButton.click()
                                                # paste the file
                                                pasteOperation = self.d(text=u"粘贴", className="android.widget.TextView", packageName="com.alibaba.micropc.fileexplorer")
                                                pasteOperation.click()
                                                time.sleep(2)
                                                newPasteFile = self.d(text="hello1", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                                # check the file exists
                                                self.assertTrue(newPasteFile.exists)
                                                # entry the dest dir, now path is /sdcard/test_CutAndPasteFileorDir/dest
                                            	destDir = self.d(text="dest", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                            	if destDir.exists:
                                            		destDir.click()
                                            		destDir.click()
                                            		newCutFile = self.d(text="hello1", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                            		# check the file not exists
                                            		self.assertNotTrue(newCutFile.exists)
                                            		BackToParentPath = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/middlePath")
                                            		if BackToParentPath.exists:
                                            			# back to parent path, now the path is /sdcard/test_CutAndPasteFileorDir
                                            			BackToParentPath.click()
                                            			# cut the dir
                                                        destDir = self.d(text="dest", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                                        if destDir.exists:
                                                         	destDir.click()
                                                         	operationButton = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/imageButton_operation")
                                                         	if operationButton.exists:
                                                         		operationButton.click()
                                                         		
                                                                cutOperation = self.d(text=u"剪切", className="android.widget.TextView", packageName="com.alibaba.micropc.fileexplorer")
                                                                if cutOperation.exists:
                                                                	# cut
                                                                    cutOperation.click()
                                                                    time.sleep(2)
                                                                    #back to the parent path, now the path is /sdcard
                                                                    BackToParentPath = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/middlePath")
                                                                    if BackToParentPath.exists:
                                                        				BackToParentPath.click()
                                                        				operationButton = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/imageButton_operation")
                                                        				if operationButton.exists:
                                                        					operationButton.click()
                                                        					# paste the dir
                                                        					pasteOperation = self.d(text=u"粘贴", className="android.widget.TextView", packageName="com.alibaba.micropc.fileexplorer")
                                                        					pasteOperation.click()
                                                        					time.sleep(2)
                                                        					newDestDir = self.d(text="dest", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                                        			  		self.assertTrue(newDestDir.exists)
                                        
                        
            self.adb_tools.adb_shell("rm -R /sdcard/test_CutAndPasteFileorDir")
            apk_manager.close_apk(apk)
            
        logger.info('Exit -- MUAT:FileSystemTest:test_CutAndPasteFileorDir')
    
    def test_CopyAndPasteFileorDir(self):
        logger.info('Enter -- MUAT:FileSystemTest:test_CopyAndPasteFileorDir')
        apk_manager = ApkManager()
        apk = 'FileExplorer.apk'
        
        ret = self.adb_tools.adb_shell("mkdir /sdcard/test_CopyAndPasteFileorDir", need_ret=True)
        if ret[0].find("failed") == -1:
            ret = self.adb_tools.adb_shell("mkdir /sdcard/test_CopyAndPasteFileorDir/dest", need_ret=True)
            if ret[0].find("failed") == -1:
                self.adb_tools.adb_shell("dd if=/dev/zero of=/sdcard/test_CopyAndPasteFileorDir/dest/hello1.txt bs=1M count=1")
                self.adb_tools.adb_shell("dd if=/dev/zero of=/sdcard/test_CopyAndPasteFileorDir/dest/hello2.txt bs=1M count=1")
            else:
                self.skipTest('mkdir dest failed, errstr: %s') % ret[0]
        else:
            self.skipTest('mkdir test_CopyAndPasteFileorDir failed, errstr: %s') % ret[0]
        
        
        if apk in apk_manager.local_apks_info:
            # stop apk if the apk already started
            apk_manager.close_apk(apk)

            # start apk
            apk_manager.start_apk(apk)
            time.sleep(1)
            
            fileexplorer = self.d(text=u"文件管理器", packageName="com.alibaba.micropc.fileexplorer")
            self.assertTrue(fileexplorer.exists)
            if fileexplorer.exists:
                InternalSD = self.d(text=u"内置SD卡", resourceId="com.alibaba.micropc.fileexplorer:id/textView_device_text")
                self.assertTrue(InternalSD.exists)
                if InternalSD.exists:
                    InternalSD.click()
                    InternalSD.click()
                    testDir = self.d(text="test_CopyAndPasteFileorDir", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                    if testDir.exists:
                        testDir.click()
                        testDir.click()
                        
                        destDir = self.d(text="dest", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                        if destDir.exists:
                            destDir.click()
                            destDir.click()
                            # now path is /sdcard/test_CutAndPasteFileorDir/dest
                            # cut the file to patent path
                            toCopyFile = self.d(text="hello1", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                            self.assertTrue(toCopyFile.exists)
                            if toCopyFile.exists:
                                toCopyFile.click()
                                operationButton = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/imageButton_operation")
                                if operationButton.exists:
                                    operationButton.click()
                                    copyOperation = self.d(text=u"复制", className="android.widget.TextView", packageName="com.alibaba.micropc.fileexplorer")
                                    if copyOperation.exists:
                                    	# cut 
                                        copyOperation.click()
                                        time.sleep(2)
                                        
                                        # back to parent path. now path is /sdcard/test_CutAndPasteFileorDir                                 
                                        BackToParentPath = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/middlePath")
                                        if BackToParentPath.exists:
                                            BackToParentPath.click()
                                            
                                            operationButton = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/imageButton_operation")
                                            if operationButton.exists:
                                                operationButton.click()
                                                # paste the file
                                                pasteOperation = self.d(text=u"粘贴", className="android.widget.TextView", packageName="com.alibaba.micropc.fileexplorer")
                                                pasteOperation.click()
                                                time.sleep(2)
                                                newPasteFile = self.d(text="hello1", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                                # check the file exists
                                                self.assertTrue(newPasteFile.exists)
                                                # entry the dest dir, now path is /sdcard/test_CutAndPasteFileorDir/dest
                                            	destDir = self.d(text="dest", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                            	if destDir.exists:
                                            		destDir.click()
                                            		destDir.click()
                                            		newCopyFile = self.d(text="hello1", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                            		# check the file exists
                                            		self.assertTrue(newCopyFile.exists)
                                            		BackToParentPath = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/middlePath")
                                            		if BackToParentPath.exists:
                                            			# back to parent path, now the path is /sdcard/test_CutAndPasteFileorDir
                                            			BackToParentPath.click()
                                            			# cut the dir
                                                        destDir = self.d(text="dest", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                                        if destDir.exists:
                                                         	destDir.click()
                                                         	operationButton = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/imageButton_operation")
                                                         	if operationButton.exists:
                                                         		operationButton.click()
                                                         		
                                                                copyOperation = self.d(text=u"复制", className="android.widget.TextView", packageName="com.alibaba.micropc.fileexplorer")
                                                                if copyOperation.exists:
                                                                	# cut
                                                                    copyOperation.click()
                                                                    time.sleep(2)
                                                                    #back to the parent path, now the path is /sdcard
                                                                    BackToParentPath = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/middlePath")
                                                                    if BackToParentPath.exists:
                                                        				BackToParentPath.click()
                                                        				operationButton = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/imageButton_operation")
                                                        				if operationButton.exists:
                                                        					operationButton.click()
                                                        					# paste the dir
                                                        					pasteOperation = self.d(text=u"粘贴", className="android.widget.TextView", packageName="com.alibaba.micropc.fileexplorer")
                                                        					pasteOperation.click()
                                                        					time.sleep(2)
                                                        					# check the dir exists
                                                        					newDestDir = self.d(text="dest", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                                        			  		self.assertTrue(newDestDir.exists)
                                        
                        
            self.adb_tools.adb_shell("rm -R /sdcard/test_CutAndPasteFileorDir")
            apk_manager.close_apk(apk)
            
        logger.info('Exit -- MUAT:FileSystemTest:test_CutAndPasteFileorDir')   
    
    def test_RenameFileorDir(self):
        logger.info('Enter -- MUAT:FileSystemTest:test_RenameFileorDir')
        apk_manager = ApkManager()
        apk = 'FileExplorer.apk'
        
        ret = self.adb_tools.adb_shell("mkdir /sdcard/test_RenameFileorDir", need_ret=True)
        if ret[0].find("failed") == -1:
            self.adb_tools.adb_shell("dd if=/dev/zero of=/sdcard/test_RenameFileorDir/hello.txt bs=1M count=1")
        else:
            self.skipTest('mkdir failed, errstr: %s') % ret[0]
        
        
        if apk in apk_manager.local_apks_info:
            # stop apk if the apk already started
            apk_manager.close_apk(apk)

            # start apk
            apk_manager.start_apk(apk)
            time.sleep(1)
            
            fileexplorer = self.d(text=u"文件管理器", packageName="com.alibaba.micropc.fileexplorer")
            self.assertTrue(fileexplorer.exists)
            if fileexplorer.exists:
                InternalSD = self.d(text=u"内置SD卡", resourceId="com.alibaba.micropc.fileexplorer:id/textView_device_text")
                self.assertTrue(InternalSD.exists)
                if InternalSD.exists:
                    InternalSD.click()
                    InternalSD.click()
                    testDir = self.d(text="test_RenameFileorDir", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                    if testDir.exists:
                        testDir.click()
                        testDir.click()
                        toRenameFile = self.d(text="hello", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")

                        self.assertTrue(toRenameFile.exists)
                        if toRenameFile.exists:
                            toRenameFile.click()
                            operationButton = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/imageButton_operation")
                            if operationButton.exists:
                                operationButton.click()
                                renameOperation = self.d(text=u"重命名", className="android.widget.TextView", packageName="com.alibaba.micropc.fileexplorer")
                                if renameOperation.exists:
                                    renameOperation.click()
                                    time.sleep(2)
                                    editText = self.d(text="hello", className="android.widget.EditText")
                                    if editText.exists:
                                    	editText.set_text("renamedhello")
                                    	# press enter key
                                    	self.d.press(0x42)
                                    	renamedFile = self.d(text="renamedhello", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                     	self.assertTrue(renamedFile.exists)
                                     	BackToParentPath = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/middlePath")
                                     	if BackToParentPath.exists:
                                     		BackToParentPath.click()
                                     		testDir = self.d(text="test_RenameFileorDir", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                     		if testDir.exists:
                                         		testDir.click()
                                                operationButton = self.d(resourceId="com.alibaba.micropc.fileexplorer:id/imageButton_operation")
                                                if operationButton.exists:
                                                    operationButton.click()
                                                    renameOperation = self.d(text=u"重命名", className="android.widget.TextView", packageName="com.alibaba.micropc.fileexplorer")
                                                    time.sleep(2)
                                                    editText = self.d(text="test_RenameFileorDir", className="android.widget.EditText")
                                                    if editText.exists:
                                    					editText.set_text("renamed_test")
                                    					# press enter key
                                    					self.d.press(0x42)
                                    					newTestDir = self.d(text="renamed_test", packageName="com.alibaba.micropc.fileexplorer", className="android.widget.TextView")
                                    					self.assertTrue(newTestDir.exists)
            self.adb_tools.adb_shell("rm -R /sdcard/test_RenameFileorDir")
            self.adb_tools.adb_shell("rm -R /sdcard/renamed_test")
            apk_manager.close_apk(apk)
            
        logger.info('Exit -- MUAT:FileSystemTest:test_DeleteFileorDir')    
                
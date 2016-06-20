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
from dependency.getcpuinfo import getcpuinfo
from dependency import constants
from dependency.apk_manager import ApkManager
from muat_report import MuatReport, GenerateResult
from dependency.adb_log import AdbLog
from dependency.adb_mouse import AdbMouse
from dependency.adb_tools import AdbTools
from uiautomator import Device
# Init logger
logger_name = '%s-%s' % (constants.LOGGER_CLIENT_MUAT, os.getpid())
logger = logging.getLogger(logger_name)

class ChromeTest(ParametrizedTestCase):

	def setUp(self):
		# check monitor running status
		if self.mon and not self.mon.running_status:
			self.skipTest('process monitor stop')
		self.d = AutomationDevice().get_device()

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
		time.sleep(5)

	def tearDown(self):
		BaseImg = os.path.join(self.BaseImagePath, "test_TaskBar1.jpg")
		name = "test_TaskBar1_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
		img = os.path.join(self.TmpImagePath, name)
		self.d.screenshot(img)
		cropedImgPath = os.path.join(self.TmpImagePath, "croped", name.replace(".jpg", "_croped.jpg"))
		CropImage(img, cropedImgPath, 125,1040,710,1080)
		if not CompareImage(cropedImgPath, BaseImg, 0.9):
			shutil.copy(cropedImgPath, os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg")))
			self.fail("The failure file path is %s") % os.path.join(self.FailureIamgePath, name.replace(".jpg", "_failure.jpg"))
		
		#open youku
		logger.info('close the youku application................')
		self.adb_tools.adb_shell('am force-stop com.youku.phone.x86')
		time.sleep(2)
		#open ttpod
		logger.info('close the ttpod application................')
		self.adb_tools.adb_shell("am force-stop com.sds.android.ttpod")
		time.sleep(2)
		#open QQ
		logger.info('close QQ application.......................')
		self.adb_tools.adb_shell("am force-stop com.tencent.mobileqq")
		time.sleep(2)
		#open xiami
		logger.info('close xiami application.......................')
		self.adb_tools.adb_shell("am force-stop fm.xiami.main")
		time.sleep(2)
		#open qianniu
		logger.info('close qianniiu application.......................')
		self.adb_tools.adb_shell('am force-stop com.taobao.qianniu')
		time.sleep(2)
		#open weibo
		logger.info('close weibo application.......................')
		self.adb_tools.adb_shell('am force-stop com.sina.weibotab')
		time.sleep(2)
		#open wps_pro
		logger.info('close wps application.......................')
		self.adb_tools.adb_shell("am force-stop com.kingsoft.moffice_pro")
		time.sleep(2)
		#open gaode map
		logger.info('close minimap application.......................')
		self.adb_tools.adb_shell("am force-stop com.autonavi.minimap")
		time.sleep(2)
		#open wangxin
		logger.info('close mobileim application.......................')
		self.adb_tools.adb_shell("am force-stop com.alibaba.mobileim")
		time.sleep(2)
		#open taobao
		logger.info('close taobaoHD application.......................')
		self.adb_tools.adb_shell("am force-stop com.taobao.apad")
		time.sleep(2)
		#open alilang
		logger.info('close alilang application.......................')
		self.adb_tools.adb_shell("am force-stop com.alibaba.android.security.activity")
		time.sleep(2)
		self.account.logout()

	def test_OpenChromeTab(self):
		logger.info('Enter -- MUAT:ChromeTest:test_OpenChromeTab')
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
		#open alilang
# 		logger.info('open alilang application.......................')
# 		self.adb_tools.adb_shell("am start -n com.alibaba.android.security.activity/.WelcomeActivity")
# 		time.sleep(3)
		getcpuinfo("after open 10 app.....\n")
		time.sleep(10)
		#browser
		self.adb_tools.adb_shell("am start -n com.android.browser/.BrowserActivity")
		time.sleep(3)
		url = self.d(resourceId='com.android.browser:id/url', className='android.widget.EditText', packageName='com.android.browser')
		url.clear_text()
		url.set_text('cun.taobao.com')
		self.d.press(0x42)
		time.sleep(3)
		getcpuinfo("after open 1 tab....\n")
		for i in range(15):
			tabbtn = self.d(resourceId='com.android.browser:id/newtab')
			tabbtn.click()
			time.sleep(2)
			url = self.d(resourceId='com.android.browser:id/url')
			url.clear_text()
			url.set_text("cun.taobao.com")
			self.d.press(0x42)
			time.sleep(3)
			info = "open %s tab...\n" % (i+2)
			getcpuinfo(info)


		time.sleep(10)
		closebtn = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.android.browser")
		closebtn.click()
		time.sleep(3)
		getcpuinfo("after close the browser......\n")
		time.sleep(10)
		#open chrome
		self.adb_tools.adb_shell("am start -n org.chromium.chrome/com.google.android.apps.chrome.Main")
		time.sleep(3)
# 		pc_max = self.d(resourceId='android:id/pc_max', className='android.widget.ImageView', packageName='org.chromium.chrome')
# 		pc_max.click()
# 		time.sleep(2)
		# url_bar = self.d(resourceId='org.chromium.chrome:id/url_bar')
		# url_bar.click()
		# url_bar.clear_text()
		# url_bar.set_text("cun.taobao.com")
		# self.d.press(0x42)
		# time.sleep(5)
		getcpuinfo("after open chrome 1 tab.....\n")
		# d = Device('F3YMD3000812')
		# d.press(0x3e, 0x71)
		time.sleep(10)
		for i in range(15):
			# d.press(0x30, 0x71)
			# new_tab = self.d(resourceId='empty_new_tab_button')
			# new_tab.click()
			# time.sleep(3)
			# url_bar = self.d(resourceId='org.chromium.chrome:id/url_bar')
			# url_bar.click()
			# url_bar.clear_text()
			# url_bar.set_text("cun.taobao.com")
			# self.d.press(0x42)
			# time.sleep(5)
			# self.d(className='android.view.View').child(index=0).click()
			#self.mouse.click(940, 466, constants.MouseLeftKey)
			time.sleep(1)
			self.d(resourceId='org.chromium.chrome:id/menu_button', className='android.widget.ImageButton').click()
			time.sleep(2)
			self.d(resourceId='org.chromium.chrome:id/menu_item_text').click()
			time.sleep(1)
			url_bar = self.d(resourceId='org.chromium.chrome:id/url_bar')
			url_bar.clear_text()
			url_bar.set_text("cun.taobao.com")
			self.d.press(0x42)
			time.sleep(2)
# 			self.d(resourceId='org.chromium.chrome:id/title').click()
# 			time.sleep(10)
			str ='after open chrome %s tab...\n' % (i+2)
			getcpuinfo(str)
		#close chrome
		closebtn = self.d(resourceId='android:id/pc_close', className='android.widget.ImageView', packageName='org.chromium.chrome')
		closebtn.click()

		logger.info('Exit -- MUAT:ChromeTest:test_OpenChromeTab')
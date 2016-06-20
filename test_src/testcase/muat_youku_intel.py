#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'wb-zhaoxinjian'

import os
import re
import time
import logging
import random
import unittest
import shutil
import sys
from dependency import screen_shot
from dependency.parametrized_test_case import ParametrizedTestCase
from dependency.automation_device import AutomationDevice
from dependency.account import Account
from dependency import constants
from dependency.apk_manager import ApkManager
from muat_report import MuatReport, GenerateResult
from dependency.adb_log import AdbLog
from Tkconstants import TOP
from dependency.adb_mouse import AdbMouse
from dependency.adb_tools import AdbTools

# Init logger
logger_name = '%s-%s' % (constants.LOGGER_CLIENT_MUAT, os.getpid())
logger = logging.getLogger(logger_name)

class YoukuTest(ParametrizedTestCase):

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
#         time.sleep(5)
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.youku.phone.x86")
        #self.assertTure(closeButton.exists)
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
            time.sleep(2)
        else:
            #logger.info("error---------->No closeButton")
            pass

        self.adb_tools.adb_shell("am force-stop com.youku.phone.x86")
        time.sleep(2)


    def test_OpenAndExit(self):

        logger.info('Enter -- MUAT:YoukuTest:test_OpenAndExit')

        #self.adb_tools.adb_shell("am start -n com.youku.phone.x86/.ActivityWelcome")
        #self.adb_tools.adb_shell('am start -n com.youku.phone.x86/com.youku.phone.x86.ActivityWelcome')
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        youku=self.d(text=u'优酷',resourceId='com.aliyun.lightdesk:id/gv_item_appname')
        click_x = youku.info['visibleBounds']['left'] +5
        click_y = youku.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        #如果弹出安全提示对话框则点击同意
        # agree_btn = self.d(resourceId="com.youku.phone.x86:id/app_agreement_done_textview", className="android.widget.TextView", PackageName="com.youku.phone.x86")
        # self.assertEqual(agree_btn.info['text'], u'同意')
        if self.d(resourceId="com.youku.phone.x86:id/app_agreement_done_textview", className="android.widget.TextView", packageName="com.youku.phone.x86").exists:
            self.d(resourceId="com.youku.phone.x86:id/app_agreement_done_textview", className="android.widget.TextView", packageName="com.youku.phone.x86").click()
            time.sleep(3)
        else:
            pass
        #click 我的
        myyouku = self.d(resourceId="com.youku.phone.x86:id/text_myyouku", className="android.widget.TextView", packageName="com.youku.phone.x86")
        self.assertEqual(myyouku.info['text'], u'我的')
        if myyouku.exists:
            myyouku.click()
            time.sleep(1)
        #click 首页
        youkutitle = self.d(resourceId="com.youku.phone.x86:id/text_youkutitle", className="android.widget.TextView")
        self.assertEqual(youkutitle.info['text'], u'首页')
        if youkutitle.exists:
            youkutitle.click()
            time.sleep(1)
        #click 推荐
        youkuguess = self.d(resourceId="com.youku.phone.x86:id/text_youkuguess")
        self.assertEqual(youkuguess.info['text'], u'推荐')
        if youkuguess.exists:
            youkuguess.click()
            time.sleep(1)
        #click 频道
        userlike = self.d(resourceId="com.youku.phone.x86:id/text_userlike")
        self.assertEqual(userlike.info['text'], u'频道')
        if userlike.exists:
            userlike.click()
            time.sleep(1)
        #exit youku app
        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.youku.phone.x86")
        #self.assertTure(closeButton.exists)
        if closeButton.exists:
            #logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
            time.sleep(2)
        else:
            #logger.info("error---------->No closeButton")
            pass


        logger.info('Exit -- MUAT:YoukuTest:test_OpenAndExit')

    def test_PlayAndPause(self):

        logger.info('Enter -- MUAT:YoukuTest:test_PlayAndPause')

        #self.adb_tools.adb_shell("am start -n com.youku.phone.x86.x86/.ActivityWelcome")
        #self.adb_tools.adb_shell('am start -n com.youku.phone.x86/com.youku.phone.x86.ActivityWelcome')
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        youku=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text=u'优酷')
        click_x = youku.info['visibleBounds']['left'] +5
        click_y = youku.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        time.sleep(5)
        #如果弹出安全提示对话框则点击同意
        # agree_btn = self.d(resourceId="com.youku.phone.x86:id/app_agreement_done_textview", className="android.widget.TextView", PackageName="com.youku.phone.x86")
        # self.assertEqual(agree_btn.info['text'], u'同意')
        if self.d(resourceId="com.youku.phone.x86:id/app_agreement_done_textview", className="android.widget.TextView", packageName="com.youku.phone.x86").exists:
            self.d(resourceId="com.youku.phone.x86:id/app_agreement_done_textview", className="android.widget.TextView", packageName="com.youku.phone.x86").click()
            time.sleep(3)
        else:
            pass

        #click 我的
        myyouku = self.d(resourceId="com.youku.phone.x86:id/text_myyouku", className="android.widget.TextView", packageName="com.youku.phone.x86")
        self.assertEqual(myyouku.info['text'], u'我的')
        # logger.info('myyouku info is (%s)' % (myyouku.info['text']))
        if myyouku.exists:
            myyouku.click()
            time.sleep(1)
        #click 首页
        youkutitle = self.d(resourceId="com.youku.phone.x86:id/text_youkutitle", className="android.widget.TextView")
        self.assertEqual(youkutitle.info['text'], u'首页')
        if youkutitle.exists:
            youkutitle.click()
            time.sleep(1)

        #点击首页左侧的视频,进入视频播放界面
        text_youkutitle = self.d(resourceId="com.youku.phone.x86:id/text_youkutitle", className="android.widget.TextView")
        self.assertEqual(text_youkutitle.info['selected'], True)
        if text_youkutitle.exists:
            text_youkutitle.click()
            time.sleep(1)

        video = self.d(resourceId="com.youku.phone.x86:id/homepage_gallery_item_imageview", className="android.widget.ImageView")
        self.assertTrue(video.exists)
        if video.exists:
            video.click()
            #广告45s
            time.sleep(45)
            #视频播放1分钟
            time.sleep(30)
        #调出暂停按钮，点击按钮使食品暂停
        left_border = self.d(resourceId='android:id/left_border', className='android.widget.ImageView')
        self.assertTrue(left_border.exists)
        if left_border.exists:
            pause_btn_x = left_border.info['visibleBounds']['right'] + 60
            pause_btn_y = left_border.info['visibleBounds']['bottom'] - 60
            time.sleep(2)
            self.mouse.doubleclick(pause_btn_x, pause_btn_y, constants.MouseLeftKey)
            time.sleep(15)
            self.mouse.doubleclick(pause_btn_x, pause_btn_y, constants.MouseLeftKey)




        logger.info('Exit -- MUAT:YoukuTest:test_PlayAndPause')

    def test_FastForwardAndRewind(self):
        logger.info('Enter -- MUAT:YoukuTest:test_FastForwardAndRewind')

        #self.adb_tools.adb_shell("am start -n com.youku.phone.x86/.ActivityWelcome")
        #self.adb_tools.adb_shell('am start -n com.youku.phone.x86/com.youku.phone.x86.ActivityWelcome')
        time.sleep(1)
        self.d.click(constants.MUAT_APP_LIST_EMPTY_X, constants.MUAT_APP_LIST_EMPTY_Y)
        time.sleep(0.2)
        self.d.click(constants.MUAT_APP_LIST_POINT_X, constants.MUAT_APP_LIST_POINT_Y)
        time.sleep(1)
        youku=self.d(resourceId='com.aliyun.lightdesk:id/gv_item_appname',text=u'优酷')
        click_x = youku.info['visibleBounds']['left'] +5
        click_y = youku.info['visibleBounds']['top'] +5
        self.mouse.click(click_x, click_y, constants.MouseLeftKey)
        time.sleep(5)
        #如果弹出安全提示对话框则点击同意
        # agree_btn = self.d(resourceId="com.youku.phone.x86:id/app_agreement_done_textview", className="android.widget.TextView", PackageName="com.youku.phone.x86")
        # self.assertEqual(agree_btn.info['text'], u'同意')
        if self.d(resourceId="com.youku.phone.x86:id/app_agreement_done_textview", className="android.widget.TextView", packageName="com.youku.phone.x86").exists:
            self.d(resourceId="com.youku.phone.x86:id/app_agreement_done_textview", className="android.widget.TextView", packageName="com.youku.phone.x86").click()
            time.sleep(3)
        else:
            pass

        #click 我的
        myyouku = self.d(resourceId="com.youku.phone.x86:id/text_myyouku", className="android.widget.TextView")
        self.assertEqual(myyouku.info['text'], u'我的')
        if not myyouku.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self, name)
            time.sleep(2)
        elif myyouku.exists:
            myyouku.click()
            time.sleep(1)
        #click 首页
        youkutitle = self.d(resourceId="com.youku.phone.x86:id/text_youkutitle", className="android.widget.TextView")
        self.assertEqual(youkutitle.info['text'], u'首页')
        if youkutitle.exists:
            youkutitle.click()
            time.sleep(1)

        #点击首页左侧的视频,进入视频播放界面
        text_youkutitle = self.d(resourceId="com.youku.phone.x86:id/text_youkutitle", className="android.widget.TextView")
        self.assertEqual(text_youkutitle.info['selected'], True)
        if text_youkutitle.exists:
            text_youkutitle.click()
            time.sleep(1)

        video = self.d(resourceId="com.youku.phone.x86:id/homepage_gallery_item_imageview", className="android.widget.ImageView")
        self.assertTrue(video.exists)
        if video.exists:
            video.click()
        #广告45s
        time.sleep(60)
        #视频播放1分钟
        time.sleep(30)

        left_border = self.d(resourceId="android:id/left_border", className="android.widget.ImageView")
        Sx = left_border.info['visibleBounds']['right'] + 200
        Sy = (left_border.info['visibleBounds']['top'] + left_border.info['visibleBounds']['bottom'])/2
        Ex = Sx + 400
        Ey = Sy

        self.d.swipe(Sx, Sy, Ex, Ey, steps=10)
        time.sleep(10)
        self.d.swipe(Ex, Ey, Sx, Sy, steps=10)
        time.sleep(10)

        logger.info('Exit -- MUAT:YoukuTest:test_FastForwardAndRewind')
    def tearDown(self):

        closeButton = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.youku.phone.x86")
        #self.assertTure(closeButton.exists)
        if closeButton.exists:
            logger.debug('click close button: (%s)' % (closeButton.info['packageName']))
            closeButton.click()
            time.sleep(2)
        else:
            #logger.info("error---------->No closeButton")
            pass
        # self.adb_tools.adb_shell("am force-stop com.youku.phone.x86")
        self.adb_tools.adb_shell("am force-stop com.youku.phone.x86")
#         self.account.sleep()
        
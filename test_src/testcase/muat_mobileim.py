#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__: 'wb-zhaoxinjian'
#__mobilephone_ '15313661853'

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

#wangxin test case
class MobileImTest(ParametrizedTestCase):

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
        Button1=self.d(resourceId='com.yunpc.yunosloginui:id/avatar')
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if not Button1.exists:
                break
            else:
                time.sleep(1)
        # if self.adb_tools.adb_shell('ls -al /mydata/app/com.alibaba.mobileim-1.apk'):
        #     self.adb_tools.adb_push('')
        self.adb_tools.adb_shell('am force-stop com.alibaba.mobileim')
        time.sleep(2)
        self.adb_tools.adb_shell('am start -n com.alibaba.mobileim/com.alibaba.mobileim.ui.login.LoginActivity')
        mobileimdialog = self.d(resourceId='android:id/pc_title', className='android.widget.TextView', packageName='com.alibaba.mobileim')
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if  mobileimdialog.exists:
                break
            else:
                time.sleep(1)
        if not mobileimdialog.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(mobileimdialog.exists)
        #if wangxin start , run login
        #  @wb-zhaoxinjian
        if mobileimdialog.exists:
            if self.d(resourceId="com.alibaba.mobileim:id/guide_image_one", className="android.widget.ImageView").exists:
                CustomViewPager = self.d(resourceId="com.alibaba.mobileim:id/container", className="com.alibaba.mobileim.fundamental.widget.CustomViewPager")
                if CustomViewPager.exsits:
                    #startX = CustomViewPager.info
                    logger.debug('CustomViewPager: (%s)' % (CustomViewPager.info['className']))
            else:
                #input wangxin login account:
                wx_account = self.d(resourceId="com.alibaba.mobileim:id/account", className="android.widget.EditText")
                if wx_account.exists and wx_account.info['text'] == u'淘宝帐号/手机号':
                    #self.assertEqual(wx_account.info['text'], u"淘宝帐号/手机号")
                    wx_account.clear_text()
                    time.sleep(2)
                    wx_account.set_text(constants.TEST_WX_USERNAME)
                    time.sleep(2)
                elif wx_account.exists and wx_account.info['text'] == constants.TEST_WX_USERNAME:
                    pass

                #input wangxin login password
                wx_password = self.d(resourceId="com.alibaba.mobileim:id/password", className="android.widget.EditText")
                if wx_password.exists:
                    # self.assertEqual(password.info['text'], u'密码')
                    wx_password.clear_text()
                    wx_password.set_text(constants.TEST_WX_PASSWD)
                    time.sleep(2)

                wx_loginbtn = self.d(resourceId="com.alibaba.mobileim:id/login", className="android.widget.Button")
                if wx_loginbtn.exists:
                    self.assertEqual(wx_loginbtn.info['text'], u'登录')
                    wx_loginbtn.click()
                    start=time.time()
                    while time.time()-start<constants.Time_Out:
                        if not wx_loginbtn.exists:
                            break
                        else:
                            time.sleep(1)

                #whether update dialog appear, if click cancel button, if not run else operation
                if self.d(resourceId="com.alibaba.mobileim:id/pcenterPanel", className="android.widget.LinearLayout").exists:
                    update_cancelBtn = self.d(resourceId="com.alibaba.mobileim:id/button2", className="android.widget.Button")
                    if not update_cancelBtn.exists:
                        name = sys._getframe().f_code.co_name
                        screen_shot.ScreenShot(self,name)
                    self.assertTrue(update_cancelBtn.exists)
                    if update_cancelBtn.exists:
                        update_cancelBtn.click()
                        time.sleep(1)

    def test_LoginAndLogout(self):
        logger.info('Enter -- MUAT:MobileImTest:test_LoginAndLogout')
        #这部分内容已经移到tearUp()函数中了
        # self.adb_tools.adb_shell('am start -n com.alibaba.mobileim/com.alibaba.mobileim.ui.login.LoginActivity')
        # time.sleep(5)
        # mobileimdialog = self.d(resourceId='android:id/pc_decor_content', className='android.widget.RelativeLayout', packageName='com.alibaba.mobileim')
        # self.assertTrue(mobileimdialog.exists)
        # #if wangxin start , run login
        # #  @wb-zhaoxinjian
        # if mobileimdialog.exists:
        #     if self.d(resourceId="com.alibaba.mobileim:id/guide_image_one", className="android.widget.ImageView").exists:
        #         CustomViewPager = self.d(resourceId="com.alibaba.mobileim:id/container", className="com.alibaba.mobileim.fundamental.widget.CustomViewPager")
        #         if CustomViewPager.exsits:
        #             #startX = CustomViewPager.info
        #             logger.debug('CustomViewPager: (%s)' % (CustomViewPager.info['className']))
        #     else:
        #         #input wangxin login account:
        #         wx_account = self.d(resourceId="com.alibaba.mobileim:id/account", className="android.widget.EditText")
        #         if wx_account.exists and wx_account.info['text'] == u'淘宝帐号/手机号':
        #             #self.assertEqual(wx_account.info['text'], u"淘宝帐号/手机号")
        #             wx_account.clear_text()
        #             time.sleep(2)
        #             wx_account.set_text(constants.TEST_WX_USERNAME)
        #             time.sleep(2)
        #         elif wx_account.exists and wx_account.info['text'] == constants.TEST_WX_USERNAME:
        #             pass
        #
        #         #input wangxin login password
        #         wx_password = self.d(resourceId="com.alibaba.mobileim:id/password", className="android.widget.EditText")
        #         if wx_password.exists:
        #             # self.assertEqual(password.info['text'], u'密码')
        #             wx_password.clear_text()
        #             wx_password.set_text("test1234")
        #             time.sleep(2)
        #
        #         wx_loginbtn = self.d(resourceId="com.alibaba.mobileim:id/login", className="android.widget.Button")
        #         if wx_loginbtn.exists:
        #             self.assertEqual(wx_loginbtn.info['text'], u'登录')
        #             wx_loginbtn.click()
        #             time.sleep(5)
        #
        #         #whether update dialog appear, if click cancel button, if not run else operation
        #         if self.d(resourceId="com.alibaba.mobileim:id/pcenterPanel", className="android.widget.LinearLayout").exists:
        #             update_cancelBtn = self.d(resourceId="com.alibaba.mobileim:id/button2", className="android.widget.Button")
        #             self.assertTrue(update_cancelBtn.exists)
        #             if update_cancelBtn.exists:
        #                 update_cancelBtn.click()
        #                 time.sleep(1)
 
        # check more infomation
        self_btn = self.d(resourceId="com.alibaba.mobileim:id/title_self_button", className="android.widget.TextView")
        self.assertEqual(self_btn.info['text'], u'更多')
 
        if self_btn.exists:
            self_btn.click()
            time.sleep(1)
            # more info screenshot and compare
 
            self_btn.click()
 
            # enter contact tab
        tab_friends = self.d(resourceId="com.alibaba.mobileim:id/tab_friends_text", className="android.widget.TextView")
        self.assertEqual(tab_friends.info["text"], u"联系人")
 
        if tab_friends.exists:
            tab_friends.click()
            time.sleep(1)
 
            # search friends
        friends_search = self.d(resourceId="com.alibaba.mobileim:id/friends_search_text",
                                className="android.widget.TextView")
        self.assertEqual(friends_search.info["text"], u"搜索")
 
        if friends_search.exists:
            friends_search.click()
            time.sleep(1)
 
            search_key = self.d(resourceId="com.alibaba.mobileim:id/search_key", className="android.widget.EditText")
            self.assertEqual(search_key.info['text'], u'搜索')
            if search_key.exists:
                search_key.clear_text()
                search_key.set_text('tester_1')
                time.sleep(2)
 
                searched_friend = self.d(resourceId="com.alibaba.mobileim:id/select_name",className="android.widget.TextView")
                self.assertEqual(searched_friend.info['text'], 'tester_1')
                time.sleep(2)
 
                if searched_friend.exists:
                    self.d(resourceId="com.alibaba.mobileim:id/title_button",className="android.widget.TextView").click()
 
         # tab_corner test
        tab_corner = self.d(resourceId="com.alibaba.mobileim:id/tab_corner_text", className="android.widget.TextView")
        self.assertEqual(tab_corner.info['text'], u'行家')
 
        if tab_corner.exists:
            tab_corner.click()
            time.sleep(1)
            start_x = tab_corner.info['visibleBounds']['left']
            start_y = tab_corner.info['visibleBounds']['top'] - 20
            end_x = start_x
            end_y = start_y - 820
 
            for i in range(5):
                self.d.drag(start_x, start_y, end_x, end_y, steps=20)
                time.sleep(1)
 
 
        logger.info("Exit --  MUAT:MobileImTest:test_LoginAndLogout")
 
    def test_SendMessage(self):
        logger.info('Enter -- MUAT:MobileImTest:test_SendMessage')
        #Add friends
        tab_friends = self.d(resourceId="com.alibaba.mobileim:id/tab_friends_text", className="android.widget.TextView")
        self.assertEqual(tab_friends.info["text"], u"联系人")
 
        if tab_friends.exists:
            tab_friends.click()
            time.sleep(1)
            #add_friends_btn
            add_contacts_btn = self.d(resourceId="com.alibaba.mobileim:id/title_button")
            if not add_contacts_btn.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(add_contacts_btn.exists)
            if add_contacts_btn.exists:
                add_contacts_btn.click()
                time.sleep(1)
            #添加好友界面
            title = self.d(resourceId="com.alibaba.mobileim:id/title_text", className="android.widget.TextView")
            self.assertEqual(title.info['text'], u'添加好友') #assert the dialog title
            if title.exists:
                search_text = self.d(resourceId="com.alibaba.mobileim:id/search_keyword", className="android.widget.EditText")
                self.assertEqual(search_text.info['text'], u'淘宝帐号')
                if search_text.exists:
                    search_text.clear_text()
                    search_text.set_text(constants.TEST_REMOTE_USERNAME)
 
                    search_btn = self.d(resourceId="com.alibaba.mobileim:id/search_btn", className="android.widget.Button")
                    self.assertEqual(search_btn.info['text'], u'搜索')
                    if search_btn.exists:
                        search_btn.click()
                        time.sleep(2)
            #名片页
            # add_friend_btn = self.d(text=u'添加好友', className="android.widget.Button")
            # self.assertTure(add_friend_btn.exists)
            # if add_friend_btn.exists:
            #     add_friend_btn.click()
            #     time.sleep(1)
            # #添加好友页面
            # if self.d(resourceId="com.alibaba.mobileim:id/name", className="android.widget.TextView").info['text'] == constants.TEST_REMOTE_USERNAME:
            #     confirm_msg = self.d(resourceId="com.alibaba.mobileim:id/confirm_msg", className="android.widget.EditText")
            #     self.assertTrue(confirm_msg.exists)
            #     if confirm_msg.exists:
            #         confirm_msg.clear_text()
            #         confirm_msg.set_text("Hello")
            # send_btn = self.d(text="发送", className="android.widget.TextView")
            # self.assertTrue(send_btn.exists)
            # if send_btn.exists:
            #     send_btn.click()
            #     time.sleep(2)
            btn_send_msg = self.d(resourceId="com.alibaba.mobileim:id/btn_send_message", className="android.widget.Button")
            if not btn_send_msg.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(btn_send_msg.exists)
            if btn_send_msg.exists:
                btn_send_msg.click()
            #进入发送消息对话框
            #check friend's ID
            chat_title = self.d(resourceId="com.alibaba.mobileim:id/chat_title", className="android.widget.TextView")
            self.assertEqual(chat_title.info['text'], constants.TEST_REMOTE_USERNAME)
            #send text message
            chat_inputtext = self.d(resourceId="com.alibaba.mobileim:id/chat_inputtext", className="android.widget.EditText")
            if not chat_inputtext.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(chat_inputtext.exists)
            if chat_inputtext.exists:
                chat_inputtext.click()
                chat_inputtext.clear_text()
 
                chat_inputtext.set_text("hello, nice to meet you.")
                time.sleep(1)
                if self.d(text="发送", className="android.widget.Button").exists:
                    self.d(text="发送", className="android.widget.Button").click()
                else:
                    logger.info(u"发送按钮不存在")
                    pass
            #send emotion image
            #进入表情选择界面
            reply_bar_expand = self.d(resourceId="com.alibaba.mobileim:id/reply_bar_expand", className="android.widget.CheckBox")
            if not reply_bar_expand.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(reply_bar_expand.exists)
            if reply_bar_expand.exists:
                reply_bar_expand.click()
                emotion = self.d(text=u"表情", className="android.widget.TextView")
                if not emotion.exists:
                    name = sys._getframe().f_code.co_name
                    screen_shot.ScreenShot(self,name)
                self.assertTrue(emotion.exists)
                if emotion.exists:
                    emotion.click()
                    time.sleep(1)
                    if self.d(text=u"阿里旺旺表情").exists:
                        self.d(text=u"阿里旺旺表情").click()
                        time.sleep(1)
                    smily_scroller = self.d(resourceId="com.alibaba.mobileim:id/smily_scroller",className="android.widget.FrameLayout")
                    if not smily_scroller.exists:
                        name = sys._getframe().f_code.co_name
                        screen_shot.ScreenShot(self,name)
                    self.assertTrue(smily_scroller.exists)
                    if smily_scroller.exists:
                        # 表情选取坐标起始值：Sx = 655 , Sy = 830 表情间距： Dx = 102, Dy = 55
                        Sx = 655
                        Sy = 830
                        Dx = 102
                        Dy = 55
                        # 表情页滑动起始和结束坐标点
                        startx = smily_scroller.info['visibleBounds']['left'] + 50
                        starty = smily_scroller.info['visibleBounds']['top'] + 80
                        endx = smily_scroller.info['visibleBounds']['left'] + 660
                        endy = starty
 
                        Nx = random.randint(0, 6)
                        Ny = random.randint(0, 2)
                        if Ny == 2 and Nx == 6:
                            Nx = Nx - 1
                        else:
                            pass
 
                        for i in range(random.randint(0, 4)):
                            self.d.drag(startx, starty, endx, endy, steps=10)
                            time.sleep(1)
                        self.d.click(Sx + Nx * Dx, Sy + Ny * Dy)
 
                        if self.d(text="发送", className="android.widget.Button").exists:
                            self.d(text="发送", className="android.widget.Button").click()
                        else:
                            logger.info(u"发送按钮不存在")
                            pass
                    #淘公仔表情
                    if self.d(text="淘公仔表情", className="android.widget.RadioButton").exists:
                        self.d(text="淘公仔表情", className="android.widget.RadioButton").click()
                        smile_layout = self.d(resourceId="com.alibaba.mobileim:id/smile_layout", className="android.widget.LinearLayout")
                        if not smile_layout.exists:
                            name = sys._getframe().f_code.co_name
                            screen_shot.ScreenShot(self,name)
                        self.assertTrue(smile_layout.exists)
                        #logger.info("click the emotion.")
                        if smile_layout.exists:
                            time.sleep(1)
                            #获取第一个淘公仔的坐标点
                            x = smile_layout.info['visibleBounds']['left'] +80
                            y = smile_layout.info['visibleBounds']['top'] +40
                            self.d.click(x, y)
                            time.sleep(1)
            #返回主界面
            chat_back = self.d(resourceId="com.alibaba.mobileim:id/chat_back", className="android.widget.TextView")
            self.assertEqual(chat_back.info['text'], u'返回')
            if chat_back.exists:
                chat_back.click()
                time.sleep(1)
            title_back = self.d(resourceId="com.alibaba.mobileim:id/title_back", className="android.widget.TextView")
            self.assertEqual(title_back.info['text'], u'返回')
            if title_back.exists:
                title_back.click()
                time.sleep(1)
 
 
        logger.info('Exit --  MUAT:MobileImTest:test_SendMessage')
 
    def test_SendtakePhoto(self):
        logger.info('Enter -- MUAT:MobileImTest:test_SendtakePhoto')
        #点击消息栏
        tab_message = self.d(resourceId="com.alibaba.mobileim:id/tab_message_text", className="android.widget.TextView")
        self.assertEqual(tab_message.info['text'], u'消息')
        if tab_message.exists:
            tab_message.click()
            time.sleep(1)
            #查找历史消息找到wb-zhaoxinjian， 点击进入消息对话框
            friend = self.d(text=constants.TEST_REMOTE_USERNAME, resourceId="com.alibaba.mobileim:id/name", className="android.widget.TextView")
            if not friend.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(friend.exists)
            if friend.exists:
                friend.click()
                time.sleep(2)
            # else:
            #     #如果不存在则寻找另外的联系人
            #     pass
            #进入扩展选择界面，选择拍照发送
            reply_bar_expand = self.d(resourceId="com.alibaba.mobileim:id/reply_bar_expand", className="android.widget.CheckBox")
            if not reply_bar_expand.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(reply_bar_expand.exists)
            if reply_bar_expand.exists:
                reply_bar_expand.click()
                takepic = self.d(text=u"拍照", className="android.widget.TextView")
                if not takepic.exists:
                    name = sys._getframe().f_code.co_name
                    screen_shot.ScreenShot(self,name)
                self.assertTrue(takepic.exists)
                if takepic.exists:
                    takepic.click()
                    camera = self.d(resourceId="com.android.camera2:id/shutter_button", className="android.widget.ImageView", packageName="com.android.camera2")
                    start=time.time()
                    while time.time()-start<constants.Time_Out:
                        if  camera.exists:
                            break
                        else:
                            time.sleep(1)
                    #调用系统的相机拍摄照片
                    self.assertEqual(camera.info['contentDescription'], u'快门')
                    if camera.exists:
                        camera.click()
                        btn_done = self.d(resourceId="com.android.camera2:id/btn_done", className="android.widget.ImageView", packageName="com.android.camera2")
                        start=time.time()
                        while time.time()-start<constants.Time_Out:
                            if  btn_done.exists:
                                break
                            else:
                                time.sleep(1)
                        #确认完成拍照
                        self.assertEqual(btn_done.info['contentDescription'], u'完成')
                        if btn_done.exists:
                            btn_done.click()
                            btn_confirm = self.d(resourceId="com.alibaba.mobileim:id/confirm", className="android.widget.Button", packageName="com.alibaba.mobileim")
                            start=time.time()
                            while time.time()-start<constants.Time_Out:
                                if  btn_confirm.exists:
                                    break
                                else:
                                    time.sleep(1)
                            #点击确定按钮，发送照片
                            self.assertEqual(btn_confirm.info['text'], u'确定')
                            if btn_confirm.exists:
                                btn_confirm.click()
                                time.sleep(2)
            #返回主界面
            chat_back = self.d(resourceId="com.alibaba.mobileim:id/chat_back", className="android.widget.TextView")
            self.assertEqual(chat_back.info['text'], u'返回')
            if chat_back.exists:
                chat_back.click()
                time.sleep(1)
 
 
        logger.info('Exit --  MUAT:MobileImTest:test_SendtakePhoto')

    def test_SendCard(self):
        logger.info('Enter -- MUAT:MobileImTest:test_SendCard')
        #点击消息栏
        tab_message = self.d(resourceId="com.alibaba.mobileim:id/tab_message_text", className="android.widget.TextView")
        self.assertEqual(tab_message.info['text'], u'消息')
        if tab_message.exists:
            tab_message.click()
            time.sleep(1)
            #查找历史消息找到wb-zhaoxinjian， 点击进入消息对话框
            friend = self.d(text=constants.TEST_REMOTE_USERNAME, resourceId="com.alibaba.mobileim:id/name", className="android.widget.TextView")
            if not friend.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(friend.exists)
            if friend.exists:
                friend.click()
                time.sleep(2)
            # else:
            #     #如果不存在则寻找另外的联系人
            #     pass
            #进入扩展选择界面，选择名片
            reply_bar_expand = self.d(resourceId="com.alibaba.mobileim:id/reply_bar_expand", className="android.widget.CheckBox")
            if not reply_bar_expand.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(reply_bar_expand.exists)
            if reply_bar_expand.exists:
                reply_bar_expand.click()
                card_btn = self.d(text=u"名片", className="android.widget.TextView")
                if not card_btn.exists:
                    name = sys._getframe().f_code.co_name
                    screen_shot.ScreenShot(self,name)
                self.assertTrue(card_btn.exists)
                if card_btn.exists:
                    card_btn.click()
                    time.sleep(3)
                    #进入选择好友界面，选择好友，并发送
                    wx_friends_btn = self.d(resourceId="com.alibaba.mobileim:id/wx_friends_button", className="android.widget.Button")
                    self.assertEqual(wx_friends_btn.info['text'], u'旺旺好友')
                    if wx_friends_btn.exists:
                        wx_friends_btn.click()
                        time.sleep(1)
                        #选择 景止、洗石、云渡
                        self.d(text=u"景止").click()
                        time.sleep(1)
                        self.d(text=u"洗石").click()
                        time.sleep(1)
                        self.d(text=u"云渡").click()
                        time.sleep(1)
                        #点击确定按钮
                        startbtn = self.d(resourceId="com.alibaba.mobileim:id/start", className="android.widget.Button")
                        if not startbtn.exists:
                            name = sys._getframe().f_code.co_name
                            screen_shot.ScreenShot(self,name)
                        self.assertTrue(startbtn.exists)
                        if startbtn.exists:
                            startbtn.click()
                            time.sleep(1)
            #返回主界面
            chat_back = self.d(resourceId="com.alibaba.mobileim:id/chat_back", className="android.widget.TextView")
            self.assertEqual(chat_back.info['text'], u'返回')
            if chat_back.exists:
                chat_back.click()
                time.sleep(1)


        logger.info('Exit --  MUAT:MobileImTest:test_SendCard')

    def test_SendPicture(self):
        logger.info('Enter -- MUAT:MobileImTest:test_SendPicture')
        #点击消息栏
        tab_message = self.d(resourceId="com.alibaba.mobileim:id/tab_message_text", className="android.widget.TextView")
        self.assertEqual(tab_message.info['text'], u'消息')
        if tab_message.exists:
            tab_message.click()
            time.sleep(1)
            #查找历史消息找到wb-zhaoxinjian， 点击进入消息对话框
            friend = self.d(text=constants.TEST_REMOTE_USERNAME, resourceId="com.alibaba.mobileim:id/name", className="android.widget.TextView")
            if not friend.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(friend.exists)
            if friend.exists:
                friend.click()
                time.sleep(2)
            # else:
            #     #如果不存在则寻找另外的联系人
            #     pass
            #进入扩展选择界面，选择名片
            reply_bar_expand = self.d(resourceId="com.alibaba.mobileim:id/reply_bar_expand", className="android.widget.CheckBox")
            if not reply_bar_expand.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(reply_bar_expand.exists)
            if reply_bar_expand.exists:
                reply_bar_expand.click()
                selectpic_btn = self.d(text=u"选择照片", className="android.widget.TextView")
                if not selectpic_btn.exists:
                    name = sys._getframe().f_code.co_name
                    screen_shot.ScreenShot(self,name)
                self.assertTrue(selectpic_btn.exists)
                if selectpic_btn.exists:
                    selectpic_btn.click()
                    time.sleep(3)
                    pic = self.d(resourceId="com.alibaba.mobileim:id/image_item", className="android.widget.ImageView")
                    if not pic.exists:
                        name = sys._getframe().f_code.co_name
                        screen_shot.ScreenShot(self,name)
                    self.assertTrue(pic.exists)
                    if pic.exists:
                        # logger.info("pic--->(s%)" %(type(pic)))
                        pic.click()
                        time.sleep(1)
                        #选择图片
                        img_check = self.d(resourceId="com.alibaba.mobileim:id/image_check", className="android.widget.ImageView")
                        if not img_check.exists:
                            name = sys._getframe().f_code.co_name
                            screen_shot.ScreenShot(self,name)
                        self.assertTrue(img_check.exists)
                        if img_check.exists:
                            img_check.click()
                            time.sleep(2)
                        #点击完成， 发送图片
                        select_finish = self.d(resourceId="com.alibaba.mobileim:id/select_finish", className="android.widget.Button")
                        self.assertEqual(select_finish.info['text'], u'完成')
                        if select_finish.exists:
                            select_finish.click()
                            time.sleep(2)
        #返回主界面
        chat_back = self.d(resourceId="com.alibaba.mobileim:id/chat_back", className="android.widget.TextView")
        self.assertEqual(chat_back.info['text'], u'返回')
        if chat_back.exists:
            chat_back.click()
            time.sleep(1)
 
        logger.info('Exit --  MUAT:MobileImTest:test_SendPicture')
 
    def test_SendVoice(self):
        logger.info('Enter -- MUAT:MobileImTest:test_SendVoice')
 
        #点击消息栏
        tab_message = self.d(resourceId="com.alibaba.mobileim:id/tab_message_text", className="android.widget.TextView")
        self.assertEqual(tab_message.info['text'], u'消息')
        if tab_message.exists:
            tab_message.click()
            time.sleep(1)
            #查找历史消息找到wb-zhaoxinjian， 点击进入消息对话框
            friend = self.d(text=constants.TEST_REMOTE_USERNAME, resourceId="com.alibaba.mobileim:id/name", className="android.widget.TextView")
            if not friend.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(friend.exists)
            if friend.exists:
                friend.click()
                time.sleep(2)
            # else:
            #     #如果不存在则寻找另外的联系人
            #     pass
            #进入扩展选择界面，选择名片
            reply_bar_expand = self.d(resourceId="com.alibaba.mobileim:id/reply_bar_expand", className="android.widget.CheckBox")
            if not reply_bar_expand.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(reply_bar_expand.exists)
            if reply_bar_expand.exists:
                reply_bar_expand.click()
                voice_btn = self.d(text=u"语音消息", className="android.widget.TextView")
                if not voice_btn.exists:
                    name = sys._getframe().f_code.co_name
                    screen_shot.ScreenShot(self,name)
                self.assertTrue(voice_btn.exists)
                if voice_btn.exists:
                    voice_btn.click()
                    time.sleep(3)
                #长按，启动语音录音
                chat_record = self.d(resourceId="com.alibaba.mobileim:id/chat_record", className="android.widget.Button")
                self.assertEqual(chat_record.info['text'], u'请长按讲话')
                if chat_record.exists:
                    '''
                    还没有解决长按的方法，暂时用long_click()
                    '''
                    chat_record.long_click()
                    time.sleep(2)
        #返回主界面
        chat_back = self.d(resourceId="com.alibaba.mobileim:id/chat_back", className="android.widget.TextView")
        self.assertEqual(chat_back.info['text'], u'返回')
        if chat_back.exists:
            chat_back.click()
            time.sleep(1)
 
        logger.info('Exit --  MUAT:MobileImTest:test_SendVoice')
 
    def test_ModifyInfo(self):
        logger.info('Enter -- MUAT:MobileImTest:test_ModifyInfo')
 
        MobileimTitle=self.d(resourceId='android:id/pc_title', className='android.widget.TextView', packageName='com.alibaba.mobileim')
        if MobileimTitle.exists:
            self.assertEqual(MobileimTitle.info['text'], u'旺信')
            meButton=self.d(resourceId='com.alibaba.mobileim:id/tab_me_text')
            if meButton.exists:
                meButton.click()
                time.sleep(2)
                moreButton=self.d(text=u'更多',packageName='com.alibaba.mobileim')
                if moreButton.exists:
                    moreButton.click()
                    time.sleep(2)
                    if not self.d(text=u'设置', packageName='com.alibaba.mobileim').exists:
                        name = sys._getframe().f_code.co_name
                        screen_shot.ScreenShot(self,name)
                    self.assertTrue(self.d(text=u'设置', packageName='com.alibaba.mobileim').exists)
                    profileButton = self.d(text=u'个人资料', packageName='com.alibaba.mobileim')
                    #modify profile
                    if profileButton.exists:
                        profileButton.click()
                        time.sleep(2)
                        profileName=self.d(resourceId='com.alibaba.mobileim:id/profile_name')
                        profileName.click()
                        time.sleep(2)
                        ModifyName=self.d(resourceId='com.alibaba.mobileim:id/modify_group_name',className='android.widget.EditText')
                        cancelButton=self.d(resourceId='com.alibaba.mobileim:id/modify_cancel',className='android.widget.ImageView')
                        cancelButton.click()
                        #ModifyName.clear_text()
                        ModifyName.set_text("who are you")
                        time.sleep(2)
                        okButton=self.d(text=u'完成',resourceId='com.alibaba.mobileim:id/title_button')
                        if okButton.exists:
                            okButton.click()
                            time.sleep(2)
                            self.assertEqual(profileName.info['text'], "who are you")
                            profileName.click()
                            time.sleep(2)
                            cancelButton.click()
                            ModifyName.set_text("tester_1")
                            time.sleep(2)
                            okButton.click()
                            self.assertEqual(profileName.info['text'], "tester_1")
                        #modify male
                        profileSex=self.d(resourceId='com.alibaba.mobileim:id/setting_profile_gender')
                        if profileSex.exists:
                            if not profileSex.info['text'] == u'男':
                                profileSex.click()
                                time.sleep(2)
                                self.d(resourceId='com.alibaba.mobileim:id/profile_gender_male').click()
                                time.sleep(2)
                                self.assertEqual(profileSex.info['text'], u'男')
                            else:
                                profileSex.click()
                                time.sleep(2)
                                self.d(resourceId='com.alibaba.mobileim:id/profile_gender_female').click()
                                time.sleep(2)
                                self.assertEqual(profileSex.info['text'], u'女')
                        #更换头像
                        profileHead=self.d(resourceId='com.alibaba.mobileim:id/people_head')
                        if profileHead.exists:
                            profileHead.click()
                            TakePicture=self.d(text=u'拍照',resourceId='android:id/text1')
                            if TakePicture.exists:
                                TakePicture.click()
                                start=time.time()
                                while time.time()-start<constants.Time_Out:
                                    if  self.d(resourceId='com.android.camera2:id/shutter_button').exists:
                                        break
                                    else:
                                        time.sleep(1)
                                self.d(resourceId='com.android.camera2:id/shutter_button').click()
                                doneButton=self.d(resourceId='com.android.camera2:id/btn_done')
                                start=time.time()
                                while time.time()-start<constants.Time_Out:
                                    if  doneButton.exists:
                                        break
                                    else:
                                        time.sleep(1)
                                doneButton.click()
                                saveButton=self.d(resourceId='com.alibaba.mobileim:id/save')
                                start=time.time()
                                while time.time()-start<constants.Time_Out:
                                    if  saveButton.exists:
                                        break
                                    else:
                                        time.sleep(1)
                                saveButton.click()
                                time.sleep(3)
 
                        #modify area
                        profileAddress=self.d(resourceId='com.alibaba.mobileim:id/setting_profile_address')
                        area_title=self.d(resourceId='com.alibaba.mobileim:id/title')
                        bj1_x=area_title.info['visibleBounds']['right'] - 20
                        bj1_y=area_title.info['visibleBounds']['bottom'] + 20
                        bj2_x=bj1_x
                        bj2_y=bj1_y + 44
                        tj1_x=bj1_x
                        tj1_y=bj2_y
                        tj2_x=bj1_x
                        tj2_y=bj2_y + 44
                        if profileAddress.exists:
                            profileAddress.click()
                            time.sleep(2)
                            self.d.click(bj1_x,bj1_y)
                            time.sleep(2)
                            self.d.click(bj2_x,bj2_y)
                            time.sleep(3)
                            self.assertEqual(profileAddress.info['text'], u'北京 北京')
                            profileAddress.click()
                            time.sleep(2)
                            self.d.click(tj1_x,tj1_y)
                            time.sleep(2)
                            self.d.click(tj2_x,tj2_y)
                            time.sleep(3)
                            self.assertEqual(profileAddress.info['text'], u'天津 天津')
 
                    #退出登陆
                    backButton=self.d(text=u'返回',resourceId='com.alibaba.mobileim:id/title_back')
                    backButton.click()
                    time.sleep(1)
                    backButton.click()
                    time.sleep(1)
        #             logoutButton=self.d(resourceId='com.alibaba.mobileim:id/setting_logout',className='android.widget.TextView')
        #             self.assertTrue(logoutButton.exists)
        #             if logoutButton.exists:
        #                 logoutButton.click()
        #                 time.sleep(1)
        #                 self.d.press(66)
        #                 self.d.press(66)
        #                 time.sleep(3)
        #             self.assertTrue(LoginButton.exists)
        #
        # closeButton=self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.alibaba.mobileim")
        # if closeButton.exists:
        #     closeButton.click()
        #     time.sleep(3)
        logger.info('Exit -- MUAT:MobileImTest:test_ModifyInfo')
 
    def test_CheckInfo(self):
        logger.info('Enter -- MUAT:MobileImTest:test_CheckInfo')
        # self.adb_tools.adb_shell('am start -n com.alibaba.mobileim/com.alibaba.mobileim.ui.login.LoginActivity')
        # time.sleep(5)
        # #登陆
        # LoginButton=self.d(resourceId='com.alibaba.mobileim:id/login')
        # if LoginButton.exists:
        #     LoginButton.click()
        #     LoginButton.click()
        #     time.sleep(5)
 
        MobileimTitle=self.d(resourceId='android:id/pc_title')
        if not MobileimTitle.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(MobileimTitle.exists)
        if MobileimTitle.exists:
            MobileimTitle.click()
            logger.info('MobileimTitle is here')
 
        MessageButton=self.d(resourceId='com.alibaba.mobileim:id/tab_message_text')
        if not MessageButton.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(MessageButton.exists)
        if MessageButton.exists:
            MessageButton.click()
            logger.info('Message is here')
 
        FriendsButton=self.d(resourceId='com.alibaba.mobileim:id/tab_friends_text')
        if not FriendsButton.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(FriendsButton.exists)
        if FriendsButton.exists:
            FriendsButton.click()
            logger.info('Friends is here')
            SearchButton=self.d(resourceId='com.alibaba.mobileim:id/search_layout')
            if not SearchButton.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(SearchButton.exists)
            ShopButton=self.d(resourceId='com.alibaba.mobileim:id/shop_layout')
            if not ShopButton.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(ShopButton.exists)
            if ShopButton.exists:
                ShopButton.click()
                logger.info('Shop is here')
            GuyBtton=self.d(resourceId='com.alibaba.mobileim:id/friends_layout')
            self.assertTrue(GuyBtton.exists)
            if GuyBtton.exists:
                GuyBtton.click()
                logger.info('Guys is here')
            GruopButton=self.d(resourceId='com.alibaba.mobileim:id/tribe_layout')
            self.assertTrue(GruopButton.exists)
            if GruopButton.exists:
                GruopButton.click()
                logger.info('Gruop is here')
 
        CornerButton=self.d(resourceId='com.alibaba.mobileim:id/tab_corner_text')
        self.assertTrue(CornerButton.exists)
        if CornerButton.exists:
            CornerButton.click()
            logger.info('Corner is here')
 
        MeButton=self.d(resourceId='com.alibaba.mobileim:id/tab_me_text')
        self.assertTrue(MeButton.exists)
        if MeButton.exists:
            MeButton.click()
            logger.info('Me is here')
 
        MaxBtton=self.d(resourceId='android:id/pc_max')
        if not MaxBtton.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(MaxBtton.exists)
        if MaxBtton.exists:
            MaxBtton.click()
            time.sleep(2)
            MaxBtton.click()
            time.sleep(2)
             
 
 
        # closeButton=self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.alibaba.mobileim")
        # if closeButton.exists:
        #     closeButton.click()
        #     time.sleep(3)
        logger.info('Exit -- MUAT:MobileImTest:test_CheckInfo')

#     def test_Drag(self):
#         logger.info('Enter -- MUAT:MobileImTest:test_Drag')
#         self.adb_tools.adb_shell('am start -n com.alibaba.mobileim/com.alibaba.mobileim.ui.login.LoginActivity')
#         time.sleep(5)
#         Button2=self.d(text=u'取消',resourceId='com.alibaba.mobileim:id/button2')
#         if Button2.exists:
#             Button2.click()
#         #登陆
#         LoginButton=self.d(resourceId='com.alibaba.mobileim:id/login')
#         if LoginButton.exists:
#             LoginButton.click()
#             LoginButton.click()
#             time.sleep(5)
#         #拖拉窗口
#         meButton=self.d(resourceId='com.alibaba.mobileim:id/tab_me_text')
#         start_x=meButton.info['visibleBounds']['right']
#         start_y=meButton.info['visibleBounds']['bottom']
#         end_x  =start_x + 100
#         end_x0 =start_x - 100
#         end_y  =start_y + 50
#         self.d.drag(start_x,start_y,end_x,end_y,steps=1)
#         self.d.drag(start_x,start_y,end_x0,end_y)
#         time.sleep(3)





        # closeButton=self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.alibaba.mobileim")
        # if closeButton.exists:
        #     closeButton.click()
        #     time.sleep(3)
        # logger.info('Exit -- MUAT:SettingsSystemTest:test_Drag')

    def tearDown(self):
        # tab_me test
        tab_me = self.d(resourceId="com.alibaba.mobileim:id/tab_me_text", className="android.widget.TextView")
        self.assertEqual(tab_me.info['text'], u'我')

        if tab_me.exists:
            tab_me.click()
            time.sleep(1)

            myname = self.d(resourceId="com.alibaba.mobileim:id/title_text", className="android.widget.TextView")
            self.assertEqual(myname.info['text'], 'tester_1')

            # logout test
            title_btn = self.d(resourceId="com.alibaba.mobileim:id/title_button")
            self.assertEqual(title_btn.info['text'], u'更多')

            if title_btn.exists:
                title_btn.click()
                time.sleep(2)

            # account logout
            logout_btn = self.d(resourceId='com.alibaba.mobileim:id/setting_logout')
            self.assertEqual(logout_btn.info['text'], u'退出登录')

            if logout_btn.exists:
                logout_btn.click()

            exit_massege = self.d(resourceId="com.alibaba.mobileim:id/message", className="android.widget.TextView")
            self.assertEqual(exit_massege.info['text'], u'退出后您将收不到新消息通知，是否确认退出？')
            time.sleep(1)
            if exit_massege.exists:
                self.d(resourceId="com.alibaba.mobileim:id/button1", className="android.widget.Button").click()

        #clear the account
        select_account = self.d(resourceId="com.alibaba.mobileim:id/select_account", className="android.widget.ImageView", packageName="com.alibaba.mobileim")
        if select_account.exists:
            select_account.click()
            if self.d(resourceId='com.alibaba.mobileim:id/delete').exists:
                self.d(resourceId='com.alibaba.mobileim:id/delete').click()

                delete_massage = self.d(resourceId='com.alibaba.mobileim:id/message', className='android.widget.TextView')
                self.assertEqual(delete_massage.info['text'], u'确认删除该帐号记录？')
                if delete_massage.exists:
                    self.d(resourceId="com.alibaba.mobileim:id/button1", className="android.widget.Button").click()

        closebtn = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.alibaba.mobileim")
        #self.assertTure(closebtn.exists)

        if closebtn.exists:
            logger.debug('click close button: (%s)' % (closebtn.info['packageName']))
            closebtn.click()
        #logger.info("EXIT -- MUAT:MobileImTest:close_mobileim")
        self.adb_tools.adb_shell('am force-stop com.alibaba.mobileim')
        self.account.sleep()
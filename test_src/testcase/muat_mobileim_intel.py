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

#         self.account.sleep()
#         self.account.wakeup()
        self.account.login()
        Button1=self.d(resourceId='com.yunpc.yunosloginui:id/avatar')
        start=time.time()
        while time.time()-start<constants.Time_Out:
            if not Button1.exists:
                break
            else:
                time.sleep(1)
        self.adb_tools.adb_shell('am force-stop com.alibaba.mobileim')
        time.sleep(2)
        # self.adb_tools.adb_shell('am start -n com.alibaba.mobileim/com.alibaba.mobileim.ui.login.LoginActivity')
        self.adb_tools.adb_shell('am start -n com.alibaba.mobileim/.ui.tab.MainTabActivity')
#        /.ui.tab.MainTabActivity  /com.alibaba.mobileim.SplashActivity
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
        if mobileimdialog.exists:
            if self.d(resourceId="com.alibaba.mobileim:id/guide_image_one", className="android.widget.ImageView").exists:
                CustomViewPager = self.d(resourceId="com.alibaba.mobileim:id/container", className="com.alibaba.mobileim.fundamental.widget.CustomViewPager")
                if CustomViewPager.exsits:
                    #startX = CustomViewPager.info
                    logger.debug('CustomViewPager: (%s)' % (CustomViewPager.info['className']))
            else:
                #input wangxin login account:
                wx_account = self.d(resourceId="com.alibaba.mobileim:id/accountCompleteTextView", className="android.widget.EditText")
                if wx_account.exists and wx_account.info['text'] == constants.TEST_WX_USERNAME:
                    pass

                elif wx_account.exists and wx_account.info['text'] == u'淘宝帐号/手机号':
                    #self.assertEqual(wx_account.info['text'], u"淘宝帐号/手机号")
                    wx_account.clear_text()
                    time.sleep(2)
                    wx_account.set_text(constants.TEST_WX_USERNAME)
                    time.sleep(2)

                #input wangxin login password
                wx_password = self.d(resourceId="com.alibaba.mobileim:id/content", className="android.widget.EditText")
                if wx_password.exists:
                    # self.assertEqual(password.info['text'], u'密码')
                    wx_password.clear_text()
                    wx_password.set_text(constants.TEST_WX_PASSWD)
                    time.sleep(2)

                wx_loginbtn = self.d(resourceId="com.alibaba.mobileim:id/loginButton", className="android.widget.Button")
                if wx_loginbtn.exists:
                    self.assertEqual(wx_loginbtn.info['text'], u'登录')
                    wx_loginbtn.click()
                    #mobileimimg = self.d(resourceId='com.alibaba.mobileim:id/wxheadImage', className='android.widget.TextView', packageName='com.alibaba.mobileim')
                    start=time.time()
                    while time.time()-start<constants.Time_Out:
                        if self.d(resourceId='com.alibaba.mobileim:id/tab_me_text').exists:
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
  
    def test_SendMessage(self):
        logger.info('Enter -- MUAT:MobileImTest:test_SendMessage')
        tab_friends = self.d(resourceId="com.alibaba.mobileim:id/tab_friends_text", className="android.widget.ImageView")
        self.assertTrue(tab_friends.info["clickable"])
        if tab_friends.exists:
            tab_friends.click()
            time.sleep(1)
            FriendTag=self.d(resourceId='com.alibaba.mobileim:id/friends_layout',packageName='com.alibaba.mobileim')
            FriendTag.click()
            time.sleep(2)
            Friends=self.d(text='tb3489593',resourceId='com.alibaba.mobileim:id/select_name')
            self.assertTrue(Friends.exists)
            Friends.click()
            time.sleep(1)
            
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
                #切换输入法
#                 self.d.press(113,1)
  
                chat_inputtext.set_text("hello, nice to meet you ")
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
                    # smily_scroller = self.d(resourceId="com.alibaba.mobileim:id/smily_scroller",className="android.widget.FrameLayout")
                    # if not smily_scroller.exists:
                    #     name = sys._getframe().f_code.co_name
                    #     screen_shot.ScreenShot(self,name)
                    # self.assertTrue(smily_scroller.exists)
                    # if smily_scroller.exists:
                    #     # 表情选取坐标起始值：Sx = 655 , Sy = 830 表情间距： Dx = 102, Dy = 55
                    #     Sx = 655
                    #     Sy = 830
                    #     Dx = 102
                    #     Dy = 55
                    #     # 表情页滑动起始和结束坐标点
                    #     startx = smily_scroller.info['visibleBounds']['left'] + 50
                    #     starty = smily_scroller.info['visibleBounds']['top'] + 80
                    #     endx = smily_scroller.info['visibleBounds']['left'] + 660
                    #     endy = starty
                    #
                    #     Nx = random.randint(0, 6)
                    #     Ny = random.randint(0, 2)
                    #     if Ny == 2 and Nx == 6:
                    #         Nx = Nx - 1
                    #     else:
                    #         pass
                    #
                    #     for i in range(random.randint(0, 4)):
                    #         self.d.drag(startx, starty, endx, endy, steps=10)
                    #         time.sleep(1)
                    #     self.d.click(Sx + Nx * Dx, Sy + Ny * Dy)
                    #
                        #select emotion
                        emotion_icon = self.d(resourceId='com.alibaba.mobileim:id/image', className='android.widget.ImageView')
                        self.assertTrue(emotion_icon.info['enabled'])
                        if emotion_icon.exists:
                            emotion_icon.click()
                            time.sleep(1)
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
            title_back = self.d(resourceId="com.alibaba.mobileim:id/title_back", className="android.widget.TextView")
            # self.assertTrue(title_back.info['clickable'])
            if title_back.exists:
                title_back.click()
                time.sleep(1)
                title_back.click()
                time.sleep(1)
 
        logger.info('Exit --  MUAT:MobileImTest:test_SendMessage')
  
    def test_SendtakePhoto(self):
        logger.info('Enter -- MUAT:MobileImTest:test_SendtakePhoto')
        #点击消息栏
        tab_message = self.d(resourceId="com.alibaba.mobileim:id/tab_message_text", className="android.widget.ImageView")
        # self.assertTrue(tab_message.info['enabled'])
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
            title_back = self.d(resourceId="com.alibaba.mobileim:id/title_back", className="android.widget.TextView")
            # self.assertTrue(title_back.info['clickable'])
            if title_back.exists:
                title_back.click()
                time.sleep(1)
                title_back.click()
                time.sleep(1)
  
  
        logger.info('Exit --  MUAT:MobileImTest:test_SendtakePhoto')
 
    def test_SendCard(self):
        logger.info('Enter -- MUAT:MobileImTest:test_SendCard')
        #点击消息栏
        tab_message = self.d(resourceId="com.alibaba.mobileim:id/tab_message_text", className="android.widget.ImageView")
        self.assertTrue(tab_message.info['enabled'])
        if tab_message.info['clickable']:
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
                        # self.d(text=u"景止").click()
                        self.d(text=u'旺信团队').click()
#                         time.sleep(1)
#                         self.d(text=u"洗石").click()
#                         time.sleep(1)
#                         self.d(text=u"云渡").click()
#                         time.sleep(1)
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
            # chat_back = self.d(resourceId="com.alibaba.mobileim:id/chat_back", className="android.widget.TextView")
            # self.assertTrue(chat_back.info['enabled'])
            # if chat_back.info['clickable']:
            #     chat_back.click()
            #     time.sleep(1)
            title_back = self.d(resourceId="com.alibaba.mobileim:id/title_back", className="android.widget.TextView")
            # self.assertTrue(title_back.info['clickable'])
            if title_back.exists:
                title_back.click()
                time.sleep(1)
                title_back.click()
                time.sleep(1)
 
        logger.info('Exit --  MUAT:MobileImTest:test_SendCard')
 
    def test_SendPicture(self):
        logger.info('Enter -- MUAT:MobileImTest:test_SendPicture')
        #点击消息栏
        tab_message = self.d(resourceId="com.alibaba.mobileim:id/tab_message_text", className="android.widget.ImageView")
        self.assertTrue(tab_message.info['enabled'])
        if tab_message.info['clickable']:
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
            PlusButton = self.d(resourceId="com.alibaba.mobileim:id/reply_bar_expand", className="android.widget.CheckBox")
            if not PlusButton.exists:
                name = sys._getframe().f_code.co_name
                screen_shot.ScreenShot(self,name)
            self.assertTrue(PlusButton.exists)
            if PlusButton.exists:
                PlusButton.click()
                selectpic_btn = self.d(text=u"选择照片", className="android.widget.TextView")
                if not selectpic_btn.exists:
                    name = sys._getframe().f_code.co_name
                    screen_shot.ScreenShot(self,name)
                self.assertTrue(selectpic_btn.exists)
                if selectpic_btn.exists:
                    selectpic_btn.click()
                    time.sleep(1)
                    pic = self.d(resourceId="com.alibaba.mobileim:id/image_item", className="android.widget.ImageView")
                    if not pic.exists:
                        name = sys._getframe().f_code.co_name
                        screen_shot.ScreenShot(self,name)
                    self.assertTrue(pic.exists)
                    self.d(resourceId='com.alibaba.mobileim:id/image_check',packageName='com.alibaba.mobileim').click()
                        #点击完成， 发送图片
#                             self.d(resourceId="com.alibaba.mobileim:id/select_finish", className="android.widget.Button").click()
                    TitleBar=self.d(resourceId='android:id/pc_titlebar',packageName='com.alibaba.mobileim')
                    click_x=TitleBar.info['visibleBounds']['right']-30
                    click_y=TitleBar.info['visibleBounds']['bottom']+20
                    self.mouse.click(click_x, click_y, constants.MouseLeftKey)
                    
#                     select_finish = self.d(resourceId="com.alibaba.mobileim:id/finish", className="android.widget.Button")
#                     self.assertEqual(select_finish.info['text'], u'发送')
#                     select_finish.click()
                    time.sleep(2)
            #返回主界面
            title_back = self.d(resourceId="com.alibaba.mobileim:id/title_back", className="android.widget.TextView")
            # self.assertTrue(title_back.info['clickable'])
            if title_back.exists:
                title_back.click()
                time.sleep(1)
                title_back.click()
                time.sleep(1)
  
        logger.info('Exit --  MUAT:MobileImTest:test_SendPicture')
  
    def test_SendVoice(self):
        logger.info('Enter -- MUAT:MobileImTest:test_SendVoice')
  
        #点击消息栏
        tab_message = self.d(resourceId="com.alibaba.mobileim:id/tab_message_text", className="android.widget.ImageView")
        self.assertTrue(tab_message.info['enabled'])
        if tab_message.info['clickable']:
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
            title_back = self.d(resourceId="com.alibaba.mobileim:id/title_back", className="android.widget.TextView")
            # self.assertTrue(title_back.info['clickable'])
            if title_back.exists:
                title_back.click()
                time.sleep(1)
                title_back.click()
                time.sleep(1)
  
        logger.info('Exit --  MUAT:MobileImTest:test_SendVoice')
 
    def test_ModifyInfo(self):
        logger.info('Enter -- MUAT:MobileImTest:test_ModifyInfo')
        meButton=self.d(resourceId='com.alibaba.mobileim:id/tab_me_text')
        if meButton.exists:
            meButton.click()
            time.sleep(2)
#                 moreButton=self.d(text=u'更多',packageName='com.alibaba.mobileim')
#                 if moreButton.exists:
#                     moreButton.click()
#                     time.sleep(2)
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
                #切换输入法
#                 self.d.press(113,1)
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
                    #切换输入法
#                     self.d.press(113,1)
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
                    time.sleep(2)
                    self.assertEqual(profileAddress.info['text'], u'北京 北京')
                    profileAddress.click()
                    time.sleep(2)
                    self.d.click(tj1_x,tj1_y)
                    time.sleep(2)
                    self.d.click(tj2_x,tj2_y)
                    time.sleep(2)
                    self.assertEqual(profileAddress.info['text'], u'天津 天津')
                    time.sleep(2)
                        
                #更换头像
                self.d(resourceId='com.alibaba.mobileim:id/title_back').click()
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
                        time.sleep(2)
        logger.info('Exit -- MUAT:MobileImTest:test_ModifyInfo')
 
    def test_CheckInfo(self):
        logger.info('Enter -- MUAT:MobileImTest:test_CheckInfo')
  
        MobileimTitle=self.d(resourceId='android:id/pc_title')
        if not MobileimTitle.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(MobileimTitle.exists)
        if MobileimTitle.exists:
            MobileimTitle.click()
            logger.info('MobileimTitle is here')
            time.sleep(1)
  
        MessageButton=self.d(resourceId='com.alibaba.mobileim:id/tab_message_text')
        if not MessageButton.exists:
            name = sys._getframe().f_code.co_name
            screen_shot.ScreenShot(self,name)
        self.assertTrue(MessageButton.exists)
        if MessageButton.exists:
            MessageButton.click()
            logger.info('Message is here')
            time.sleep(1)
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
                time.sleep(1)
            GuyBtton=self.d(resourceId='com.alibaba.mobileim:id/friends_layout')
            self.assertTrue(GuyBtton.exists)
            if GuyBtton.exists:
                GuyBtton.click()
                logger.info('Guys is here')
                time.sleep(1)
            GruopButton=self.d(resourceId='com.alibaba.mobileim:id/tribe_layout')
            self.assertTrue(GruopButton.exists)
            if GruopButton.exists:
                GruopButton.click()
                logger.info('Gruop is here')
                time.sleep(1)
  
        CornerButton=self.d(resourceId='com.alibaba.mobileim:id/hangjia_iv')
        self.assertTrue(CornerButton.exists)
        if CornerButton.exists:
            CornerButton.click()
            logger.info('hangjia is here')
            CancelButton=self.d(text=u'取消',resourceId='com.alibaba.mobileim:id/button2')
            if CancelButton.exists:
                CancelButton.click()
                time.sleep(1)
            
#         MJX=self.d(resourceId='com.alibaba.mobileim:id/mjx_iv')
#         self.assertTrue(MJX.exists)
#         if MJX.exists:
#             MJX.click()
#             logger.info('MJX is here')
#             time.sleep(1)
#             self.d.press(0x42)
            
  
        MeButton=self.d(resourceId='com.alibaba.mobileim:id/tab_me_text')
        self.assertTrue(MeButton.exists)
        if MeButton.exists:
            MeButton.click()
            logger.info('Me is here')
            time.sleep(1)
  
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
        tab_me = self.d(resourceId="com.alibaba.mobileim:id/tab_me_text", className="android.widget.ImageView")
        # self.assertTrue(tab_me.info['clickable'])

#         if tab_me.exists:
#             tab_me.click()
#             time.sleep(1)
# 
#             myname = self.d(resourceId="com.alibaba.mobileim:id/title_text", className="android.widget.TextView")
#             self.assertEqual(myname.info['text'], 'tester_1')
# 
#             # setting button
#             setting_btn = self.d(resourceId="com.alibaba.mobileim:id/setting", className="android.widget.Button")
#             self.assertEqual(setting_btn.info['text'], u'设置')
# 
#             if setting_btn.exists:
#                 setting_btn.click()
#                 time.sleep(2)
# 
#             # account logout
#             logout_btn = self.d(resourceId='com.alibaba.mobileim:id/setting_logout')
#             self.assertEqual(logout_btn.info['text'], u'退出登录')
# 
#             if logout_btn.exists:
#                 logout_btn.click()
#                 time.sleep(1)
# 
#             exit_massege = self.d(resourceId="com.alibaba.mobileim:id/message", className="android.widget.TextView")
#             self.assertEqual(exit_massege.info['text'], u'退出后您将收不到新消息通知，是否确认退出？')
#             time.sleep(1)
#             if exit_massege.exists:
#                 self.d(resourceId="com.alibaba.mobileim:id/button1", className="android.widget.Button").click()
#                 time.sleep(2)
# 
#             accountClearButton = self.d(resourceId="com.alibaba.mobileim:id/accountClearButton", className="android.widget.TextView")
#             if not accountClearButton.exists:
#                 name = sys._getframe().f_code.co_name
#                 screen_shot.ScreenShot(self, name)
#                 time.sleep(3)
#             elif accountClearButton.exists:
#                 accountClearButton.click()
#                 time.sleep(1)

        closebtn = self.d(resourceId="android:id/pc_close", className="android.widget.ImageView", packageName="com.alibaba.mobileim")
        #self.assertTure(closebtn.exists)

        if closebtn.exists:
            logger.debug('click close button: (%s)' % (closebtn.info['packageName']))
            closebtn.click()
        #logger.info("EXIT -- MUAT:MobileImTest:close_mobileim")
        self.adb_tools.adb_shell('am force-stop com.alibaba.mobileim')

# -*- coding: utf-8 -*-

import os
import time

import constants
from logging import Logger

class Account(object):
    def __init__(self, device, logger=None):
        self.d          = device
        self.logger     = logger

        self.username_input = None
        self.passwd_input   = None
        self.login_btn      = None

        self.username_validation    = False

    def get_username_input(self):
        username_input = self.d(packageName='com.yunpc.yunosloginui', resourceId='com.yunpc.yunosloginui:id/username')
        if username_input.exists and username_input.count == 1:
            self.username_input = username_input

    def get_passwd_input(self):
        passwd_input = self.d(packageName='com.yunpc.yunosloginui', resourceId='com.yunpc.yunosloginui:id/password')
        if passwd_input.exists and passwd_input.count == 1:
            self.passwd_input = passwd_input

    def get_login_btn(self):
        login_btn = self.d(packageName='com.yunpc.yunosloginui', resourceId='com.yunpc.yunosloginui:id/btn_login')
        if login_btn.exists and login_btn.count == 1:
            self.login_btn = login_btn

    def input_username(self):
        self.get_username_input()
        if self.username_input:
            old_text = self.username_input.text
            if old_text == u'用户名':
                self.username_input.set_text(constants.TEST_USERNAME)
            elif old_text == constants.TEST_USERNAME:
                pass
            else:
                old_text_len = len(old_text)
                for i in range(old_text_len):
                    self.username_input.clear_text()

                while True:
                    if self.username_input.text == u'用户名':
                        break
                    else:
                        self.username_input.clear_text()

                self.username_input.set_text(constants.TEST_USERNAME)

            new_text = self.username_input.text
            if new_text == constants.TEST_USERNAME:
                self.username_validation = True
        else:
            if self.logger:
                self.logger.error('not found username input')

    def input_passwd(self):
        self.get_passwd_input()
        if self.passwd_input:
            self.passwd_input.set_text(constants.TEST_PASSWD)
        else:
            if self.logger:
                self.logger.error('not found password input')

    def click_login(self):
        self.get_login_btn()
        if self.login_btn:
            self.login_btn.click()

    def login(self):
        self.input_username()
        if self.username_validation == True:
            self.input_passwd()
            self.click_login()
        else:
            if self.logger:
                self.logger.error('user name not validation')

    def logout(self):
        if self.logger:
            Logger.warning('tobe implement')

    def reboot(self):
        if self.logger:
            Logger.warning('tobe implement')

    def shutdown(self):
        if self.logger:
            Logger.warning('tobe implement')

    def sleep(self):
        if self.logger:
            Logger.info('sleep device')
        self.d.sleep()

    def wakeup(self):
        if self.logger:
            Logger.info('wakeup device')
        self.d.wakeup()

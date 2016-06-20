# -*- coding:utf-8 -*-

'''
This module used to parse/generate the command message from websocket, eg:
[
{"type":"data", "name":"http://10.32.168.29/vm_data_typeperf.py", "start_time":"2014-9-15 17:30:00", "end_time":"2014-9-16 17:30:00", "parameters":{"download_url":["http://10.32.168.29/counters.txt"],"config_file":["counters.txt"], "counter_type":"system"}, "rate":"1"},
{"type":"scenario", "name":"http://10.32.168.29/vm_scenario_video_ie_scroll.py", "start_time":"2014-9-15 17:30:00", "end_time":"2014-9-16 17:30:00", "parameters":{"video_url":["http://www.iqiyi.com/v_19rrhifb4k.html?src=focustext_1_20130410_6"], "video_full":"yes", "scroll_direction":["vertical"], "scroll_speed":["normal"]}, "rate":"0"}
]
'''

import os
import re
import shutil
import logging

import json
import urllib

import constants
from parse_parameters import ParseParameters

logger = logging.getLogger(constants.LOGGER_CLIENT_MAIN)

class Command():
    TYPE = 'type'
    NAME = 'name'
    START_TIME = 'start_time'
    END_TIME = 'end_time'
    PARAMETERS = 'parameters'
    RATE = 'rate'

    TYPE_SCENARIO = 'scenario'
    TYPE_DATA     = 'data'
    DEBUG_MODE    = "debug_mode"

    # for security only the official server address are available
    #URL_VALIDATE = re.compile(r'http://3p.taobao.net/.*', re.I)
    URL_VALIDATE = re.compile(r'http://.*', re.I)

    def __init__(self, command):
        self.command = command
        self._parameters = None
        self._debugmode = True
        self._validation_command = False
        

    def validate_command(self):
        if self.command and isinstance(self.command, dict):
            self._validation_command = True
        else:
            logger.error('command not valid: (%s)' % (self.command))

        if self._validation_command:
            checks = [Command.TYPE, Command.NAME, 
                      Command.START_TIME, Command.END_TIME, 
                      Command.PARAMETERS, Command.RATE, Command.DEBUG_MODE]
            # check integrity of item
            for check in checks:
                if not self.command.has_key(check):
                    self._validation_command = False
                    logger.error('command (%s) does not has: %s' % (Command, check))
                    break
            # load parameters
            if self._validation_command:
                self._parameters = ParseParameters(self.command[Command.PARAMETERS])
                self._debugmode = self.command[Command.DEBUG_MODE]

    @property
    def command_type(self):
        if self.command.has_key(Command.TYPE):
            return self.command[Command.TYPE]
        else:
            return None

    @property
    def name(self):
        if self.command.has_key(Command.NAME):
            return self.command[Command.NAME]
        else:
            return None
    
    @property
    def start_time(self):
        if self.command.has_key(Command.START_TIME):
            return self.command[Command.START_TIME]
        else:
            return None
        
    @property
    def end_time(self):
        if self.command.has_key(Command.END_TIME):
            return self.command[Command.END_TIME]
        else:
            return None

    @property
    def parameters(self):
        if self._parameters:
            return self._parameters
        else:
            return None

    @property
    def rate(self):
        if self.command.has_key(Command.RATE):
            return self.command[Command.RATE]
        else:
            return None

    @property
    def validation_command(self):
        return self._validation_command 

    def __str__(self):
        if self._validation_command: 
            return 'command-type:%s, name:%s, start_time:%s, end_time:%s, rate:%s, debug_mode:%s' % (
                            self.command[Command.TYPE],
                            self.command[Command.NAME],
                            self.command[Command.START_TIME],
                            self.command[Command.END_TIME],
                            self.command[Command.RATE],
                            self.command[Command.DEBUG_MODE])
        else:
            return 'command-not-validation'

class ParseCommand():
    def __init__(self, command):
        self.command_list = command
        self.scenario_list = []
        self.data_list = []
        self.download_list = []
        self.validation_commandlist = None
        self.validation_download = None

    def parse_command(self):
        # command_list must be a list, but an empty list is acceptable
        if not isinstance(self.command_list, list):
            logger.error('command is not a list: %s' % (self.command_list))
            self.validation_commandlist = False
        else:
            self.validation_commandlist = True
            self.validate_commandlist()

    def validate_commandlist(self):
        for li in self.command_list:
            command = Command(li)
            command.validate_command()
            
            # add command into data_list or scenario_list
            if command.validation_command:
                if command.command_type == Command.TYPE_SCENARIO:
                    self.scenario_list.append(command)
                elif command.command_type == Command.TYPE_DATA:
                    self.data_list.append(command)
                else:
                    logger.error('command type not recgonized: %s' % (command))
            else:
                break

    def download(self):
        # create download list (name and parameters item of scenario_list/data_list)
        for li in self.scenario_list, self.data_list:
            for command in li:
                # add NAME item into download list
                if Command.URL_VALIDATE.match(command.name):
                    self.download_list.append(command.name)

                # parameters should be a list, if the url match the regulation will be append to download list
                if command.parameters:
                    download_url = command.parameters.download_url
                    if download_url and isinstance(download_url, list):
                        for url in download_url:
                            if Command.URL_VALIDATE.match(url):
                                self.download_list.append(url)


        # download the file
        for download_url in self.download_list:
            try:
                filename = urllib.unquote(download_url).decode('utf-8').split('/')[-1]
                if not constants.DEBUG:
                    logger.debug('Start Download file (%s) from url: %s' % (filename,download_url))
                    urllib.urlretrieve(download_url, filename)
                else:
                    if constants.SCRIPT_DOWNLOAD_INTERNET:
                        debug_url = "%s/%s" % (constants.SCRIPT_DOWNLOAD_PATH, filename)
                        logger.debug('Start Download file (%s) from debug url: %s' % (filename,debug_url))
                        urllib.urlretrieve(debug_url, filename)
                    else:
                        file_src  = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), constants.SCRIPT_DOWNLOAD_PATH), filename)
                        logger.debug('Start Download file (%s) from local file: %s' % (filename,file_src))
                        shutil.copy(file_src, filename)
            except:
                logger.error('Download file failed: %s ' % (filename))

        # check the all download file exist
        self.validation_download = True
        self.check_download()

    def check_download(self):
        for download_url in self.download_list:
            try:
                filename = urllib.unquote(download_url).decode('utf-8').split('/')[-1]
                if not os.path.exists(filename):
                    self.validation_download = False
                    logger.error('Download file not exist %s' % (filename))
                    break
            except:
                logger.error('check download file failed')

    def is_ready(self):
        return self.validation_commandlist and self.validation_download

class GenerateCommand():
    AVAILABLE_ITEMS    = [
                            Command.TYPE,
                            Command.NAME,
                            Command.START_TIME,
                            Command.END_TIME,
                            Command.PARAMETERS,
                            Command.RATE,
                            Command.DEBUG_MODE                            
                          ]

    def __init__(self):
        self._command = []

    def add_command(self, **kwargs):
        command = {}
        for key in kwargs:
            if key in GenerateCommand.AVAILABLE_ITEMS:
                command[key] = kwargs[key]

        # check the validation of the command
        c = Command(command)
        c.validate_command()

        if c.validation_command:
            self._command.append(command)

    @property
    def command(self):
        return self._command


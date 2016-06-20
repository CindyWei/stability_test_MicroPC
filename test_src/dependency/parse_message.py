# -*- coding:utf-8 -*-

'''
This module used to parse the message from websocket, eg:
{
    "action": "start",
    "test_id": "20140722_107",
    "case_id": "107",
    "test_type": "performance",
    "command": [
        {"type":"data", "name":"http://10.32.168.29/vm_data_typeperf.py", "start_time":"2014-9-15 17:30:00", "end_time":"2014-9-16 17:30:00", "parameters":{"download_url":["http://10.32.168.29/counters.txt"],"config_file":["counters.txt"], "counter_type":"system"}, "rate":"1"},
        {"type":"scenario", "name":"http://10.32.168.29/vm_scenario_video_ie_scroll.py", "start_time":"2014-9-15 17:30:00", "end_time":"2014-9-16 17:30:00", "parameters":{"video_url":["http://www.iqiyi.com/v_19rrhifb4k.html?src=focustext_1_20130410_6"], "video_full":"yes", "scroll_direction":["vertical"], "scroll_speed":["normal"]}, "rate":"0"}
    ]
}
'''

import json
import logging
import constants

# Init logger
logger = logging.getLogger(constants.LOGGER_CLIENT_MAIN)

class ParseMessage():
    MESSAGE_ACTION   = 'action'
    MESSAGE_TESTID   = 'test_id'
    MESSAGE_CASEID   = 'case_id'
    MESSAGE_TESTTYPE = 'test_type'
    MESSAGE_COMMAND  = 'command'

    def __init__(self, message):
        self.validation_message = False

        # Decode json format message
        try:
            self.message = json.loads(message)
            self.validation_message = True
            self.validate_message()
        except (TypeError, ValueError) as err:
            logger.error('load message error, not json formatted: %s' % (message))

    # validate message
    def validate_message(self):
        checks = [ParseMessage.MESSAGE_TESTID, ParseMessage.MESSAGE_CASEID, 
                  ParseMessage.MESSAGE_ACTION]
        for check in checks:
            if not self.message.has_key(check):
                logger.error('message does not have item: %s' % (check))
                self.validation_message = False
                break

        if self.validation_message:
            if self.message[ParseMessage.MESSAGE_ACTION] == 'start':
                start_checks = [ParseMessage.MESSAGE_COMMAND, ParseMessage.MESSAGE_TESTTYPE] 
                for check in start_checks:
                    if not self.message.has_key(check):
                        logger.error('start message does not have item: %s' % (check))
                        self.validation_message = False
                        break
            elif self.message[ParseMessage.MESSAGE_ACTION] == 'stop':
                pass
            else:
                logger.error('message does not support this action: %s' % (self.message[ParseMessage.MESSAGE_ACTION]))
                self.validation_message = False

    def is_ready(self):
        return self.validation_message

    @property
    def action(self):
        if self.validation_message and self.message.has_key(ParseMessage.MESSAGE_ACTION):
            return self.message[ParseMessage.MESSAGE_ACTION]
        else:
            return ""

    @property
    def testid(self):
        if self.validation_message and self.message.has_key(ParseMessage.MESSAGE_TESTID):
            return self.message[ParseMessage.MESSAGE_TESTID]
        else:
            return ""

    @property
    def caseid(self):
        if self.validation_message and self.message.has_key(ParseMessage.MESSAGE_CASEID):
            return self.message[ParseMessage.MESSAGE_CASEID]
        else:
            return ""

    @property
    def testtype(self):
        if self.validation_message and self.message.has_key(ParseMessage.MESSAGE_TESTTYPE):
            return self.message[ParseMessage.MESSAGE_TESTTYPE]
        else:
            return ""

    @property
    def command(self):
        if self.validation_message and self.message.has_key(ParseMessage.MESSAGE_COMMAND):
            return self.message[ParseMessage.MESSAGE_COMMAND]
        else:
            return ""

    @property
    def json_message(self):
        if self.validation_message:
            return self.message
        else:
            return ""

class GenerateMessage():
    AVAILABLE_ITEMS    = [
                            ParseMessage.MESSAGE_ACTION,
                            ParseMessage.MESSAGE_TESTID,
                            ParseMessage.MESSAGE_CASEID,
                            ParseMessage.MESSAGE_TESTTYPE,
                            ParseMessage.MESSAGE_COMMAND
                          ]

    def __init__(self, **kwargs):
        self._message = ''
        message = {}
        for key in kwargs:
            if key in GenerateMessage.AVAILABLE_ITEMS:
                message[key] = kwargs[key]
        self._message = json.dumps(message)

        # check the validation of the message
        m = ParseMessage(self._message)

        if not m.is_ready:
            self._message = ''

    @property
    def message(self):
        return self._message

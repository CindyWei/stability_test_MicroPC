# -*- coding:utf-8 -*-

'''
This module used to parse/generate the parameters, eg:
    {"download_url":["http://10.32.168.29/counters.txt"],"config_file":["counters.txt"], "counter_type":"system"}
'''

class ParseParameters():
    DOWNLOAD_URL        = 'download_url'
    VIDEO_URL           = 'video_url'
    VIDEO_FULL          = 'video_full'
    VIDEO_REDIRECTION   = 'video_redirection'
    DRAG_DIRECTION      = 'drag_direction'
    DRAG_SPEED          = 'drag_speed'
    SCROLL_DIRECTION    = 'scroll_direction'
    SCROLL_SPEED        = 'scroll_speed'
    CONFIG_FILE         = 'config_file'
    COUNTER_TYPE        = 'counter_type'
    REQUEST_KEYS        = 'request_keys'
    CHAT_TYPE           = 'chat_type'
    CHAT_ROLE           = 'chat_role'
    CHAT_NAME           = 'chat_name'
    CHAT_IP             = 'chat_ip'
    SERIAL_NUMBER       = 'serial_number'
    WINDOW_STATE        = 'window_state'
    SPECIAL_KEYS        = 'special_keys'

    def __init__(self, parameters):
        self.params = parameters
        self.validation_parameters = False
        if self.params and isinstance(self.params, dict):
            self.validation_parameters = True

    @property
    def download_url(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.DOWNLOAD_URL):
            return self.params[ParseParameters.DOWNLOAD_URL]
        else:
            return None

    @property
    def video_url(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.VIDEO_URL):
            return self.params[ParseParameters.VIDEO_URL]
        else:
            return None

    @property
    def video_redirection(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.VIDEO_REDIRECTION):
            return self.params[ParseParameters.VIDEO_REDIRECTION]
        else:
            return None

    @property
    def video_full(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.VIDEO_FULL):
            return self.params[ParseParameters.VIDEO_FULL]
        else:
            return None

    @property
    def drag_direction(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.DRAG_DIRECTION):
            return self.params[ParseParameters.DRAG_DIRECTION]
        else:
            return None

    @property
    def drag_speed(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.DRAG_SPEED):
            return self.params[ParseParameters.DRAG_SPEED]
        else:
            return None

    @property
    def scroll_direction(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.SCROLL_DIRECTION):
            return self.params[ParseParameters.SCROLL_DIRECTION]
        else:
            return None

    @property
    def scroll_speed(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.SCROLL_SPEED):
            return self.params[ParseParameters.SCROLL_SPEED]
        else:
            return None

    @property
    def config_file(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.CONFIG_FILE):
            return self.params[ParseParameters.CONFIG_FILE]
        else:
            return None

    @property
    def counter_type(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.COUNTER_TYPE):
            return self.params[ParseParameters.COUNTER_TYPE]
        else:
            return None

    @property
    def request_keys(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.REQUEST_KEYS):
            return self.params[ParseParameters.REQUEST_KEYS]
        else:
            return None

    @property
    def chat_type(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.CHAT_TYPE):
            return self.params[ParseParameters.CHAT_TYPE]
        else:
            return None

    @property
    def chat_role(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.CHAT_ROLE):
            return self.params[ParseParameters.CHAT_ROLE]
        else:
            return None

    @property
    def chat_name(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.CHAT_NAME):
            return self.params[ParseParameters.CHAT_NAME]
        else:
            return None

    @property
    def chat_ip(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.CHAT_IP):
            return self.params[ParseParameters.CHAT_IP]
        else:
            return None

    @property
    def serial_number(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.SERIAL_NUMBER):
            return self.params[ParseParameters.SERIAL_NUMBER]
        else:
            return None

    @property
    def window_state(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.WINDOW_STATE):
            return self.params[ParseParameters.WINDOW_STATE]
        else:
            return None

    @property
    def special_keys(self):
        if self.validation_parameters and self.params.has_key(ParseParameters.SPECIAL_KEYS):
            return self.params[ParseParameters.SPECIAL_KEYS]
        else:
            return None

class GenerateParameters():
    AVAILABLE_PARAMS    = [
                            ParseParameters.DOWNLOAD_URL,
                            ParseParameters.VIDEO_URL,          ParseParameters.VIDEO_FULL,     ParseParameters.VIDEO_REDIRECTION,
                            ParseParameters.DRAG_DIRECTION,     ParseParameters.DRAG_SPEED,
                            ParseParameters.SCROLL_DIRECTION,   ParseParameters.SCROLL_SPEED,
                            ParseParameters.CONFIG_FILE,        ParseParameters.COUNTER_TYPE,   ParseParameters.REQUEST_KEYS,
                            ParseParameters.CHAT_TYPE,          ParseParameters.CHAT_ROLE,      ParseParameters.CHAT_NAME,      ParseParameters.CHAT_IP,
                            ParseParameters.SERIAL_NUMBER,      ParseParameters.WINDOW_STATE,
                            ParseParameters.SPECIAL_KEYS
                          ]

    def __init__(self, **kwargs):
        self._params = {}
        for key in kwargs:
            print key
            if key in GenerateParameters.AVAILABLE_PARAMS:
                print key
                self._params[key] = kwargs[key]

    @property
    def parameters(self):
        return self._params

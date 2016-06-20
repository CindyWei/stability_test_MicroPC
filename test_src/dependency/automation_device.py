# -*- coding: utf-8 -*-

import os

import singleton

class AutomationDevice(singleton.Singleton):
    def init(self, *args, **kwargs):
        self.d = None
        self.is_intel = None
        try:
            if kwargs and 'serial_number' in kwargs:
                self.is_intel = True
                from uiautomator import Device
                self.d = Device(kwargs['serial_number'])
            else:
                self.is_intel = False
                from uiautomator import device as d
                self.d = d
        except Exception as e:
            print(e)

    def get_device(self):
        return self.d

    def stop_device(self):
        if self.d:
            self.d.server.stop()

    def start_device(self):
        pass
		
    def is_intel_device(self):
	    return self.is_intel

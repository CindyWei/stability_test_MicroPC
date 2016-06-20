# -*- coding: utf-8 -*-
import constants
from adb_tools import AdbTools


class AdbMouse():
    def __init__(self):
        self.adb_tools          = AdbTools()
        self.gesturehelper      = '/system/bin/gesturehelper'
        
    def movetobasepoint(self):
        self.adb_tools.adb_devices()
        if self.adb_tools.devices:
            cmd = "%s mousemove %d %d" % (self.gesturehelper, -1920, -1080)
            self.adb_tools.adb_shell(cmd)
    
    def move(self, x, y):
        self.adb_tools.adb_devices()
        if self.adb_tools.devices:
            cmd = "%s mousemove %d %d" % (self.gesturehelper, x, y)
            self.adb_tools.adb_shell(cmd)
            
    def pressmove(self, x, y, rel_x, rel_y, keyType):
        self.movetobasepoint()
        self.move(x, y)
        if self.adb_tools.devices:
            cmd = "%s mousepressmove %d %d %d" % (self.gesturehelper, rel_x, rel_y, keyType)
            self.adb_tools.adb_shell(cmd)
    
    def click(self, x, y, keyType):
        self.movetobasepoint()
        self.move(x, y)
        if self.adb_tools.devices:
            cmd = "%s mouseclick %d" % (self.gesturehelper, keyType)
            self.adb_tools.adb_shell(cmd)
    
    def doubleclick(self, x, y, keyType):
        self.movetobasepoint()
        self.move(x, y)
        if self.adb_tools.devices:
            cmd = "%s mousedoubleclick %d" % (self.gesturehelper, keyType)
            self.adb_tools.adb_shell(cmd)
            
    def wheel(self, x, y, rel, repeatnum, speed):
        self.movetobasepoint()
        self.move(x, y)
        if self.adb_tools.devices:
            cmd = "%s mousewheel %d %d %d" % (self.gesturehelper, rel, repeatnum, speed)
            self.adb_tools.adb_shell(cmd)
        
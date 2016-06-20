# -*- coding: utf-8 -*-

import os
import re
import subprocess
import platform
import constants

class AdbTools():
    def __init__(self):
        self.adb        = constants.ADB

        self._availalbe         = False
        self._devices           = []
        self._devices_detail    = {}

    def check_available(self):
        self._available = False
        # check adb command
        cmd = 'WHERE /Q %s' % (self.adb)
        if platform.system() == 'Linux':
            cmd = 'sudo WHERE /Q %s' % (self.adb)
        result = subprocess.call(cmd, shell=True)
        if not result:
            self._available = True

    @property
    def available(self):
        self.check_available()
        return self._available

    def adb_start_server(self):
        cmd = '%s start-server' % (self.adb)
        if platform.system() == 'Linux':
            cmd = 'sudo %s start-server' % (self.adb)
        subprocess.call(cmd, shell=True)

    def adb_kill_server(self):
        cmd = '%s kill-server' % (self.adb)
        if platform.system() == 'Linux':
            cmd = 'sudo %s kill-server' % (self.adb)
        subprocess.call(cmd, shell=True)

    def adb_devices(self):
        self._devices = []
        re_dev = re.compile(r'^(\w+).*device$')

        # check adb devices
        cmd = '%s devices' % (self.adb)
        if platform.system() == 'Linux':
            cmd = 'sudo %s devices' % (self.adb)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while True:
            line = p.stdout.readline()
            if not line:
                break
            re_dev_se = re_dev.search(line.rstrip())
            if re_dev_se:
                device = re_dev_se.groups()[0]
                if device:
                    self._devices.append(device)
        p.wait()

        #print('adb devices found: %s' % (self._devices))

        self._devices_detail = {}
        # check adb devices detail infomation
        cmd = '%s devices -l' % (self.adb)
        if platform.system() == 'Linux':
            cmd = 'sudo %s devices -l' % (self.adb)
        re_detail = re.compile(r'^(\w+).*device product:(.*) model:(.*) device:(.*)$')
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while True:
            line = p.stdout.readline()
            if not line:
                break
            re_detail_se = re_detail.search(line.rstrip())
            if re_detail_se:
                detail = re_detail_se.groups()
                if detail[0] in self._devices:
                    self._devices_detail[detail[0]] = detail[1:]
        p.wait()

    @property
    def devices(self):
        return self._devices

    @property
    def devices_detail(self):
        return self._devices_detail

    def adb_connect(self, **kwargs):
        try:
            if kwargs and 'serial_number' in kwargs:
                cmd = '%s connect %s' % (self.adb, kwargs['serial_number'])
                if platform.system() == 'Linux':
                    cmd = 'sudo %s connect %s' % (self.adb, kwargs['serial_number'])
                p = subprocess.Popen(cmd, shell=True)
                p.wait()
        except:
            pass
        else:
            if kwargs and 'serial_number' in kwargs:
                print('adb connect %s' % (kwargs['serial_number']))

    def adb_shell(self, command, **kwargs):
        ret = (None, None)
        try:
            if kwargs and 'serial_number' in kwargs:
                adb_special = '%s -s %s' % (self.adb, kwargs['serial_number'])
            elif len(self._devices) <= 1:
                adb_special = '%s' % (self.adb)
            else:
                print('please specify the device')
                raise()

            need_ret = False
            if kwargs and 'need_ret' in kwargs:
                need_ret = kwargs['need_ret']
        except:
            pass
        else:
            cmd = '%s shell %s' % (adb_special, command)
            if platform.system() == 'Linux':
                cmd = 'sudo %s shell %s' % (adb_special, command)
            if need_ret:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                ret = p.communicate()
            else:
                p = subprocess.Popen(cmd, shell=True)
                p.wait()

            return ret

    def adb_reboot(self, **kwargs):
        try:
            if kwargs and 'serial_number' in kwargs:
                adb_special = '%s -s %s' % (self.adb, kwargs['serial_number'])
            elif len(self._devices) <= 1:
                adb_special = '%s' % (self.adb)
            else:
                print('please specify the device')
                raise()
        except:
            pass
        else:
            print('reboot box ... ...')
            cmd = '%s reboot' % (adb_special)
            if platform.system() == 'Linux':
                cmd = 'sudo %s reboot' % (adb_special)
            p = subprocess.Popen(cmd, shell=True)
            p.wait()

    def adb_remount(self, **kwargs):
        try:
            if kwargs and 'serial_number' in kwargs:
                adb_special = '%s -s %s' % (self.adb, kwargs['serial_number'])
            elif len(self._devices) <= 1:
                adb_special = '%s' % (self.adb)
            else:
                print('please specify the device')
                raise()
        except:
            pass
        else:
            cmd = '%s remount' % (adb_special)
            if platform.system() == 'Linux':
                cmd = 'sudo %s remount' % (adb_special)
            p = subprocess.Popen(cmd, shell=True)
            p.wait()

    def adb_chmod(self, mode, filename, **kwargs):
        try:
            if kwargs and 'serial_number' in kwargs:
                adb_special = '%s -s %s' % (self.adb, kwargs['serial_number'])
            elif len(self._devices) <= 1:
                adb_special = '%s' % (self.adb)
            else:
                print('please specify the device')
                raise()
        except:
            pass
        else:
            cmd = '%s shell chmod %s %s' % (adb_special, mode, filename)
            if platform.system() == 'Linux':
                cmd = 'sudo %s shell chmod %s %s' % (adb_special, mode, filename)
            p = subprocess.Popen(cmd, shell=True)
            p.wait()

    def adb_rm(self, filename, **kwargs):
        try:
            if kwargs and 'serial_number' in kwargs:
                adb_special = '%s -s %s' % (self.adb, kwargs['serial_number'])
            elif len(self._devices) <= 1:
                adb_special = '%s' % (self.adb)
            else:
                print('please specify the device')
                raise()
        except:
            pass
        else:
            cmd = '%s shell rm %s' % (adb_special, filename)
            if platform.system() == 'Linux':
                cmd = 'sudo %s shell rm %s' % (adb_special, filename)
            p = subprocess.Popen(cmd, shell=True)
            p.wait()

    def adb_getprop(self, name, **kwargs):
        try:
            if kwargs and 'serial_number' in kwargs:
                adb_special = '%s -s %s' % (self.adb, kwargs['serial_number'])
            elif len(self._devices) <= 1:
                adb_special = '%s' % (self.adb)
            else:
                print('please specify the device')
                raise()
        except:
            return ''
        else:
            cmd = '%s shell getprop %s' % (adb_special, name)
            if platform.system() == 'Linux':
                cmd = 'sudo %s shell getprop %s' % (adb_special, name)
            value = ''
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            while True:
                line = p.stdout.readline()
                if not line:
                    break
                else:
                    value = line.rstrip()
                    break
            p.wait()
            return value

    def adb_setprop(self, name, value, **kwargs):
        try:
            if kwargs and 'serial_number' in kwargs:
                adb_special = '%s -s %s' % (self.adb, kwargs['serial_number'])
            elif len(self._devices) <= 1:
                adb_special = '%s' % (self.adb)
            else:
                print('please specify the device')
                raise()
        except:
            pass
        else:
            cmd = '%s shell setprop %s %s' % (adb_special, name, value)
            if platform.system() == 'Linux':
                cmd = 'sudo %s shell setprop %s %s' % (adb_special, name, value)
            p = subprocess.Popen(cmd, shell=True)
            p.wait()

    def adb_pull(self, src, dest, **kwargs):
        try:
            if kwargs and 'serial_number' in kwargs:
                adb_special = '%s -s %s' % (self.adb, kwargs['serial_number'])
            elif len(self._devices) <= 1:
                adb_special = '%s' % (self.adb)
            else:
                print('please specify the device')
                raise()
        except:
            pass
        else:
            if os.path.exists(dest):
                if os.path.isdir(dest):
                    shutil.rmtree(dest)
                else:
                    os.remove(dest)

            cmd = '%s pull %s %s' % (adb_special, src, dest)
            if platform.system() == 'Linux':
                cmd = 'sudo %s pull %s %s' % (adb_special, src, dest)
            print cmd
            p = subprocess.Popen(cmd, shell=True)
            p.wait()

    def adb_push(self, src, dest, **kwargs):
        try:
            if kwargs and 'serial_number' in kwargs:
                adb_special = '%s -s %s' % (self.adb, kwargs['serial_number'])
            elif len(self._devices) <= 1:
                adb_special = '%s' % (self.adb)
            else:
                print('please specify the device')
                raise()
        except:
            pass
        else:
            if os.path.exists(src):
                if os.path.isfile(src):
                    cmd = '%s push %s %s' % (adb_special, src, dest)
                    if platform.system() == 'Linux':
                        cmd = 'sudo %s push %s %s' % (adb_special, src, dest)
                    p = subprocess.Popen(cmd, shell=True)
                    p.wait()
                else:
                    print('push file error: (%s) not a file' % (src))
            else:
                print('push file error: (%s) not exist' % (src))
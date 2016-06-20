# -*- coding: utf-8 -*-
import os
import threading
import subprocess

import constants
from non_block_stream_reader import NonBlockStreamReader

class AdbLog(threading.Thread):
    MODE_RE                           = 0x01
    MODE_NEED_DETECT                  = 0x10
    MODE_NEED_CONTINUE                = 0x20

    def __init__(self, mode, wanted_re, detect_re=None, logger=None, serial_number=None):
        super(AdbLog, self).__init__()
        self.adb            = constants.ADB

        self.mode           = mode
        self.need_detect    = True if (self.mode & AdbLog.MODE_NEED_DETECT) else False
        self.need_continue  = True if (self.mode & AdbLog.MODE_NEED_CONTINUE) else False
        self.wanted_re      = wanted_re
        self.detect_re      = detect_re
        self.logger         = logger
        self.serial_number  = serial_number

        self.detect_found   = False if self.need_detect else True
        self.p              = None
        self._result        = []
        self._running_status= True

    def clear(self):
        if self.serial_number:
            adb_special = '%s -s %s' % (self.adb, self.serial_number)
        else:
            adb_special = '%s' % (self.adb)

        cmd = '%s logcat -c' % (adb_special)
        os.popen(cmd)

    def run(self):
        if self.serial_number:
            adb_special = '%s -s %s' % (self.adb, self.serial_number)
        else:
            adb_special = '%s' % (self.adb)

        cmd = '%s logcat -v time' % (adb_special)
        self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        nb_reader = NonBlockStreamReader(self.p.stdout)
        while True:
            if not self._running_status:
                if self.logger:
                    self.logger.debug('detect running_status set to False')
                break

            line = nb_reader.readline(constants.ADBLOG_READLINE_TIMEOUT)

            if not line:
                continue
            else:
                line = line.rstrip()

            if self.detect_found:
                wanted_re_se = self.wanted_re.search(line)
                if wanted_re_se:
                    if self.logger:
                        #self.logger.debug('wanted_re found: (%s)' % (line))
                        pass
                    self._result.append(wanted_re_se.groups())
                    if not self.need_continue:
                        break
                    else:
                        continue
                else:
                    continue

            if self.need_detect and not self.detect_found:
                # find detect
                detect_re_se = self.detect_re.search(line)
                if detect_re_se:
                    if self.logger:
                        self.logger.debug('detect_re found: (%s)' % (line))
                    self._result.append(detect_re_se.groups())
                    self.detect_found = True

        if self.p:
            self.p.terminate()
            self.p.wait()

    def stop_log(self):
        self._running_status = False
        if self.logger:
            self.logger.debug('stop adb log threading')

    @property
    def result(self):
        return self._result

# -*- coding:utf-8 -*-

"""
process monitor thread used to receive stop signal, through Queue/Pipe
"""

import os
import sys
import time
import threading

class ProcessMonitor(threading.Thread):
    def __init__(self, qin=None, logger=None, thread_num=0, timeout=1.0):
        super(ProcessMonitor, self).__init__()
        self.qin = qin
        self.logger = logger
        self._running_status = True
        
        self.thread_num = thread_num
        self.stopped = False
        self.timeout = timeout

    def run(self):
        def target_func():
            self.logger.debug('ProcessMonitor Start')
            while True:
                if self.qin:
                    values = self.qin.get(True)
    
                    if values and type(values) == list:
                        for value in values:
                            if value == 'stop-%s' % (os.getpid()):
                                if self.logger:
                                    self.logger.debug('receive %s signal' % (value))
                                self._running_status = False
                                values.remove(value)
                                break
    
                        if values:
                            self.qin.put(values)
    
                        if self._running_status == False:
                            break
                        else:
                            time.sleep(1)
                    else:
                        self.logger.warning('(%s) not a good signal' % (value))
                        self.qin.put(value)
                        time.sleep(1)
                else:
                    line = sys.stdin.readline()
                    if line.rstrip() == 'stop':
                        self._running_status = False
                        break
                    
        subthread = threading.Thread(target=target_func, args=())
        subthread.setDaemon(True)
        subthread.start()

        while not self.stopped:
            subthread.join(self.timeout)
        self.logger.debug('ProcessMonitor Stop')
        
    def stop(self):
        self.stopped = True
    
    def isStopped(self):
        return self.stopped

    @property
    def running_status(self):
        return self._running_status

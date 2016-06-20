#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import struct
import cPickle
import threading
from SocketServer import ThreadingTCPServer, StreamRequestHandler

import logging
import logging.handlers
import singleton
import constants

class LoggerClient(singleton.Singleton):
    # overwrite Singleton init function, it will be run only one time
    def init(self, name=constants.LOGGER_CLIENT_MAIN):
        # main logger
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.propagate = 0
        self.logger.setLevel(logging.DEBUG)

        # set socket handle
        self.sh = logging.handlers.SocketHandler(constants.LOGGER_SERVER_IP, constants.LOGGER_SERVER_PORT)
        self.sh.setLevel(logging.DEBUG)

        # set console handle
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)

        # set logger format
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s")
        self.sh.setFormatter(formatter)
        self.ch.setFormatter(formatter)

        # add handle to logger
        #logger.addHandler(fh)
        self.logger.addHandler(self.sh)
        self.logger.addHandler(self.ch)

    def __init__(self, name=constants.LOGGER_CLIENT_MAIN):
        pass

    def close_sh(self):
        if self.sh:
            self.sh.close()

class LogRequestHandler(StreamRequestHandler):
    def handle(self):
        while True:
            try:
                chunk = self.connection.recv(4)
            except Exception as e:
                print e
                break
            if len(chunk) < 4:
                break
            slen = struct.unpack(">L", chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)

            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data):
        return cPickle.loads(data)

    def handleLogRecord(self, record):
        logger = logging.getLogger(constants.LOGGER_SERVER_NAME)
        logger.handle(record)

class LoggerServer(threading.Thread):
    def __init__(self):
        super(LoggerServer, self).__init__()
        self.server = None
        self.mh     = None
        self.omh    = None

    def run(self):
        # check logger path
        logger_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), constants.LOGGER_DIR)
        logger_online_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), constants.LOGGER_ONLINE_DIR)

        if os.path.exists(logger_path):
            if not os.path.isdir(logger_path):
                os.remove(logger_path)
                os.mkdir(logger_path)
        else:
            os.mkdir(logger_path)

        logger_file = os.path.join(logger_path, constants.LOGGER_FILE)
        logger_online_file = os.path.join(logger_online_path, constants.LOGGER_ONLINE_FILE)

        # rotating file handler
        #rh = logging.handlers.RotatingFileHandler(logger_file,
        #                              maxBytes = constants.LOGGER_FILE_MAX_BYTE,
        #                              backupCount = constants.LOGGER_FILE_BACKUP_COUNT)
        #rh.setLevel(logging.DEBUG)
        # RotatingFileHandler failed sometimes because of os.rename(), so change to FileHandler, and maintain the log files manually
        if os.path.exists(logger_file):
            logger_file_stat = os.stat(logger_file)
            if logger_file_stat.st_size > constants.LOGGER_FILE_MAX_BYTE:
                file_list = os.listdir(logger_path)
                for count in range(constants.LOGGER_FILE_BACKUP_COUNT, 0, -1):
                    if os.path.exists('%s.%s' % (logger_file, count)):
                        if count == constants.LOGGER_FILE_BACKUP_COUNT:
                            os.remove('%s.%s' % (logger_file, count))
                        else:
                            os.rename('%s.%s' % (logger_file, count), '%s.%s' % (logger_file, count + 1))
                os.rename(logger_file, '%s.%s' % (logger_file, str(1)))

        fh = logging.FileHandler(logger_file)
        fh.setLevel(logging.DEBUG)
        ofh = logging.FileHandler(logger_online_file)
        ofh.setLevel(logging.DEBUG)

        # memory handler for rotate file handler
        self.mh = logging.handlers.MemoryHandler(constants.LOGGER_FILE_MEMORY_CACHE, target = fh)
        self.mh.setLevel(logging.DEBUG)
        self.omh = logging.handlers.MemoryHandler(constants.LOGGER_FILE_MEMORY_CACHE, target = ofh)
        self.omh.setLevel(logging.DEBUG)

        # set logger format
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s")
        #rh.setFormatter(formatter)
        fh.setFormatter(formatter)
        ofh.setFormatter(formatter)
        self.mh.setFormatter(formatter)
        self.omh.setFormatter(formatter)

        # main logger
        logger = logging.getLogger(constants.LOGGER_SERVER_NAME)
        logger.propagate = 0
        logger.setLevel(logging.DEBUG)

        # add handle to logger
        logger.addHandler(self.mh)
        logger.addHandler(self.omh)

        self.server = ThreadingTCPServer((constants.LOGGER_SERVER_IP, constants.LOGGER_SERVER_PORT), LogRequestHandler)
        self.server.serve_forever()
        self.server.server_close()

    def stop_server(self):
        if self.mh:
            self.mh.flush()
        if self.omh:
            self.omh.flush()
        if self.server:
            self.server.shutdown()

    def get_server(self):
        return self.server

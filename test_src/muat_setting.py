#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import logging
import unittest

from muat_report import GenerateResult, MuatReport
from dependency.automation_device import AutomationDevice
from dependency.account import Account
from dependency.apk_manager import ApkManager
from dependency.parametrized_test_case import ParametrizedTestCase
from dependency import constants
from dependency.adb_log import AdbLog



# Init logger
logger_name = '%s-%s' % (constants.LOGGER_CLIENT_MPT, os.getpid())
logger = logging.getLogger(logger_name)

class SettingTest(ParametrizedTestCase):
    def setUp(self):
        # check monitor running status
        if self.mon and not self.mon.running_status:
            self.skipTest('process monitor stop')

        self.d       = AutomationDevice().get_device()
        self.account = Account(self.d)

        self.account.sleep()
        self.account.wakeup()
        self.account.login()

    def tearDown(self):
        self.account.sleep()

    def test_mpc_settings(self):
        logger.info('Enter -- MPT:SettingsTest:test_mpc_settings')
        value = {}
        report = MuatReport()
        serial_number = None
        if self.param and self.param.parameters and self.param.parameters.serial_number:
            serial_number = self.param.parameters.serial_number

        apk_manager = ApkManager()
        apk = constants.MPT_SETTING_APK
        apk_info = apk_manager.get_apk_info(apk)

        if apk in apk_manager.local_apks_info:
            while True:
                for i in range(constants.MPT_SETTING_COUNT):
                    # check monitor running status
                    if self.mon and not self.mon.running_status:
                        break

                    # start apk
                    apk_manager.start_apk(apk, serial_number=serial_number)
                    time.sleep(1)

                    for resource_id in constants.MPT_SETTING_APK_RESOURCEIDS:
                        # check monitor running status
                        if self.mon and not self.mon.running_status:
                            break

                        # start adb log capture thread
                        detect_re = re.compile(r'MPT click UiSelector.PACKAGE NAME=%s, RESOURCE_ID=(%s:id/%s). at (.*)$' % (apk_info.package_name, apk_info.package_name, resource_id))
                        wanted_re = re.compile(r'MPT: sf post one frame at (.*)$')

                        adb_log = AdbLog(mode=AdbLog.MODE_RE | AdbLog.MODE_NEED_DETECT, wanted_re=wanted_re, detect_re=detect_re, logger=logger, serial_number=serial_number)
                        adb_log.clear()
                        adb_log.start()

                        # click setting items
                        button = self.d(packageName=apk_info.package_name, resourceId='%s:id/%s' % (apk_info.package_name, resource_id))
                        if button.exists:
                            logger.debug('click item (%s)' % (resource_id))
                            button.click()
                            time.sleep(2)
                        else:
                            logger.warning('not found item(%s)' % (resource_id))

                        # check the log and get the data
                        while True:
                            if len(adb_log.result) == 2:
                                break
                            else:
                                time.sleep(1)

                        # store the result
                        click_item = ''
                        start_time = 0
                        end_time = 0
                        cost_time = 0
                        try:
                            click_item      = adb_log.result[0][0]
                            start_time      = int(adb_log.result[0][1])
                            end_time        = int(adb_log.result[1][0])
                            if click_item == '%s:id/%s' % (apk_info.package_name, resource_id):
                                cost_time = end_time - start_time
                            else:
                                logger.error('detect_re detect the wrong item: (%s)' % (adb_log.result[0]))
                        except:
                            logger.error('retrieve time from (%s) error' % (adb_log.result))

                        logger.info('setting item(%s) cost: %s' % (resource_id, cost_time))

                        if resource_id in value:
                            value[resource_id].append(cost_time)
                        else:
                            value[resource_id] = [cost_time]

                        # report message
                        report.add_message(data_name='muat_setting', MON_Time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), item=resource_id, unit='ms', value=cost_time, item_name=constants.MPT_SETTING_APK_RESOURCEIDS_CN[resource_id].decode('gb2312'))

                        adb_log.join()

                    # close apk
                    apk_manager.close_apk(apk)

                if self.mon and not self.mon.running_status:
                    break

                if self.param and self.param.parameters and self.param.parameters.special_keys and 'run_one_cycle' in self.param.parameters.special_keys:
                    break

        if value:
            logger.debug('setting test : %s' % (value))
            #result_items = []
            summary = {}
            for resource_id in value:
                summary[resource_id] = sum(value[resource_id]) / len(value[resource_id])
                #result_items.append(summary[resource_id])
            #summary[constants.MPT_SETTING_RESULT_TOTAL] = sum(result_items) / len(result_items)
            logger.debug('setting test - summary: %s' % (summary))

            result = GenerateResult(case=os.path.basename(os.path.abspath(__file__)), unit='ms', standard=0, summary=summary, value=value)
            if result.result:
                report.add_result(result.result)
        else:
            logger.error('setting test failed')

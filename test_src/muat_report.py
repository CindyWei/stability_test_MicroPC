# -*- coding: utf-8 -*-

import os
import csv
import time

from dependency.singleton import *
from dependency.send_message import *
from dependency import singleton

class ItemTranslator():
    def __init__(self):
        self._trans_dict = {
                            # mpt_applaunch.py
                            'appstore.apk'    : '应用商店',
                            'Browser.apk'     : '浏览器',
                            'MpcSettings.apk' : '设置',

                            # mpt_applist.py
                            'AppList'         : '应用列表',

                            # mpt_setting.py
                            'exToggleButton0' : '系统',
                            'exToggleButton1' : '网络',
                            'exToggleButton2' : '壁纸',
                            'exToggleButton4' : '显示',
                            'exToggleButton5' : '日期和时间',
                            'exToggleButton7' : '版权信息',
                            'exToggleButton8' : '设备注册',

                            # mpt_statusbar.py
                            'calendar'        : '日历',
                            'net'             : '网络',
                           }
    def get_item(self, item):
        if item in self._trans_dict:
            return self._trans_dict[item]
        else:
            return None


class Result():
    CASE = 'case'
    UNIT = 'unit'
    STANDARD = 'standard'
    SUMMARY = 'summary'
    VALUE = 'value'

    def __init__(self, result):
        self._result = result
        self._validation = True

        self.validate_result()

    def validate_result(self):
        checks = [Result.CASE, Result.UNIT, Result.STANDARD,
                  Result.SUMMARY, Result.VALUE]

        for check in checks:
            if not self._result.has_key(check):
                self._validation = False
                break

        if not self.summary or not self.value:
            self._validation = False
        elif type(self.summary) != dict or type(self.value) != dict:
            self._validation = False
        elif len(self.summary) != len(self.value):
            self._validation = False
        else:
            pass

    @property
    def case(self):
        if Result.CASE in self._result:
            return self._result[Result.CASE]
        else:
            return ''

    @property
    def unit(self):
        if Result.UNIT in self._result:
            return self._result[Result.UNIT]
        else:
            return ''

    @property
    def standard(self):
        if Result.STANDARD in self._result:
            return self._result[Result.STANDARD]
        else:
            return ''

    @property
    def summary(self):
        if Result.SUMMARY in self._result:
            return self._result[Result.SUMMARY]
        else:
            return ''

    @property
    def value(self):
        if Result.VALUE in self._result:
            return self._result[Result.VALUE]
        else:
            return ''

    @property
    def validation(self):
        return self._validation

    def csv_output(self):
        translator = ItemTranslator()
        csv_lists = []

        if self._validation:
            item_count = 0
            for item in self.summary:
                item_score = ''
                if self.standard:
                    item_score = '%.0f%%' % (float(self.summary[item]) / float(self.standard) * 100)

                item_trans = translator.get_item(item)
                if not item_trans:
                    item_trans = item

                if item_count == 0:
                    csv_lists.append([self.case, self.unit, item_trans, self.summary[item], item_score, self.value[item]])
                else:
                    csv_lists.append(['', '', item_trans, self.summary[item], item_score, self.value[item]])

                item_count = item_count + 1

        return csv_lists


class GenerateResult():
    AVAILABLE_ITEMS    = [
                            Result.CASE,
                            Result.UNIT,
                            Result.STANDARD,
                            Result.SUMMARY,
                            Result.VALUE
                          ]

    def __init__(self, **kwargs):
        self._result = {}
        for key in kwargs:
            if key in GenerateResult.AVAILABLE_ITEMS:
                self._result[key] = kwargs[key]

        # check the validation of the message
        res = Result(self._result)

        if not res.validation:
            self._result = {}

    @property
    def result(self):
        return self._result


class MuatReport(singleton.Singleton):
    def init(self, qout, *args, **kwargs):
        self.qout = qout
        self._results = []
        self.filename = time.strftime('%Y%m%d-%H%M%S-MPT.csv', time.localtime(time.time()))

    def add_message(self, **kwargs):
        if self.qout and kwargs:
            if 'data_name' in kwargs and 'MON_Time' in kwargs:
                kwargs[send_message.RPL_SENDER] = 'micropc'
                self.qout.put(kwargs)

    def add_result(self, result):
        if result and type(result) == dict:
            res = Result(result)
            if res.validation:
                self._results.append(result)

    def clear_result(self):
        self._results = []

    def generate_report(self, logger=None):
        f = csv.writer(open(self.filename, "wb+"))

        # Write CSV Header, If you dont need that, remove this line
        f.writerow([self.filename])
        f.writerow(["Case", "Unit", "Item", "Summary", "Score", "Value"])

        if self._results:
            for res in self._results:
                result = Result(res)
                csv_lists = result.csv_output()

                if csv_lists:
                    for csv_list in csv_lists:
                        f.writerow(csv_list)
                        if logger:
                            logger.debug(csv_list)

    @property
    def result(self):
        return self._results

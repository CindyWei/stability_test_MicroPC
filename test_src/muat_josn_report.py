#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import json
import requests
import bs4

from dependency.adb_tools import AdbTools
from dependency import constants

class JsonReport():
    def __init__(self):
        self.adb_tool = AdbTools()
        
        self.data = {}
        
        self.name = "MicroPC UI AutoTest"
        self.buildinfo = ""
        self.env = ""
        self.start_time = ""
        
        
        self.tester = 'yufan.yk'
        self.status = ""
        self.report_link = ""
        
        self.num = []
        self.totalnum = None
        self.passnum = None
        self.failnum = None
        self.errnum = None
        
        self.case_result = []
        self.test_run_result = []

    def UploadReportTo3P(self, htmlreport):
        filename = os.path.splitext(os.path.split(htmlreport)[1])[0]
        url = constants.REPORT_URL_WITHOUT_TESTID % (filename)
        return url
        
    def GenerateJsonResult(self, htmlreport):
        soup = bs4.BeautifulSoup(open(htmlreport))
        p = soup.findAll('p')
        for tmp in p:
            if tmp.text.find("Start Time:") != -1:
                self.start_time = tmp.text.replace("Start Time:", "").strip()
                break
        tr = soup.findAll("tr", {"id": "total_row"})
        for td in tr:
            for t in td.findAll("td"):
                self.num.append(t.text)
        
        if len(self.num) > 5:
            if self.num[0] == "Total":
                self.totalnum = self.num[1]
                self.passnum = self.num[2]
                self.failnum = self.num[3]
                self.errnum = self.num[4]
        
        if self.totalnum == self.passnum:
            self.status = "pass"
        else:
            self.status = "failed"
        
        div = soup.findAll("div", {"class": "testcase"})
        for d in div:
            next_sibling = d.parent.next_siblings
            case_name = d.text
            case_result = ""
            case_status = ""
            error_log = ""
            for sibling in next_sibling:
                for s in sibling:
                    if type(s) == bs4.element.Tag:
                        for result in s.parent.findAll('a', {"class", "popup_link"}):
                            case_result = result.text.strip()
                            if case_result.encode("utf-8") != u"pass":
                                case_status = 'fail'
                            else:
                                case_status = case_result
                            break
                        for taginfo in s.parent.findAll('div', {"class", "popup_window"}):
                            for tag in taginfo:
                                for log in tag.parent.findAll('pre'):
                                    error_log = log.text.strip()
                                    break
                                break
                            break
                        break
                    elif type(s) == bs4.element.NavigableString:
                        if s.strip() != "":
                            case_result = s.strip()
                            if case_result.encode("utf-8") != u"pass":
                                case_status = 'fail'
                            else:
                                case_status = case_result
                            break
            self.case_result.append({"binary_name":"", "case_id": "", "case_name":case_name, "case_result": case_result, "status": case_status, "error_log":error_log, "status_reason":""})
        
        ret = self.adb_tool.adb_shell("getprop ro.build.version.release", need_ret=True)
        if ret[0].rstrip() != "":
            self.buildinfo = ret[0].rstrip()
        
        self.report_link = self.UploadReportTo3P(htmlreport)
        
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        
        self.test_run_result = [{"env":"", "extra":"", "finish_prepare":"", "tester":self.tester, "status": self.status, "status_reason":"", "start_time": self.start_time, "end_time": now, "report_link":self.report_link, "case_results": self.case_result}]
        
        test_data = {"test_run_results": self.test_run_result, "type": "TEST", "build_info": self.buildinfo, "env": "Linux", "extra":"", "name":self.name, "purpose": u"MicroPC UI自动化测试", "reg_time": now, "target": u"云PC"}   
        
        tp = json.dumps(test_data)
        
        return tp
    
    def PostToCluster(self, info):
        url = 'http://cluster.aliyun-inc.com/tianchi/apis/insert_whole_test.json'
        print info
        r = requests.post(url, data={"test_info": info})
        print r.json()
        jsonstr = json.dumps(r.json())
        ret = json.loads(jsonstr)
        if ret['status'] == 'succeed':
            return ret['test_id']
        else:
            return 0


    def PostTo3P(self, file, testid):
        filename = os.path.splitext(os.path.split(file)[1])[0]
        url = constants.REPORT_URL % (filename, str(testid))
        files = {'file': open(file, 'rb')}
        r = requests.post(url, files=files)
        print r.json()
        
        
        
                
                
                
                
        
    
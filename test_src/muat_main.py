#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import sys
import logging
import time
import datetime
import unittest
import xmlrunner

from dependency.automation_device import *
from dependency.parametrized_test_case import *
from dependency import constants, parse_parameters, parse_command, log_tools, HTMLTestRunner
from dependency.process_monitor import ProcessMonitor
from dependency.parse_parameters import *
from dependency.parse_command import *
from muat_josn_report import JsonReport
#from win32com.client.selecttlb import FLAG_CONTROL

logger_server       = None
logger_client       = None
logger              = None
automation_device   = None
csv_report          = None

# load test case from module
def load_tests_from_module(module):
    return unittest.defaultTestLoader.loadTestsFromModule(module)

# find test case from file like "muat_*.py"
def find_all_testcase(args, mon):
    files = []

    if not args.parameters or not args.parameters.config_file:
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        print path
        files = os.listdir(path)
    else:
        files = args.parameters.config_file
    path = os.path.abspath(os.getcwd())
    sys.path.append(os.path.join(path, 'testcase'))
    print sys.path
    test = re.compile(r"^muat_.*\.py$", re.IGNORECASE)
    files = filter(test.search, files)
    logger.info('MUAT test case: (%s)' % (files))

    filenameToModuleName = lambda f: os.path.splitext(f)[0]
    moduleNames = map(filenameToModuleName, files)
    modules = map(__import__, moduleNames)

    #return unittest.TestSuite(map(load_tests_from_module, modules))
    # load cases from class, this method could pass parameter to each test case
    suite = unittest.TestSuite()
#recycle the suite
#     cyclenum = 3
#     tmpnum = 0
#     while tmpnum < cyclenum:
    for module in modules:
        test_classes = None
        if module.__name__ == 'muat_multiwindows':
            test_classes = [module.MultiWindowsTest]
        elif module.__name__ == 'muat_appsystem':
            test_classes = [module.AppSystemTest]
        elif module.__name__ == 'muat_settingssystem':
            test_classes = [module.SettingsSystemTest]
        elif module.__name__ == 'muat_mobileim_intel':
            test_classes = [module.MobileImTest]
        elif module.__name__ == 'muat_youku_intel':
            test_classes = [module.YoukuTest]
        elif module.__name__ == 'muat_filesystem':
            test_classes = [module.FileSystemTest]
        elif module.__name__ == 'muat_desktopsystem':
            test_classes = [module.DesktopSystemTest]
        elif module.__name__ == 'muat_browser':
            test_classes = [module.BrowserTest]
        elif module.__name__ == 'muat_cuntao':
            test_classes = [module.CunTaoTest]
        elif module.__name__ == 'muat_stressvdi':
            test_classes = [module.StressVdiTest]
        elif module.__name__ == 'muat_wps':
            test_classes = [module.WPSTest]
        elif module.__name__ == 'muat_input':
            test_classes = [module.InputTest]
        elif module.__name__ == 'muat_chrome':
            test_classes = [module.ChromeTest]
        elif module.__name__ == 'muat_paint':
            test_classes = [module.PaintTest]
        elif module.__name__ == 'muat_printscreen':
            test_classes = [module.PrintScreenTest]
        elif module.__name__ == 'muat_browserpro':
            test_classes = [module.BrowserProTest]
        else:
            pass
        
        if test_classes:
            for test_class in test_classes:
                suite.addTest(ParametrizedTestCase.parametrize(test_class, param=args, mon=mon))
#         tmpnum += 1
    return suite

def prepare_test_env(args, qout):
    # Init logger server
    if args.parameters and args.parameters.special_keys and 'enable_logger_server' in args.parameters.special_keys:
        print '-------------------- enable logger server --------------------'
        global logger_server
        logger_server = log_tools.LoggerServer()
        logger_server.start()

    global logger_client
    global logger
    logger_name = '%s-%s' % (constants.LOGGER_CLIENT_MUAT, os.getpid())
    logger_client = log_tools.LoggerClient(logger_name)
    logger = logging.getLogger(logger_name)
    logger.info('Start muat test')

    # Init uiautomator server
    global automation_device
    if args.parameters and args.parameters.serial_number:
        automation_device = AutomationDevice(serial_number=args.parameters.serial_number)
    else:
        automation_device = AutomationDevice()

    # Open report
    #global csv_report
    #csv_report = MuatReport(qout)

def clear_test_env():
    # generate report
    #if csv_report:
        #csv_report.generate_report(logger)

    # stop uiautomator server
    if automation_device:
        automation_device.stop_device()

    # close logger client and server
    if logger_client:
        logger_client.close_sh()

    if logger_server:
        logger_server.stop_server()
        logger_server.join()
    logger.info('stop muat test')

# find all test case and run test
def main(args, qout=None, qin=None):
    prepare_test_env(args, qout)

    # start monitor thread
    mon = ProcessMonitor(qin, logger)
    mon.start()

    # create test suite and run the test
    suite = find_all_testcase(args, mon)
#     runner = xmlrunner.XMLTestRunner(output='test-reports')
#     runner.run(suite)
    
    report_filename = "TEST-MUAT-%s.html" % time.strftime('%Y%m%d%H%M%S', time.localtime())
    report_file = os.path.join(os.path.abspath(os.path.dirname("__file__")), "test-reports", report_filename)
    fp = file(report_file, 'wb')
    fp.close()

#change the testgroup running time by modifying the constant RUNNINGTIMEOUT in file constants.py
#if you want to run once, change the value of RUNNING_TIMEOUT to 0.

    #startime = datetime.datetime.now()
    starttime = datetime.datetime.now()
    endtime = starttime + datetime.timedelta(hours=constants.RUNNING_TIMEOUT)
    flag = True
     
    while flag:
        if starttime == endtime:
            fp = file(report_file, 'ab')
            runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='MicroPC UI AutoTest', description='Test Report')
            runner.run(suite)
            fp.close()
            flag = False
            #break

        elif datetime.datetime.now() > endtime:
            flag = False
        else:
            fp = file(report_file, 'ab')
            runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='MicroPC UI AutoTest', description='Test Report')
            runner.run(suite)
            fp.close()


      
    mon.stop()
    mon.join(1)
    clear_test_env()
    #fp.close()
    
    if args._debugmode == False:
        reporter = JsonReport()
        jsoninfo = reporter.GenerateJsonResult(report_file)
        test_id = reporter.PostToCluster(jsoninfo)
        reporter.PostTo3P(report_file, test_id)

if __name__ == "__main__":
    # prepare args with enable_logger_server
#     params = parse_parameters.GenerateParameters(special_keys = ['muat_desktopsystem.py'])
#     params = parse_parameters.GenerateParameters(special_keys = ['enable_logger_server', 'run_one_cycle'], config_file = ['muat_browser.py', 'muat_cuntao.py',  'muat_appsystem.py', 'muat_settingssystem.py', 'muat_desktopsystem.py', 'muat_multiwindows.py'])
    params = parse_parameters.GenerateParameters(special_keys = ['enable_logger_server', 'run_one_cycle'], config_file = ['muat_mobileim_intel.py','muat_wps.py','muat_cuntao.py','muat_appsystem.py','muat_browser.py','muat_desktopsystem.py','muat_multiwindows.py','muat_settingssystem.py','muat_printscreen.py'])
    command = parse_command.GenerateCommand()
    command.add_command(
        type       = 'scenario',
        name       = 'single_unittest',
        start_time = '',
        end_time   = '',
        parameters = params.parameters,
        rate       = '0',
        debug_mode = True)

    args = parse_command.Command(command.command[0])
    args.validate_command()

    if args.validation_command:
        print args
        main(args, qout=None, qin=None)

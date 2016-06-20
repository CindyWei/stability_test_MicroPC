# -*- coding: utf-8 -*-

import unittest

class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None, mon=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param
        self.mon   = mon

    @staticmethod
    def parametrize(testcase_klass, param=None, mon=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param, mon=mon))
        return suite

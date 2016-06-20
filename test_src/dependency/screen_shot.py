#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import logging
import unittest
import shutil
import inspect
import sys

def ScreenShot(self,x):
    x
    TmpImagePath1 = os.path.join(os.path.abspath(os.path.dirname("__file__")), "test-reports", "TmpImage1")
    name1 = x + "_%s.jpg" % time.strftime('%Y%m%d%H%M%S', time.localtime())
    img1 = os.path.join(TmpImagePath1, name1)
    self.d.screenshot(img1)
    time.sleep(5)
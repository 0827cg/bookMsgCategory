#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-10-24 16-23

import os
from util.logUtil import LogUtil
from util.configureUtil import ConfigureUtil

class BookMsgPro():

    _strLogDirPath = 'logs' + os.sep
    strConfigDirPath = 'conf' + os.sep
    strConfigFileName = 'book.conf'

    logUtilObj = LogUtil(_strLogDirPath)
    configureUtilObj = ConfigureUtil(logUtilObj, strConfigDirPath, strConfigFileName)
    configParserObj = configureUtilObj.getCustomizeConfigParserObj()


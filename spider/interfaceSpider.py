#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe: 请求接口, 获取json数据
# author: cg
# time: 2018-10-24 16-33

import urllib.request
import json
import time
from lib.bookMsgPro import BookMsgPro


class InterfaceSpider(BookMsgPro):

    '''
    describe: 请求接口, 获取json数据
    '''


    def getJsonMsg(self, strUrl):

        '''
        describe: get请求, 且不需要传入参数
        :param strUrl: 接口全路径
        :return: 返回一个dict字典类型数据
        '''

        # bytesData = urllib.request.urlopen(strUrl).read()
        self.logUtilObj.writerLog('正在请求接口: ' + strUrl)
        intIndexTime = time.time()
        httpResponseData = urllib.request.urlopen(strUrl)
        bytesData = httpResponseData.read()
        strData = bytesData.decode('utf-8')

        self.logUtilObj.writerLog('response: ' + strData)

        self.logUtilObj.writerLog('请求成功---耗时: ' + str(round(time.time() - intIndexTime, 4)) + 's')
        dictData = json.loads(strData)

        return dictData


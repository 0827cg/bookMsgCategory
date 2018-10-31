#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe: 操作类
# author: cg
# time: 2018-10-26 11-15

import gzip
import os
import json
import time
from lib.bookMsgPro import BookMsgPro
from util.fileUtil import FileUtil
from util.stringUtil import StringUtil
from spider.htmlSpider import HtmlSpider
from operatorBin.operatePage import OperatePage

class OperatorMsg(BookMsgPro):

    def __init__(self):

        if self.__initConfig() == 1:
            self.runDo()
        else:
            self.logUtilObj.writerLog('配置文件缺少配置参数')


    def runDo(self):

        intIndexTime = time.time()
        self.logUtilObj.writerLog('run Do')

        self.operatePageObj = OperatePage()
        dictPageUrl = self.operatePageObj.getHrefPage()

        intPageNum = 1

        for strUrl, strPageName in dictPageUrl.items():

            if strUrl != 'none':
                self.loopNextAndGetMsg(intPageNum, strUrl, strPageName)
            else:
                self.logUtilObj.writerLog('为找到[strPageName=' + strPageName + ',intPageNum=' + str(intPageNum) + ']页面的url')

            # strNextUrl = self.operatePageObj.getNextPageUrl(strUrl)
            # if strNextUrl is not None:
            #
            #     tagLabel = self.operatePageObj.getValueLabelForUrl(strNextUrl)
            #     # self.logUtilObj.writerLog(str(tagLabel))
            #     # xmlSpiderObj = XmlSpider()
            #     # xmlSpiderObj.getValueMessageByLabel(tagLabel)
            #
            #     dictResult = self.operatePageObj.getValueMessageByLabel(strNextUrl, tagLabel)
        intNowTime = time.time()
        strMinusSec = str(round(intNowTime - intIndexTime, 4)) + 's'
        strMinusMin = str(round((intNowTime - intIndexTime) / 60, 4)) + 'min'
        self.logUtilObj.writerLog('[程序只需完成, ---总耗时: ' + strMinusSec + '(' + strMinusMin + ')')


    def loopNextAndGetMsg(self, intPageNum, strUrl, strPageName):

        '''
        describe: 先获取当前页面中所有图书的信息, 并保存, 之后在获取此页面的下一页, 再次获取图书信息, 直到无下一页结束
        :param intPageNum: 当前页面的页数编号
        :param strUrl: 当前页面的url
        :param strPageName: 当前页面所属的标签名
        :return:
        '''

        intIndexTime = time.time()
        self.logUtilObj.writerLog('准备获取当前页面[strPageName=' + strPageName + ', intPageName=' +
                                  str(intPageNum) + ']的页面数据, 此时[strUrl=' + strUrl + ']...')

        # 获取也面内容
        strHtmlData = HtmlSpider().getHtmlStrMsg(strUrl)

        # 获取当前页面中存在book信息的标签块
        tagLabel = self.operatePageObj.getValueLabelByData(strHtmlData)

        # 从标签块中遍历图书, 获取图书信息
        dictResult = self.operatePageObj.getValueMessageByLabel(strUrl, tagLabel)
        # listBookMsg = dictResult['bookMsg']

        # 将图书信息写入到文件
        intResult = self.saveBookMsg(intPageNum, strPageName, strUrl, dictResult)
        if intResult != 1:
            self.logUtilObj.writerLog('保存图书信息出错')


        intNoFullBookNum = int(dictResult['intNoFullBook'])

        self.logUtilObj.writerLog('[strPageName=' + strPageName + ']的第' + str(intPageNum) + '页信息已爬取完成')
        self.logUtilObj.writerLog('存在' + str(intNoFullBookNum) + '本图书信息未完全获取')

        # 爬取完当前页面后, 尝试获取当前页面的下一页url
        strNextUrl = self.operatePageObj.getNextPageByData(strHtmlData, strUrl)
        if strNextUrl is None:

            self.logUtilObj.writerLog('[strPageName=' + strPageName +
                                      ']的页面此时已无下一页,[intPageNum=' + str(intPageNum) + ']')
            intNowTime = time.time()
            strMinusSec = str(round(intNowTime - intIndexTime, 4)) + 's'
            strMinusMin = str(round((intNowTime - intIndexTime) / 60, 4)) + 'min'
            self.logUtilObj.writerLog('[strPageName=' + strPageName + ']的' + str(intPageNum) +
                                      '张页面信息抓取完成, ---耗时: ' + strMinusSec + '(' + strMinusMin + ')')
        else:
            self.loopNextAndGetMsg(intPageNum + 1, strNextUrl, strPageName)


    def saveBookMsg(self, intPageNum, strPageName, strUrl, dictResult):

        '''
        describe: 写数据
        :param intPageNum: 当前页面的页数编号
        :param strPageName: 当前页面所属的标签名
        :param strUrl: 当前页面对应的url
        :param dictResult: 当前页面中book的数据
        :return: 1: 成功, -1: 出错
        '''

        fileUtilObj = FileUtil()

        try:

            dictConfig = self.configureUtilObj.getConfig(self.configParserObj)

            strRootPath = dictConfig.get(self.configureUtilObj.configMsgObj.strSaveFilePathKey)
            strParCateGoryName = dictConfig.get(self.configureUtilObj.configMsgObj.strParCateGoryNameKey)

            # 替换个别字符
            strNextDirName = StringUtil.replaceAllChar(strParCateGoryName)

            strOutFileName = str(intPageNum) + '.json'

            strFullPathFileName = strRootPath + strNextDirName + os.sep + strPageName + os.sep + strOutFileName

            strBookMsgData = json.dumps(dictResult, indent=3, ensure_ascii=False)

            fileUtilObj.checkAndCreateDir(strRootPath + strNextDirName + os.sep + strPageName + os.sep)
            fileUtilObj.writerFileContent(strFullPathFileName, strBookMsgData)

        except Exception as error:

            self.logUtilObj.writerLog('当前页面[strPageName=' + strPageName + ', intPageNum=' + str(intPageNum) +
                                      'strUrl=' + strUrl + ']的图书信息写入出错')
            return -1
        else:
            self.logUtilObj.writerLog('当前页面[strPageName=' + strPageName + ', intPageNum=' + str(intPageNum) +
                                      ', strUrl=' + strUrl + ']写入完成')
            self.logUtilObj.writerLog('保存文件路径为: ' + strFullPathFileName)
            return 1





    def __initConfig(self):

        '''
        describe: 初始化和检测配置文件
        :return: 1: 配置文件无错误, -1: 配置文件有错
        '''

        self.fileUtilObj = FileUtil()

        self.fileUtilObj.checkAndCreateDir(self.strConfigDirPath)

        intIndex = self.configureUtilObj.checkAndInitConfigure(self.configParserObj)

        self.logUtilObj.writerLog('check and init config result: ' + str(intIndex))

        return intIndex


#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe: 解析页面用的spider
# author: cg
# time: 2018-10-24 16-33

import urllib.request
import time
from lib.bookMsgPro import BookMsgPro
from bs4 import BeautifulSoup


class HtmlSpider(BookMsgPro):


    def getHtmlHttpReponse(self, strUrl):

        '''
        describe: 请求url, 获取响应内容
        :param strUrl: 需要请求的url
        :return: 返回一个httpResponse类型的数据
        '''

        self.logUtilObj.writerLog('正在请求页面[' + strUrl + ']')
        intIndexTime = time.time()
        httpResponseData = urllib.request.urlopen(strUrl)

        intCode = httpResponseData.getcode()

        self.logUtilObj.writerLog(str(httpResponseData.info()))
        self.logUtilObj.writerLog('response url:[' + httpResponseData.geturl() + ']')

        if intCode == 200:
            self.logUtilObj.writerLog('请求成功---耗时: ' + str(round(time.time() - intIndexTime, 4)) + 's')
        else:
            self.logUtilObj.writerLog('请求出错[code=' + str(intCode) + ']--耗时: '+
                                      str(round(time.time() - intIndexTime, 4)) + 's')

        return httpResponseData


    def getHtmlMsg(self, strUrl):

        '''
        describe: 根据url获取页面数据,
        :param strUrl: 需要获取的页面的url
        :return: 返回页面数据, 为bytes类型
        '''

        httpResponseData = self.getHtmlHttpReponse(strUrl)

        # 读取响应体
        bytesData = httpResponseData.read()

        httpResponseData.close()
        return bytesData


    def getHtmlStrMsg(self, strUrl):

        '''
        describe: 根据url来获取页面的源代码内容, 已按页面编码来解码
        :param strUrl: 需要获取的页面的url
        :return: 返回页面数据, 为str类型
        '''

        httpResponseData = self.getHtmlHttpReponse(strUrl)
        strCoding = httpResponseData.headers.get_content_charset()
        bytesData = httpResponseData.read()
        strHtml = bytesData.decode(strCoding, 'ignore')

        httpResponseData.close()
        # print(httpResponseData.closed)
        return strHtml


    def getDivLabelByClassValue(self, strUrl, strValue):

        '''
        describe: 获取div标签, 根据div标签中的class属性值来在规定页面获取
        :param strUrl: 页面的url
        :param strValue: div标签中的class属性的值
        :return: 返回存放该标签的ResultSet类型数据
        '''

        bytesData = self.getHtmlMsg(strUrl)
        beautifulObj = BeautifulSoup(bytesData, "html.parser")
        resultSetLabel = beautifulObj.findAll('div', {'class': strValue})

        return resultSetLabel

    def getDivLabelByClassValueOnData(self, data, strValue):

        '''
        describe: 获取div标签, 在已有的页面数据基础上,根据div标签中的class属性值来在规定页面获取
        :param data: 页面的数据, 可为bytes类型,和str类型
        :param strValue: div标签中的class属性的值
        :return: 返回存放该标签的ResultSet类型数据
        '''

        beautifulObj = BeautifulSoup(data, 'html.parser')
        resultSetLabel = beautifulObj.find_all('div', class_=strValue)

        self.logUtilObj.writerLog('爬取到[div]的标签如: ' + str(resultSetLabel))

        return resultSetLabel

    def getLabelByText(self, strUrl, strLabelName, strText):

        '''
        describe: 根据标签的名字和标签的内容值来在规定的url页面中获取需要的标签
        :param strUrl: 需要打开的页面路径
        :param strLabelName: 需要获取的标签名字
        :param strText: 标签里面的内容
        :return: 返回一个存放标签的ResultSet类型数据
        '''

        bytesData = self.getHtmlMsg(strUrl)
        beautifulObj = BeautifulSoup(bytesData, "html.parser")
        resultSetLabel = beautifulObj.find_all(strLabelName, text=strText)

        self.logUtilObj.writerLog('爬取[text=' + strText + ']的[' + strLabelName + ']标签如: ' + str(resultSetLabel))

        return resultSetLabel


    def getLabelByTextOnData(self, data, strLabelName, strText):

        '''
        describe: 在已有的页面数据基础上, 根据标签的名字和标签的内容值来获取标签
        :param data: bytes类型的页面数据, 也可为str类型
        :param strLabelName: 需要获取的标签名
        :param strText: 需要获取的标签的内容值
        :return: 返回一个存放标签的ResultSet类型数据
        '''

        beautifulObj = BeautifulSoup(data, "html.parser")
        resultSetLabel = beautifulObj.find_all(strLabelName, text=strText)

        self.logUtilObj.writerLog('爬取到[text=' + strText + ']的[' + strLabelName + ']标签如: ' + str(resultSetLabel))

        return resultSetLabel

    def getLabelByKeyValueOnData(self, data, strLabelName, strKey, strValue):

        '''
        describe: 在已有的页面数据基础上, 根据标签的名字和标签的属性及属性值来获取标签, 只会获取一个, 所以要求参数值是页面中的唯一
        :param data: 页面数据, 可为bytes, str类型
        :param strLabelName: 需要获取的标签名
        :param strKey: 需要获取的标签的属性名
        :param strValue: 需要获取的标签的属性名的值
        :return: 返回一个bs4.element.Tag类型的数据
        '''

        beautifulObj = BeautifulSoup(data, "html.parser")
        tagLabel = beautifulObj.find(strLabelName, {strKey: strValue})

        self.logUtilObj.writerLog('爬取到[' + strKey + '=' + strValue + ']的[' +
                                  strLabelName + ']标签如: ' + str(tagLabel))

        return tagLabel


    def getLabelByKeyValueAndBrotherOnData(self, data, strLabelName, strKey, strValue):

        '''
        describe: 在已有的页面数据基础上, 根据标签的名字和标签的属性及属性值来获取标签, 只会获取一个, 所以要求参数值是页面中的唯一
        :param data: 页面数据, 可为bytes, str类型
        :param strLabelName: 需要获取的标签名
        :param strKey: 需要获取的标签的属性名
        :param strValue: 需要获取的标签的属性名的值
        :return: 返回一个bs4.element.Tag类型的数据
        '''

        beautifulObj = BeautifulSoup(data, "html.parser")
        resultSetLabel = beautifulObj.find_previous_siblings(strLabelName, {strKey: strValue})

        self.logUtilObj.writerLog('爬取到[' + strKey + '=' + strValue + ']的[' +
                                  strLabelName + ']标签如: ' + str(resultSetLabel))

        return resultSetLabel


    def getLabelByMoreKeyValueOnData(self, data, strLabelName, **kwargs):

        '''
        describe: 在已有的页面数据基础上, 根据标签的名字和多个标签的属性及属性值来获取标签(目前不支持class 和text, 暂时废弃)
        :param data: 页面数据, 可为bytes, str类型
        :param strLabelName: 需要获取的标签名
        :param kwargs: 键值对类型数据, 如, class='xxx', title='xxx'
        :return: 返回一个存放标签的resultSet类型数据
        '''

        beautifulObj = BeautifulSoup(data, "html.parser")
        resultSetLabel = beautifulObj.find_all(strLabelName, kwargs)

        self.logUtilObj.writerLog('爬取到[kwargs=' + str(kwargs) + ']的[' + strLabelName + ']标签如: ' + str(resultSetLabel))

        return resultSetLabel



    def getLabelKeyValue(self, strUrl, strLabelName, strText, strKey):

        '''
        describe: 在规定的页面里, 根据标签名和标签的内容值, 来获取该标签所含有的属性的值
        :param strUrl: 页面url
        :param strLabelName: 标签名
        :param strText: 标签的内容值
        :param strKey: 需要获取的标签中的属性的名字
        :return: 返回标签中的该属性的值, 为str类型数据
        '''

        self.logUtilObj.writerLog('正在爬取[ strText=' + strText + ' ]的标签strKey=' + strKey + '的值....')

        strValue = ''
        resultSetLabel = self.getLabelByText(strUrl, strLabelName, strText)

        for Tagitem in resultSetLabel:
            strValue = Tagitem.get(strKey)

        self.logUtilObj.writerLog('爬取完成,[' + strKey + ']的值为' + strValue)
        return strValue


    def getLabelKeyValueOnData(self, data, strLabelName, strText, strKey):

        '''
        describe: 在已知的页面数据中, 根据标签名和标签的内容值, 来获取该标签所含有的属性的值
        :param data: 已知的页面数据, bytes类型或str类型
        :param strLabelName: 标签名
        :param strText: 标签的内容值
        :param strKey: 需要获取的标签中的属性的名字
        :return: 返回标签中的该属性的值, 为str类型数据
        '''

        self.logUtilObj.writerLog('正在从页面内容中解析爬取[strText=' + strText + ']的标签strKey=' + strKey + '的值....')

        intIndexTime = time.time()

        strValue = ''
        resultSetLabel = self.getLabelByTextOnData(data, strLabelName, strText)

        for Tagitem in resultSetLabel:
            strValue = Tagitem.get(strKey)

        self.logUtilObj.writerLog('爬取完成,[' + strKey + ']的值为' + strValue +
                                  '---耗时: ' + str(round(time.time() - intIndexTime, 4)) + 's')
        return strValue






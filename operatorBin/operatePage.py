#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-10-29 19:11

import time
import urllib.parse
from lib.bookMsgPro import BookMsgPro
from util.fileUtil import FileUtil
from util.stringUtil import StringUtil
from bs4 import element
from spider.htmlSpider import HtmlSpider

class OperatePage(BookMsgPro):

    '''
    获取页面的url, 包括页面中需要请求的url和下一页url. 在方法getHrefPage()中将会自动获取根url(http/https + 域名)
    '''

    def __init__(self):

        self.htmlSpiderObj = HtmlSpider()
        self.fileUtilObj = FileUtil()


    def getHrefPage(self):

        '''
        describe: 获取各个标签对应的url
        :return: 返回一个list类型的数据, 其元素为标签对应的连接
        '''

        self.logUtilObj.writerLog('正在获取所有标签对应的url...')
        dictConfig = self.configureUtilObj.getConfig(self.configParserObj)

        strFirstPageName = dictConfig.get(self.configureUtilObj.configMsgObj.strParCateGoryNameKey)
        strUrl = dictConfig.get(self.configureUtilObj.configMsgObj.strHtmlUrlKey)
        parseResultUrl = urllib.parse.urlparse(strUrl)

        # print(type(parseResultUrl))
        # print(str(parseResultUrl))
        # print(parseResultUrl.netloc)
        # print(parseResultUrl.scheme)
        self.strBaseUrl = parseResultUrl.scheme + '://' + parseResultUrl.netloc
        # strHostName = parseResultUrl.hostname
        # bytesData = htmlSpiderObj.getHtmlMsg(strUrl)
        strHtml = self.htmlSpiderObj.getHtmlStrMsg(strUrl)

        strCategoryLabelName = dictConfig.get(self.configureUtilObj.configMsgObj.strChiCategoryLabelNameKey)
        strCategoryKeyName = dictConfig.get(self.configureUtilObj.configMsgObj.strChiCategoryKeyNameKey)
        strCategoryName = dictConfig.get(self.configureUtilObj.configMsgObj.strChiCateGoryNameKey)

        listCategoryName = strCategoryName[1:-1].split(', ')

        listCategoryHref = []

        dictCategoryHrefName = {}

        for itemCategoryName in listCategoryName:

            tagLabel = self.htmlSpiderObj.getLabelByKeyValueOnData(strHtml, strCategoryLabelName, strCategoryKeyName, itemCategoryName)

            strFullUrl = self.strBaseUrl + tagLabel['href']
            # listCategoryHref.append(self.strBaseUrl + tagLabel['href'])

            dictCategoryHrefName[strFullUrl] = itemCategoryName

        self.logUtilObj.writerLog(str(listCategoryHref))

        self.logUtilObj.writerLog('获取完成, 该页面[strFirstPageName=' + strFirstPageName + ']中需要进行next爬取的url如: ' + str(listCategoryHref))

        return dictCategoryHrefName


    def getNextPageByUrl(self, strUrl):

        '''
        describe: 获取页面对应的下一页url
        :param strUrl: 此时页面的url()
        :return: 返回下一页url(根url + 页面url)
        '''

        strHtml = self.htmlSpiderObj.getHtmlStrMsg(strUrl)
        tagLable = self.htmlSpiderObj.getLabelByKeyValueOnData(strHtml, 'a', 'title', '下一页')

        if tagLable is None:

            self.logUtilObj.writerLog('此页面未发现下一页[strUrl=' + strUrl + ']')
            return None
        else:
            strNextUrl = tagLable['href']
            return self.strBaseUrl + strNextUrl


    def getNextPageByData(self, data, strUrl):

        '''
        describe: 获取页面对应的下一页url
        :param data: 此时页面的内容
        :param strUrl: 此时页面的url, 方法里并不做请求
        :return: 返回下一页url(根url + 页面url)
        '''


        tagLable = self.htmlSpiderObj.getLabelByKeyValueOnData(data, 'a', 'title', '下一页')

        if tagLable is None:

            self.logUtilObj.writerLog('此页面未发现下一页[strUrl=' + strUrl + ']')
            return None
        else:
            strNextUrl = tagLable['href']
            return self.strBaseUrl + strNextUrl


    def getValueLabelByUrl(self, strUrl):


        '''
        describe: 获取strUrl对应的页面中的属性块
        :param strUrl: 页面url
        :return:
        '''

        strHtml = self.htmlSpiderObj.getHtmlStrMsg(strUrl)

        tagLabel = self.htmlSpiderObj.getLabelByKeyValueOnData(strHtml, 'ul', 'id', 'component_0__0__6612')

        # print(type(tagLabel))
        return tagLabel


    def getValueLabelByData(self, data):


        '''
        describe: 获取页面data中的属性块
        :param data: 页面的内容
        :return:
        '''

        # strHtml = self.htmlSpiderObj.getHtmlStrMsg(strUrl)

        tagLabel = self.htmlSpiderObj.getLabelByKeyValueOnData(data, 'ul', 'id', 'component_0__0__6612')

        return tagLabel


    def getValueMessageByLabel(self, strUrl, tagLabel):

        '''
        describe: 获取tabLabel标签块中的书籍数据
        tag的 .contents 属性可以将tag的子节点以列表的方式输出,
        得到的list集合中其元素有值的话为Tag类型, 无值的话为NavigableString类型
        :param strUrl: 此时的页面的url, 方法里并不做请求
        :param tagLabel: 此时的页面对应的一个标签快, 包含有多本书籍的信息. 以需要拿到元素的标签作为tagLabel中的子标签, 即tagLabel为一个标签块
        :return: 返回一个dict类型数据, 其存在key: bookMsg, intNoFullBook. bookMsg: 图书信息, list类型, intNoFullBook: 为完全爬取的图书个数
        '''

        intIndexTime = time.time()
        self.logUtilObj.writerLog('长度: ' + str(len(tagLabel)))

        # 通过.contents或者.children的方式来获取子节点时, 会多出无数据的元素来, 使得得到的list/list_iterable集合长度多一倍+1
        # 其多出的元素类型为bs4.element.NavigableString类型,
        listTag = tagLabel.contents

        dictResult = {}

        listBookMsg = []

        intIndex = 0
        intNoFullMessageNum = 0

        for tagItem in listTag:

            intResult = 0

            if not isinstance(tagItem, element.NavigableString):

                singleBookMsg = {}

                self.logUtilObj.writerLog('正在爬取此页面[strUrl=' + strUrl + ']中的第' + str(intIndex + 1) + '本书的信息...')

                # 图书的名字, 链接, 图片链接
                tagLabelSingleBookHref = self.htmlSpiderObj.getLabelByKeyValueOnData(str(tagItem), 'a', 'name', 'itemlist-picture')
                if tagLabelSingleBookHref is not None:

                    singleBookMsg['bookName'] = tagLabelSingleBookHref.get('title')
                    singleBookMsg['bookHref'] = tagLabelSingleBookHref.get('href')

                    listPicHref = self.removeNullItem(tagLabelSingleBookHref.contents)
                    singleBookMsg['bookPicUrl'] = listPicHref[0].get('data-original')

                else:
                    singleBookMsg['bookName'] = 'none'
                    singleBookMsg['bookHref'] = 'none'
                    singleBookMsg['bookPicUrl'] = 'none'
                    intResult = -1

                # 此时图书的售价
                tagLabelBookNowPrice = self.htmlSpiderObj.getLabelByKeyValueOnData(str(tagItem), 'span', 'class', 'search_now_price')
                if tagLabelBookNowPrice is not None:

                    singleBookMsg['nowPrice'] = tagLabelBookNowPrice.get_text()
                else:
                    singleBookMsg['nowPrice'] = 'none'
                    intResult = -1

                # 图书的定价
                tagLabelBookPrePrice = self.htmlSpiderObj.getLabelByKeyValueOnData(str(tagItem), 'span', 'class', 'search_pre_price')
                if tagLabelBookPrePrice is not None:
                    singleBookMsg['prePrice'] = tagLabelBookPrePrice.get_text()
                else:
                    singleBookMsg['prePrice'] = 'none'
                    intResult = -1

                # 图书的打折详情
                tabLabelBookDiscount = self.htmlSpiderObj.getLabelByKeyValueOnData(str(tagItem), 'span', 'class', 'search_discount')
                if tabLabelBookDiscount is not None:

                    singleBookMsg['disCount'] = tabLabelBookDiscount.get_text()
                else:
                    singleBookMsg['disCount'] = 'none'
                    intResult = -1

                # 对图书的评论好评情况
                tagCommentLevel = self.htmlSpiderObj.getLabelByKeyValueOnData(str(tagItem), 'span', 'class', 'search_star_black')
                if tagCommentLevel is not None:
                    listCommentLevel = self.removeNullItem(tagCommentLevel.contents)
                    strCommentLevel = listCommentLevel[0].get('style')
                    singleBookMsg['commentLevel'] = strCommentLevel[7:-1]
                else:
                    singleBookMsg['commentLevel'] = 'none'
                    intResult = -1

                # 对图书的评论个数
                tagLabelBookComment = self.htmlSpiderObj.getLabelByKeyValueOnData(str(tagItem), 'a', 'class', 'search_comment_num')
                if tagLabelBookComment is not None:
                    singleBookMsg['commentNum'] = tagLabelBookComment.get_text()
                else:
                    singleBookMsg['commentNum'] = 'none'
                    intResult = -1

                # 图书作者
                tagLabelBookAuthor = self.htmlSpiderObj.getLabelByKeyValueOnData(str(tagItem), 'a', 'name', 'itemlist-author')
                if tagLabelBookAuthor is not None:
                    singleBookMsg['bookAuthor'] = tagLabelBookAuthor.get_text()
                else:
                    singleBookMsg['bookAuthor'] = 'none'
                    intResult = -1

                # 出版社
                tagLabelBookPubH = self.htmlSpiderObj.getLabelByKeyValueOnData(str(tagItem), 'a', 'name', 'P_cbs')
                if tagLabelBookPubH is not None:

                    singleBookMsg['bookPublishHouse'] = tagLabelBookPubH.get_text()
                else:
                    singleBookMsg['bookPublishHouse'] = 'none'
                    intResult = -1

                # 出版日期
                tagLabelBookData = self.htmlSpiderObj.getLabelByKeyValueOnData(str(tagItem), 'p', 'class', 'search_book_author')
                if tagLabelBookData is not None:
                    listData = self.removeNullItem(tagLabelBookData.contents)
                    # strData = StringUtil.replaceAllChar(listData[1].get_text())
                    singleBookMsg['bookPublishTime'] = StringUtil.replaceAllChar(listData[1].get_text())

                else:
                    singleBookMsg['bookPublishTime'] = 'none'
                    intResult = -1

                self.logUtilObj.writerLog(str(singleBookMsg))
                listBookMsg.append(singleBookMsg)


                intIndex += 1

                if intResult == -1:
                    intNoFullMessageNum += 1
        dictResult['bookMsg'] = listBookMsg
        dictResult['intNoFullBook'] = intNoFullMessageNum

        self.logUtilObj.writerLog('此页面[strUrl=' + strUrl + ']有' + str(intNoFullMessageNum) + '本书的信息未爬全')
        self.logUtilObj.writerLog('此页面[strUrl=' + strUrl + ']的图书信息抓取完成' + str(round(time.time() - intIndexTime, 4)) + 's')

        return dictResult



    def removeNullItem(self, listTag):

        '''
        describe: 删除集合中的多余元素
        :param listTag: list类型, 由tag.contents产生, 会由多余的元素如'\n'
        :return: 返回一个List类型
        '''

        listNewTag = []

        for tagItem in listTag:

            if not isinstance(tagItem, element.NavigableString):
                listNewTag.append(tagItem)

        return listNewTag









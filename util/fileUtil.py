#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-10-24 18-33


import os
import time
from lib.bookMsgPro import BookMsgPro


class FileUtil(BookMsgPro):

    '''
    describe: 文件操作类
    '''

    def readFileContent(self, strInputFileName, strEncode='utf-8'):

        '''
        describe: 读取文件内容并返回, 每次只读取1000字节, 默认为utf-8格式
        :param strInputFileName: 需要读取的文件存放路径和文件名的组合
        :param strEncode: 文件编码格式, 默认utf-8格式
        :return: 返回文件内容, str类型
        '''

        strFileContent = ''

        if os.path.exists(strInputFileName):

            with open(strInputFileName, 'r', encoding=strEncode) as fileObj:

                while fileObj.readable():
                    strFileContentItem = fileObj.read(1000)
                    if strFileContentItem != '':
                        strFileContent += strFileContentItem
                    else:
                        break
        else:
            self.logUtilObj.writerLog(strInputFileName + '文件不存在')

        return strFileContent


    def readFileContentLine(self, strInputFileName, strEncode='utf-8'):

        '''
        describe: 读取文件内容, 一行一行读取, 默认utf-8格式
        :param strInputFileName: 需要读取的文件存放路径
        :param strEncode: 文件编码格式, 默认utf-8格式
        :return: 返回文件内容, 为str类型
        '''

        strFileContent = ''

        if os.path.exists(strInputFileName):

            with open(strInputFileName, 'r', encoding=strEncode) as fileObj:

                while fileObj.readable():
                    strFileContentItem = fileObj.readline()
                    if strFileContentItem != '':
                        strFileContent += strFileContentItem
                    else:
                        break

        else:
            self.logUtilObj.writerLog(strInputFileName + '文件不存在')

        return strFileContent


    def readFileContentLineList(self, strFileName, strEncode='utf-8'):


        '''
        dsecribe: 逐行读取普通文件内容, 添加进入list集合中并返回, 一行一行读取
        add in 2018-09-18 16:57
        :param strFileName: 需要读取的文件存放路径
        :param strEncode: 文件编码格式,  默认utf-8
        :return: 返回一个list类型的集合, 元素为文件每一行的内容
        '''

        listFileContent = []

        if os.path.exists(strFileName):

            with open(strFileName, 'r', encoding=strEncode) as fileObj:

                while fileObj.readable():
                    strFileContentItem = fileObj.readline()
                    if strFileContentItem != '':
                        listFileContent.append(strFileContentItem)
                    else:
                        break

        else:
            self.logUtilObj.writerLog(strFileName + '文件不存在')

        return listFileContent



    @staticmethod
    def getLastContentForSmall(strFileName):

        '''
        describe: 读取文件的最后一行, 给小的文件使用
        add in 2018-07-05
        :param strFileName: 需要读取的文件内容
        :return: 返回文件最后一行内容, 为str类型
        '''

        with open(strFileName, 'rb') as fileObj:

            for strLine in fileObj.readlines():
                pass

        return(strLine.decode())

    @staticmethod
    def getLastContentForLarge(strFileName):

        '''
        读取文件的最后一行, 给大文件使用
        add in 2018-07-05
        :param strFileName:
        :return: 返回最后一行文件内容, 为str类型
        '''

        with open(strFileName, 'rb') as fileObj:
            fileObj.seek(-2, os.SEEK_END)

            while fileObj.read(1) != b'\n':
                fileObj.seek(-2, os.SEEK_CUR)

            return fileObj.readline().decode()

    @staticmethod
    def tailContent(strFileName):

        '''
        describe: 实现的功能类似tail -f命令读取内容, 返回迭代器
        for strContent in self.tailContent(strFileName):
            print(strContent)
        add in 2018-08-03
        :param strFileName: 需要读取的文件名, 包括路径
        :return: 迭代器,yield
        '''

        with open(strFileName, 'rb') as fileObj:
            pos = fileObj.seek(0, os.SEEK_END)
            print(pos)

            try:

                while True:
                    # currentPos = fileObj.seek(0, os.SEEK_END)
                    # print(currentPos)
                    #
                    # if currentPos > pos:
                    #     pos = fileObj.seek(0, os.SEEK_END)
                    #     continue

                    # while循环中使用sleep,休眠一点时间, 能够减少cpu消耗
                    time.sleep(0.02)


                    strLineContent = fileObj.readline()
                    if not strLineContent:
                        continue
                    else:
                        # print(strLineContent)
                        yield strLineContent.decode('utf-8').strip('\n')
            except KeyboardInterrupt:
                pass

    @staticmethod
    def writerFileContent(strFileName, strContent, whetherAdd=True):

        '''
        describe: 写入内容到文件, 这里写死了用utf-8格式写入
        :param strFileName: 文件名
        :param strContent: 需要写入的内容
        :param whetherAdd: 是否换行, 默认换行
        :return:
        '''

        if whetherAdd & True:
            with open(strFileName, 'a', encoding='utf-8') as fileObj:
                fileObj.write(strContent + '\n')
        else:
            with open(strFileName, 'a', encoding='utf-8') as fileObj:
                fileObj.write(strContent)

    @staticmethod
    def writerToFile(strFileName, strContent, whetherAdd=True):

        '''
        describe: 写入内容到指定文件
        :param strFileName: 需要写入的文件名
        :param strContent: 需要写入的内容
        :param whetherAdd: 是否清空追加, 默认True, 即默认清空追加
        :return:
        '''

        if whetherAdd & True:
            with open(strFileName, 'w', encoding='utf-8') as fileObj:
                fileObj.write(strContent)

        else:
            with open(strFileName, 'a', encoding='utf-8') as fileObj:
                fileObj.write("\n" + strContent)


    def checkAndCreateDir(self, strDirName):

        '''
        describe: 检测路径是否存放, 若不存在则创建, 支持多级
        :param strDirName: 需要检测的文件夹路径
        :return:
        '''

        if not os.path.exists(strDirName):
            os.makedirs(strDirName)
            self.logUtilObj.writerLog(strDirName + "文件夹不存在,已自动创建")
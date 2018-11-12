#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-10-24 16-23


import datetime
import time
import os

class LogUtil:

    '''
    describe: 用来做日志记录, 包含一些写入日志需要用到的函数
    '''

    def __init__(self, strLogDir):

        '''
        describe: 日志文件的名字目前只以日期来命名
        :param strLogDir: 存放日志文件的文件夹路径(支持相对路径)
        '''

        self.strLogDir = strLogDir

        # strLogFileName = self.getLogFileName()

        self.checkAndCreateDir(self.strLogDir)


    def writerLog(self, strContent, whetherAdd=True):

        '''
        describe: 写入日志, 使用utf-8的编码
        :param strContent: 需要写入的内容, 为字符串内容.这里未做类型判断,只为敦促自己使用时需要多考虑类型s
        :param whetherAdd: 是否换行, 默认换行
        :return:
        '''

        if whetherAdd & True:
            with open(self.getLogFileName(), 'a', encoding='utf-8') as fileObj:
                fileObj.write(self.getDateTimeForLog() + strContent + '\n')
        else:
            with open(self.getLogFileName(), 'a', encoding='utf-8') as fileObj:
                fileObj.write(self.getDateTimeForLog() + strContent)

        print(self.getDateTimeForLog() + strContent)


    def getTailLog(self, booleanDo):

        '''
        describe: 迭代器, 实现的功能类似tail -f命令读取日志内容
        add in 2018-08-03
        :param booleanDo:
        :return: 返回迭代器
        '''

        with open(self.getLogFileName(), 'rb') as fileObj:
            pos = fileObj.seek(0, os.SEEK_END)
            # print(pos)

            try:

                while booleanDo:

                    time.sleep(0.02)

                    # print(pos)
                    # currentPos = fileObj.seek(0, os.SEEK_END)
                    # print(currentPos)
                    #
                    # if currentPos > pos:
                    #     pos = fileObj.seek(0, os.SEEK_END)
                    #     continue

                    strLineContent = fileObj.readline()
                    if not strLineContent:
                        continue
                    else:
                        # print(strLineContent)
                        yield strLineContent.decode('utf-8').strip('\n')
            except KeyboardInterrupt:
                pass


    def getLogFileName(self):

        '''
        describe: 获取日志文件名加路径名
        :return:
        '''

        strToday = str(datetime.date.today())

        return self.strLogDir + strToday + ".log"


    def checkAndCreateDir(self, strDirName):

        '''
        describe: 检测并创建存放日志文件的文件夹路径是否存放, 若不存在则创建
        :param strDirName: 存放日志文件的文件夹路径名字
        :return:
        '''

        if not (os.path.exists(strDirName)):
            os.makedirs(strDirName)
            self.writerLog(strDirName + "文件夹不存在,已自动创建")
            self.writerLog("=================")
        else:
            self.writerLog('日志文件: ' + self.getLogFileName())

    def getDateTimeForLog(self):

        '''
        describe: 获取时间, 格式yyyy-mm-dd HH:mm:ss
        :return: 返回当前日期时间, str类型
        '''

        strTime = str(self.getTime("%Y-%m-%d %H:%M:%S"))
        return '[' + strTime + ']: '


    def getTimeForLog(self):

        '''
        describe: 获取时间, 格式yyyymmddHH
        :return: 返回当前日期时间, str类型
        '''

        strTime = str(self.getTime("%Y%m%d%H"))
        return strTime


    def getTime(self, strFormat):

        '''
        describe: 根据日期格式来获取时间日期
        :param strFormat: 时间日期格式, 如: %Y-%m-%d %H:%M:%S
        :return: 返回当前时间, str类型
        '''

        nowTime = time.localtime()
        strFormatTime = time.strftime(strFormat, nowTime)
        return strFormatTime
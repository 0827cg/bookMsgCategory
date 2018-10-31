#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-10-24 21:55

import os
import json
import configparser
from util.configMsg import ConfigMsg


class ConfigureUtil:

    '''
    describe: .conf为后缀的文件操作类, 这里用来操作配置文件
    '''

    def __init__(self, logUtilObj, strDir, strFileName):

        '''
        describe: 构造函数
        :param logUtilObj: 日志文件操作对象
        :param strDir:
        :param strFileName:
        '''

        self.logUtilObj = logUtilObj
        self.strDir = strDir
        self.strFileName = strFileName

        self.configMsgObj = ConfigMsg()

        # self.fileUtilObj = FileUtil()
        # self.strRootPath = os.getcwd()
        # self.configParserObj = configparser.ConfigParser(allow_no_value=True, delimiters=':')


    def initConfig(self, configParserObj):

        '''
        describe: 初始化配置文件, 编码格式为utf-8
        :param configParserObj: configparser的对象
        :return: 1: 初始化成功, -1: 初始化出错
        '''

        # self.fileUtilObj.checkAndCreateDir(self.strDir)
        # if not os.path.exists(self.strDir+self.strFileName):
        #     self.logUtilObj.writerLog('将初始化配置文件')

        intIndex = 0

        try:

            configParserObj.add_section(self.configMsgObj.strExportSessionName)

            configParserObj.set(self.configMsgObj.strExportSessionName, self.configMsgObj.strExportDescribe)
            configParserObj.set(self.configMsgObj.strExportSessionName, self.configMsgObj.strHtmlUrlKey,
                                self.configMsgObj.strHtmlUrlValue)
            configParserObj.set(self.configMsgObj.strExportSessionName, self.configMsgObj.strParCateGoryNameKey,
                                self.configMsgObj.strParCateGoryNameValue)

            configParserObj.set(self.configMsgObj.strExportSessionName, self.configMsgObj.strChiCategoryLabelNameKey,
                                self.configMsgObj.strChiCategoryLabelNameValue)

            configParserObj.set(self.configMsgObj.strExportSessionName, self.configMsgObj.strChiCategoryKeyNameKey,
                                self.configMsgObj.strChiCategoryKeyNameValue)

            configParserObj.set(self.configMsgObj.strExportSessionName, self.configMsgObj.strChiCateGoryNameKey,
                                self.configMsgObj.strChiCateGoryNameValue)
            configParserObj.set(self.configMsgObj.strExportSessionName, self.configMsgObj.strSpiderSleepTimeKey,
                                self.configMsgObj.strSpiderSleepTimeValue)
            configParserObj.set(self.configMsgObj.strExportSessionName, self.configMsgObj.strSaveFilePathKey,
                                self.configMsgObj.strSaveFilePathValue)


            with open(self.strDir + self.strFileName, 'w', encoding='utf-8') as configureFile:
                configParserObj.write(configureFile, space_around_delimiters=True)

        except Exception as error:

            intIndex = -1
            self.logUtilObj.writerLog('配置文件初始化出错' + str(error))

        else:

            intIndex = 1
            self.logUtilObj.writerLog('配置文件已初始化完成(' + self.strDir + self.strFileName + ')')

        return intIndex
        # else:
        #     self.logUtilObj.writerLog('配置文件已经存在(' + self.strDir + self.strFileName + ')')


    def checkAndInitConfigure(self, configParserObj):

        '''
        describe: 检测配置文件是否存在, 若存在则执行检测, 若不存在则初始化创建
        :param configParserObj: configparser的对象
        :return: 1: 存在(也可能是创建后), -1:
        '''

        # 检测配置文件是否存在, 若存在则执行检测, 若不存在则初始化创建
        # configParserObj: configparser的对象

        if not os.path.exists(self.strDir + self.strFileName):
            intIndex = self.initConfig(configParserObj)
        else:

            intIndex = self.checkConfigHasExist(configParserObj, self.configMsgObj.strExportSessionName,
                                     self.configMsgObj.listKey)

            if intIndex == 1:

                self.logUtilObj.writerLog('配置文件已经存在(' + self.strDir + self.strFileName + ')')

        return intIndex


    def getConfig(self, configParserObj):

        '''
        describe: 读取配置文件内容, 注释了不读取，值为空会读取, 读取写入的key名字全部小写
        :param configParserObj: configparser的对象
        :return: 返回一个字典
        '''

        dictConfMsg = {}
        if os.path.exists(self.strDir + self.strFileName):
            configParserObj.read(self.strDir + self.strFileName, encoding='utf-8')
            try:
                listSectionName = configParserObj.sections()
            except:

                self.logUtilObj.writerLog("读取配置文件出错")
            else:
                for sectionItem in listSectionName:

                    listKeyName = configParserObj.options(sectionItem)
                    sectionObj = configParserObj[sectionItem]

                    if len(listKeyName) != 0:
                        for keyItem in listKeyName:

                            if '#' not in keyItem:

                                valueItem = sectionObj[keyItem]
                                if valueItem is None:
                                    dictConfMsg[sectionItem] = listKeyName
                                else:
                                    dictConfMsg[keyItem] = valueItem
                            else:
                                continue
                    else:
                        dictConfMsg[sectionItem] = ''

        strConfigMsg = json.dumps(dictConfMsg, indent=3, ensure_ascii=False)
        self.logUtilObj.writerLog('配置文件中读取到的配置有: ' + strConfigMsg)
        return dictConfMsg

    def updateConfigSingleKey(self, configParserObj, strSessionName, strKey, strValue):

        '''
        修改改配置文件, 针对单个key
        :param configParserObj: configparser的对象
        :param strSessionName: 需要更改的strKey对应的上一级名字
        :param strKey: 需要更改的key
        :param strValue: 需要更改的strKey的值
        :return:
        '''

        try:
            configParserObj.set(strSessionName, strKey, strValue)
            with open(self.strDir + self.strFileName, 'w', encoding='utf-8') as configureFile:
                configParserObj.write(configureFile, space_around_delimiters=True)
        except:
            self.logUtilObj.writerLog('更新修改出错: [' + strSessionName + ']' + strKey + ' = ' + strValue)
        else:
            self.logUtilObj.writerLog('已更新修改: [' + strSessionName + ']' + strKey + ' = ' + strValue)


    def updateConfigSingleSession(self, configParserObj, strSessionName, dictMsg):

        '''
        describe: 修改配置文件, 针对单个session块
        :param configParserObj: configparser的对象
        :param strSessionName: 块名字
        :param dictMsg: 块对应的新内容, 字典类型
        :return:
        '''

        configParserObj.read(self.strDir + self.strFileName)
        try:
            for strKey, strValue in dictMsg.items():
                configParserObj.set(strSessionName, strKey, strValue)

            with open(self.strDir + self.strFileName, 'w', encoding='utf-8') as configureFile:
                configParserObj.write(configureFile, space_around_delimiters=True)
        except:
            self.logUtilObj.writerLog('更新修改出错')
        else:
            self.logUtilObj.writerLog('已经更新修改: [' + strSessionName + ']配置块')


    def checkConfigHasExist(self, configParserObj, strSession, listKey):


        '''
        describe: 检测判断配置文件中是否存在session块配置信息,及配置信息的key是否完全
        :param configParserObj: configparser的对象
        :param strSession: 块名字
        :param listKey: list类型, 其元素为strSession块中的配置项的key名字
        :return: 1: 检查的配置项存在, -1: session配置块存在, 但缺少某项key, -2: session配置块不存在
        '''

        intIndex = 0

        configParserObj.read(self.strDir + self.strFileName, encoding='utf-8')
        if configParserObj.has_section(strSession):

            for strKeyItem in listKey:
                if not configParserObj.has_option(strSession, strKeyItem):
                    self.logUtilObj.writerLog('配置文件中的' + strSession + '配置中' + strKeyItem + '的配置项不存在')
                    intIndex = -1
                    break
                else:
                    intIndex = 1
                    pass
        else:
            intIndex = -2
            self.logUtilObj.writerLog('配置文件中不存在' + strSession + '的配置块')

        return intIndex


    @staticmethod
    def getCustomizeConfigParserObj():

        '''
        describe: 静态方法, 获取configparser对象, 返回一个实例化的configparser对象, 实例化时参数可改, 参数的配置需要根据自己的需求
        :return:
        '''

        return configparser.ConfigParser(allow_no_value=True, delimiters=':')

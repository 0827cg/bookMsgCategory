#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-10-24 21:55


import os

class ConfigMsg:

    '''
    describe: 配置文件的一些key名字和初始化的值
    '''

    strExportSessionName = 'Spider Configure'
    strExportDescribe = '# spider dangdang'

    strHtmlUrlKey = 'html_url'
    strParCateGoryNameKey = 'p_category_name'
    strChiCategoryLabelNameKey = 'c_category_label'
    strChiCategoryKeyNameKey = 'c_category_key'
    strChiCateGoryNameKey = 'c_category_name'
    strSpiderSleepTimeKey = 'sleep_time'
    strSaveFilePathKey = 'save_path'


    strHtmlUrlValue = "http://category.dangdang.com/cp01.54.00.00.00.00.html"
    strParCateGoryNameValue = "计算机/网络"
    strChiCategoryLabelNameValue = 'span'
    strChiCategoryKeyNameValue = 'title'
    strChiCateGoryNameValue = "[图形图像多媒体, 程序设计, 网络与数据通信, 数据库, 家庭与办公室用书]"
    strSpiderSleepTimeValue = '3'
    strSaveFilePathValue = 'output' + os.sep


    listKey = [strHtmlUrlKey, strParCateGoryNameKey, strChiCategoryLabelNameKey, strChiCategoryKeyNameKey,
               strChiCateGoryNameKey, strSpiderSleepTimeKey, strSaveFilePathKey]



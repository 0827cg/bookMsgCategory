#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-10-26 11-13

'''
describe: 爬取当当网上的图书信息, 即根据图书标签
情景描述如: url: http://category.dangdang.com/cp01.54.00.00.00.00.html
程序将访问该页面, 获取页面中的标签的url, 具体需要获取的标签存放在配置文件中, 如[图形图像多媒体, 程序设计, 网络与数据通信, 数据库, 家庭与办公室用书]
获取到各个标签对应的url后, 将遍历访问url, 访问的同时去获取当前url下的图书信息, 再判断该页面是否存在下一页url, 如存在, 将进行下一页的图书信息爬取


不足:
    1. 目前配置文件中的sleep_time并为用到, 因为此时的程序运行时打印的耗时间隔有1~2s左右, 所以间隔也不会太小, 因此并为设置休眠--add in 2018-10-31 10:53
    2. 目前程序运行(爬取500张页面并获取信息)大概耗时18分钟, 效率上来说还是很慢, 当然也不能太快, 但就是还有需要改进的地方--add in 2018-10-31 10:56
'''



from operatorBin.operatorMsg import OperatorMsg


def main():

    OperatorMsg()


if __name__ == '__main__':
    main()
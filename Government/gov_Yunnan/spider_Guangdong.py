# -*- coding:utf-8 -*-
# -*- created by: yongzhuo -*-


'http://lygl.gd.gov.cn/?c=index&a=letterlist&page=2'

import re
import requests
from bs4 import BeautifulSoup
import requests
from lxml import etree
import pickle
import time
import datetime


Cookie = 'Cookie需要自己加，可使用浏览器上的'

def txtRead(filePath, encodeType = 'utf-8'):
    '''读取txt文件'''
    listLine = []
    try:
        file = open(filePath, 'r', encoding= encodeType)

        while True:
            line = file.readline()
            if not line:
                break

            listLine.append(line)

        file.close()

    except Exception as e:
        print(str(e))

    finally:
        return listLine


def txtWrite(listLine, filePath, type = 'w',encodeType='utf-8'):
    '''读取txt文件'''
    try:
        file = open(filePath, type, encoding=encodeType)
        file.writelines(listLine)
        file.close()

    except Exception as e:
        print(str(e))

#广东政务
def process_guangdong(addr):
    headers = {
        "Host": 'lygl.gd.gov.cn',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        "Accept-Language": 'zh-CN,zh;q=0.9',
        "Accept-Encoding": 'gzip, deflate',
        "Connection": 'keep-alive',
        "Cookie": Cookie
    }



    res = requests.get(addr, headers=headers)
    # print(res.content)
    html_content = res.content.decode('UTF-8')
    # print(html_content)

    html = etree.HTML(html_content)
    # html.xpath('//td[@class="title"]//text()')
    # tableCont = html.xpath('//tr[@class="tableCont"]//text()')
    tableCont = html.xpath('//ul[@class="gllist"]//li//a//text()')

    t_all = []
    for tableCont_0 in tableCont:
        t_all.append(tableCont_0.strip() + '\n')
    return t_all

#存储数据，表名
def operation_process_guangdong():
    res_list = []
    num_count = 0 #初始时候， numcount出错
    for i in range(83):
        num_count = num_count + 1

        addr = 'http://lygl.gd.gov.cn/?c=index&a=letterlist&page=' + str(num_count)
        t_all = process_guangdong(addr)
        print(num_count)
        res_list = res_list + t_all
        txtWrite(res_list, '省长.txt', type='a+')
        res_list = []

operation_process_guangdong()


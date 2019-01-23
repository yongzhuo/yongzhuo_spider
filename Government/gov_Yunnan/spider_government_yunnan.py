# -*- coding:utf-8 -*-
# -*- created by: yongzhuo -*-

import requests
from lxml import etree
import pickle
import time
import datetime

'''注意:   Cookie需要自己加'''
Cookie = '******注意:   Cookie需要自己加'



def txtRead(filePath, encodeType='utf-8'):
    '''读取txt文件'''
    listLine = []
    try:
        file = open(filePath, 'r', encoding=encodeType)

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


def txtWrite(listLine, filePath, type='w', encodeType='utf-8'):
    '''读取txt文件'''
    try:
        file = open(filePath, type, encoding=encodeType)
        file.writelines(listLine)
        file.close()

    except Exception as e:
        print(str(e))


def is_valid_date(strdate):
    '''判断是否是一个有效的日期字符串'''
    try:
        if ":" in strdate:
            time.strptime(strdate, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(strdate, "%Y-%m-%d")
        return True
    except:
        return False


# 分城市，昆明
# 公众问题
def process_city_2(addr):
    headers = {
        "Host": 'xxcx.yn.gov.cn',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        "Accept-Language": 'zh-CN,zh;q=0.9',
        "Accept-Encoding": 'gzip, deflate',
        "Connection": 'keep-alive',
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "Cookie": Cookie
    }

    res = requests.get(addr, headers=headers)
    # print(res.content)
    html_content = res.content.decode('gb2312', 'ignore')
    html = etree.HTML(html_content)
    # html.xpath('//td[@class="title"]//text()')
    # tableCont = html.xpath('//tr[@class="tableCont"]//text()')
    tableCont_herf = html.xpath('//tr[@height="33px"]/td[@width="50%"]//a//@href')
    tableCont = html.xpath('//tr[@height="33px"]/td//text()')

    t_all = []
    t_list_one = []
    for tableCont_0 in tableCont:
        tableCont_0_replace = tableCont_0.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        if tableCont_0_replace == '':
            continue
        if t_all:
            len_p = len(t_all)
        else:
            len_p = 0

        t_list_one.append(tableCont_0)
        if is_valid_date(tableCont_0):
            if len(t_list_one) == 3:
                t_list_one.append(tableCont_0)
                t_list_one.append(tableCont_herf[len_p])
                t_all.append('momomomo'.join(t_list_one) + '\n')
            if len(t_list_one) == 4:
                t_list_one.append(tableCont_herf[len_p])
                t_all.append('momomomo'.join(t_list_one) + '\n')
            t_list_one = []
    return t_all


def process_qa_city_2(addr=None):
    headers = {
        "Host": 'xxcx.yn.gov.cn',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        "Accept-Language": 'zh-CN,zh;q=0.9',
        "Accept-Encoding": 'gzip, deflate',
        "Connection": 'keep-alive',
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "Cookie": Cookie
    }

    res = requests.get(addr, headers=headers)
    # print(res.content)
    html_content = res.content.decode('gb2312', 'ignore')
    html = etree.HTML(html_content)
    # html.xpath('//td[@class="title"]//text()')
    # tableCont = html.xpath('//tr[@class="tableCont"]//text()')

    try:
        qas = html.xpath('//tbody//tr//td[@colspan="3"]//text()')
        question = qas[0]
        answer = qas[1]
        # answer = html.xpath('//div[@class="adminRep "]//text()')
    except Exception as e:
        print('addr: ' + addr)

    if not answer:
        answer = "noanswer"

    return ''.join(question).replace('\r\n', '').replace('\n', '').replace(' ', '').replace('\t', ''), ''.join(
        answer).replace('\r\n', '').replace('\n', '').replace(' ', '').replace('\t', '')


def operation_process_qa_city_2_1():
    # urls = txtRead('load/昆明市公众问题.txt')
    urls = txtRead('load/昆明市常见问题.txt')

    qat_list = []
    for url in urls:
        url_a = url
        url_list = url_a.strip().split('momomomo')
        qa_url = 'http://xxcx.yn.gov.cn/faq/' + url_list[3]
        question, answer = process_qa_city_2(qa_url)
        url_list.append(question)
        url_list.append(answer)
        qat_one = 'momomomo'.join(url_list)
        qat_list.append(qat_one + '\n ')
        print(len(qat_list))
        if len(qat_list) / 250 == 0:
            txtWrite(qat_list, 'load/qa_昆明市常见问题.txt')
    output = open('load/qa.pickle', 'wb')
    pickle.dump(qat_list, output)

    txtWrite(qat_list, 'load/qa_昆明市常见问题.txt')


# 常见问题
def process_city_2_1(addr):
    headers = {
        "Host": 'xxcx.yn.gov.cn',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        "Accept-Language": 'zh-CN,zh;q=0.9',
        "Accept-Encoding": 'gzip, deflate',
        "Connection": 'keep-alive',
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "Cookie": Cookie
    }

    res = requests.get(addr, headers=headers)
    # print(res.content)
    html_content = res.content.decode('gb2312', 'ignore')
    html = etree.HTML(html_content)
    # html.xpath('//td[@class="title"]//text()')
    # tableCont = html.xpath('//tr[@class="tableCont"]//text()')
    tableCont_herf = html.xpath('//tr[@height="33px"]/td[@width="50%"]//a//@href')
    tableCont = html.xpath('//tr[@height="33px"]/td//text()')

    t_all = []
    t_list_one = []
    for tableCont_0 in tableCont:
        tableCont_0_replace = tableCont_0.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        if tableCont_0_replace == '':
            continue
        if t_all:
            len_p = len(t_all)
        else:
            len_p = 0

        t_list_one.append(tableCont_0)
        if not t_list_one or len(t_list_one) == 3:
            t_list_one.append(tableCont_herf[len_p])
            t_all.append('momomomo'.join(t_list_one) + '\n')
            t_list_one = []
    return t_all


# 存储数据，表名
def operation_process_city_2():
    res_list = []
    # for num_count in range(680):
    # num_count = 2095
    # for i in range(13653-2095):
    # 常见27-322-1200-1923-2790-4534-4796-5342
    # 公众80-699-824-1042-1528-2302-2506-2833-3430-4397-4553-4927-5210-6629-7257-7446-7924-8557-9503-9939-10665-10815-10935-11116-11969-12185-13057
    num_count = 0
    for i in range(13057):
        num_count = num_count + 1
        # 常见
        # addr = 'http://xxcx.yn.gov.cn/faq/areagg_gzwt.jsp?page1=' + str(num_count) + '&partment=null&title=null&person=null&type=null&startdate=null&enddate=null&zhg=null&xzqid=8981'
        # addr = 'http://xxcx.yn.gov.cn/faq/areagg_gzwt.jsp?page1=' + str(num_count) +'&partment=null&title=null&person=null&type=null&startdate=null&enddate=null&zhg=null&xzqid=1'
        # 公众
        # addr = 'http://xxcx.yn.gov.cn/faq/areagg_cjwt.jsp?enty=null&page2=' + str(num_count) +'&partment=null&title=null&person=null&type=null&startdate=null&enddate=null&zhg=null&xzqid=8981'
        addr = 'http://xxcx.yn.gov.cn/faq/areagg_cjwt.jsp?enty=null&page2=' + str(num_count) + '&partment=null&title=null&person=null&type=null&startdate=null&enddate=null&zhg=null&xzqid=1'
        t_all = process_city_2_1(addr)
        print(num_count)
        # print(t_all)
        res_list = res_list + t_all
        # txtWrite(res_list, 'load/昆明市公众问题.txt')
        # txtWrite(res_list, 'load/常见提问_95565.txt', type='a+')
        txtWrite(res_list, '分部门_公众提问_13653.txt', type='a+')
        # time.sleep(1000)
        res_list = []
        # if num_count % 1000 == 0:
        #     time.sleep(60000)

        qat_list = []
        for url in t_all:
            url_a = url
            url_list = url_a.strip().split('momomomo')
            qa_url = 'http://xxcx.yn.gov.cn/faq/' + url_list[3]
            question, answer = process_qa_city_2(qa_url)
            url_list.append(question)
            url_list.append(answer)
            qat_one = 'momomomo'.join(url_list)
            qat_list.append(qat_one + '\n ')
            print(str(len(qat_list)) + '  question: ' + question)
        txtWrite(qat_list, 'q_a_昆明市公众问题_95565_20190109.txt', type='a+')
        # print('sleep')
        print(datetime.datetime.now())
        # time.sleep(6)


print('''注意:   Cookie需要自己加''')
operation_process_city_2()
print('''注意:   Cookie需要自己加, 否则报错UnicodeEncodeError: 'latin-1' codec can't encode characters in position 6-10: ordinal not in range(256)''')

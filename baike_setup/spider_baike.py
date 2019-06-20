# -*- coding:utf-8 -*-
# -*- created by: yongzhuo -*-


import requests
from lxml import etree




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

#
def process_sheup(addr, addr_l):
    headers = {
        "Host": 'www.sheup.net',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        "Accept-Language": 'zh-CN,zh;q=0.9',
        "Accept-Encoding": 'gzip, deflate',
        "Connection": 'keep-alive',
        'Referer': addr,
        'Upgrade-Insecure-Requests': '1'
    }


    res = requests.get(addr + addr_l, headers=headers)
    # print(res.content)
    html_content = res.content.decode('gb2312')
    # print(html_content)

    html = etree.HTML(html_content)
    # html.xpath('//td[@class="title"]//text()')
    # tableCont = html.xpath('//tr[@class="tableCont"]//text()')
    # print(html)
    tableCont = html.xpath('//div[@class="main_text2"]//div[@class="tiku_2"]//p//a//@href')

    t_all = []
    for tableCont_0 in tableCont:
        t_all.append(tableCont_0.strip() + '\n')
    return t_all


def process_sheup_ot(addr):
    headers = {
        "Host": 'www.sheup.net',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        "Accept-Language": 'zh-CN,zh;q=0.9',
        "Accept-Encoding": 'gzip, deflate',
        "Connection": 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }


    res = requests.get(addr, headers=headers)
    # print(res.content)
    html_content = res.content.decode('gb2312')
    # print(html_content)

    html = etree.HTML(html_content)
    # html.xpath('//td[@class="title"]//text()')
    # tableCont = html.xpath('//tr[@class="tableCont"]//text()')
    # print(html)
    tableConts1 = html.xpath('//div[@class="text1_s"]//div[@class="text1_s_info"]//p//text()')
    ques = tableConts1[5]
    tableConts2 = html.xpath('//div[@class="text1_s"]//div[@class="text1_s_info"]//div[@class="tiku_answer"]//p//text()')
    answer = tableConts2[1]
    return ques, answer

#存储数据，表名
def operation_process_sheup():
    for j in range(20):
        res_list = []
        j = j + 1
        qa = []
        num_count = 0  # 初始时候， numcount出错
        for i in range(150):
            num_count = num_count + 1
            addr = 'http://www.sheup.net/info_tiku_4.php?type={}'.format(j+1)
            addr_l = '&page={}'.format(num_count)
            try:
                t_all = process_sheup(addr, addr_l)
            except:
                continue
            print(num_count)
            if t_all:
                res_list = res_list + t_all
        print('url{}'.format(j))
        count = 0
        for url in res_list:
            count += 1
            print(count)
            addr = 'http://www.sheup.net/' + url.strip()
            try:
                q, a = process_sheup_ot(addr)
                print(q) # 有时候会报错，格式不对
                print(a)
            except:
                continue
            qa.append(q.replace('\n','') + 'momo'+ a.replace('\n','') + '\n')
            if count%50==0:
                txtWrite(qa, '{}'.format(j) + '.txt', type ='a+')
                qa = []

        txtWrite(qa, '{}'.format(j) + '.txt', type ='a+')

operation_process_sheup()

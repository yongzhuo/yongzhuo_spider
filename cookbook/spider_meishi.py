'''
美食节 各地小吃爬虫
主页url:  http://www.meishij.net/
排行榜url： http://top.meishi.cc/lanmu.php?cid=78
'''

# 导入相关库
import requests
from bs4 import BeautifulSoup
import bs4
from lxml import etree


def get_html_text(url):
    '''获取html文本'''
    try:
        r = requests.get(url, timeout=3)
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'

def parse_type(url):
    html = get_html_text(url)
    # 做一个简单的判断
    if html != 'error':
        html = etree.HTML(html)
        tableCont_herf = html.xpath('//div[@class ="dww clearfix dww_cpdq"]//div//dl//dd//@href')
    return tableCont_herf

def parse_city_id(url):
    '''解析对应的城市排行榜连接'''

    html = get_html_text(url)
    # 做一个简单的判断
    if html != 'error':
        try:
            html = etree.HTML(html)
            tableCont_herf = html.xpath('//div[@class="listtyle1"]//a//@href')
            tableCont_title = html.xpath('//div[@class="listtyle1"]//a//@title')
            tableCont_li1 = html.xpath('//div[@class="listtyle1"]//a//div//div//ul//li[@class="li1"]//text()')
            tableCont_li2 = html.xpath('//div[@class="listtyle1"]//a//div//div//ul//li[@class="li2"]//text()')
            len_size = len(tableCont_herf)

            last_data = []
            for size in range(len_size):
                last_data.append([tableCont_title[size], tableCont_li1[size], tableCont_li2[size], tableCont_herf[size]])

            return last_data
        except:
            return None
        # soup = BeautifulSoup(html, 'lxml')
        # # 定位到 全国各地特色小吃排行榜分类,<div>
        # cityids = soup.find('div', class_='listtyle1_list clearfix')
        # for city in cityids.find_all('listtyle1'):
        #
        #     res.append({'title': city['title'], 'url': city['href']})
        # return res
    else:
        print('error !!!!')


def parse_food_info(url):
    '''解析对应的美食信息'''

    html = get_html_text(url)

    if html != 'error':
        try:
            html = etree.HTML(html)
            tableCont_step = html.xpath('//div[@class="content clearfix"]//div[@class="c"]//p//text()')
            tableCont_main_item = html.xpath('//div[@class="materials_box"]//div//ul//li//div[@class="c"]//h4//a//text()')
            tableCont_main_many = html.xpath('//div[@class="materials_box"]//div//ul//li//div[@class="c"]//h4//span//text()')
            tableCont_ot_item = html.xpath('//div[@class="materials_box"]//div//ul//li//div[@class="c"]//h4//a//text()')
            tableCont_ot_many = html.xpath('//div[@class="materials_box"]//div//ul//li//div[@class="c"]//span//text()')

            main_item = []
            length1 = len(tableCont_main_item)
            for item in range(length1):
                main_item.append(tableCont_main_item[item] + tableCont_main_many[item])

            main_ot = []
            length2 = len(tableCont_ot_item)
            for item in range(length2):
                main_ot.append(tableCont_ot_item[item] + tableCont_ot_many[item])

            last_data = ' '.join(main_item) + 'momom' +'  '.join(main_ot) + 'momom' + ';'.join(tableCont_step)

            return last_data
        except:
            return None

        # soup = BeautifulSoup(html, 'lxml')
        # # 定位到具体排行榜的位置
        # foods = soup.find('div', class_='rank_content_top10_wraper')
        # # 开始解析信息
        # for food in foods.find_all('li'):
        #     # 寻找 食品名、做法链接、图片链接
        #     content = food.find('a', class_='img')
        #     name = content['title']
        #     detial_url = content['href']
        #     img_url = content.img['src']
        #     print('正在解析美食：{}'.format(name))
        #     # 构造一个生成器，分别返回 食物名,做法链接,图片链接
        #     yield name, detial_url, img_url
    else:
        print('error !!!!')


'''读取txt文件'''
def txtRead(filePath, encodeType = 'utf-8'):
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

'''读取txt文件'''
def txtWrite(listLine, filePath, type = 'w',encodeType='utf-8'):

    try:
        file = open(filePath, type, encoding=encodeType)
        file.writelines(listLine)
        file.close()

    except Exception as e:
        print(str(e))


def main():
    '''程序入口'''
    # 构造所有起始url列表
    # url_list = [
    #     'https://www.meishij.net/chufang/diy/jiangchangcaipu/',
    #     "https://www.meishij.net/chufang/diy/langcaipu/",
    #     "https://www.meishij.net/chufang/diy/sushi/",
    #     "https://www.meishij.net/chufang/diy/wancan/",
    #     "https://www.meishij.net/chufang/diy/sijiacai/",
    #     "https://www.meishij.net/chufang/diy/recaipu/",
    #
    #
    #
    # ]#[Home_food_url]#, Top_food_url, China_food_url, Foreign_food_url]

    url_list = parse_type('https://www.meishij.net/chufang/diy/jiangchangcaipu/')

    url_list = [url + '\n' for url in url_list]

    url_list1 = []
    for url in url_list:
        for i in range(56):
            if i != 0:
                url_list1.append(url.strip() + '?&page=' + str(i))

    txtWrite(url_list, 'meishi_2.txt', 'a+')

    print(url_list1)
    # 找到所有城市排行榜的url
    for url in url_list1:
        # 找到该分类下的所有cid
        res = parse_city_id(url)
        if res:
            cookbook = []
            for page in res:
                # 利用生成器迭代返回结果
                datas = parse_food_info(page[3])
                if datas:
                    ggo = url.replace('https://www.meishij.net/', '') + 'momom' + 'momom'.join(page) + 'momom' + datas
                    cookbook.append(ggo.replace('\n', '') + '\n')
                    print(ggo)

            txtWrite(cookbook, 'meishi_2.txt', 'a+')



main()

# 爬取酷漫屋漫画 http://m.kuman55.com/
# 以下载《仙逆》为例
# http://m.kuman55.com/12168/
# 版本：v1 直接上多线程

import os
import requests
import random
import json
import time
from lxml import etree
import threading
from queue import LifoQueue
import base64
import openpyxl

# headers，访问头部信息
USER_AGENT_LIST = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]
# 可用代理池
with open("zdaye_available.txt", "r") as f:
    proxies_pool = json.load(f)
print(len(proxies_pool))

# 判断一下表格是否已经存在，不存在就新建一个
if not os.path.exists('error.xlsx'):
    wb = openpyxl.Workbook()
else:
    wb = openpyxl.load_workbook('error.xlsx')
ws = wb.active


class Spider(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)

    def run(self):
        global proxies_pool
        # global chapters_name_url_queue
        while True:
            if chapters_name_url_queue.empty():  # 如果队列为空
                break
            # queueLock.acquire()
            i_chapter, chapter_name, chapter_url = chapters_name_url_queue.get()  # 弹出一个队列
            # queueLock.release()
            # 随机选择一个headers
            USER_AGENT = random.choice(USER_AGENT_LIST)
            headers = {'user-agent': USER_AGENT}
            # 先随机选择一个代理，不出意外是下载一章换一个代理
            proxies = random.choice(proxies_pool)
            proxies = {"http": "http://" + proxies, "https": "http://" + proxies}
            # 写个死循环让这一章的漫画都下载完
            chapter_start = time.time()
            while True:
                if time.time() - chapter_start > 1:
                    ws.append((i_chapter, chapter_name, chapter_url))
                    break
                try:
                    response = requests.get(chapter_url, headers=headers, proxies=proxies, timeout=3)
                    response_etree = etree.HTML(response.text)
                    image_url_base64 = response_etree.xpath('/html/body/script[2]/text()')[0].split('\'')[-2]
                    image_url_list = json.loads(base64.b64decode(image_url_base64).decode("utf-8").replace('\/', '/').replace('\\r', ''))
                    for num, one_picture in enumerate(image_url_list):
                        start = time.time()
                        self.download_one_picture(headers, proxies, i_chapter, chapter_name, one_picture)
                        print(i_chapter, num + 1, chapter_name, 'is download__try1, time:', time.time() - start)
                        # 如果时间很短，说明代理很好，将其添加到代理池中，虽然重复了，但随机到它的概率大了
                        if time.time() - start < 2:
                            try:
                                proxies_pool.append(proxies['http'].split('//')[1])
                            except Exception as e:
                                print('添加失败')
                    break
                except Exception as e:
                    try:
                        response = requests.get(chapter_url, headers=headers, proxies=proxies, timeout=1)
                        response_etree = etree.HTML(response.text)
                        image_url_base64 = response_etree.xpath('/html/body/script[2]/text()')[0].split('\'')[-2]
                        image_url_list = json.loads(base64.b64decode(image_url_base64).decode("utf-8").replace('\/', '/').replace('\\r', ''))
                        for num, one_picture in enumerate(image_url_list):
                            start = time.time()
                            self.download_one_picture(headers, proxies, i_chapter, chapter_name, one_picture)
                            print(i_chapter, num + 1, chapter_name, 'is download__try2, time:', time.time() - start)
                            if time.time() - start < 2:
                                try:
                                    proxies_pool.append(proxies['http'].split('//')[1])
                                except Exception as e:
                                    print('添加失败')
                        break
                    except Exception as e:
                        try:
                            response = requests.get(chapter_url, headers=headers, proxies=proxies, timeout=1)
                            response_etree = etree.HTML(response.text)
                            image_url_base64 = response_etree.xpath('/html/body/script[2]/text()')[0].split('\'')[-2]
                            image_url_list = json.loads(base64.b64decode(image_url_base64).decode("utf-8").replace('\/', '/').replace('\\r', ''))
                            for num, one_picture in enumerate(image_url_list):
                                start = time.time()
                                self.download_one_picture(headers, proxies, i_chapter, chapter_name, one_picture)
                                print(i_chapter, num + 1, chapter_name, 'is download__try3, time:', time.time() - start)
                                if time.time() - start < 2:
                                    try:
                                        proxies_pool.append(proxies['http'].split('//')[1])
                                    except Exception as e:
                                        print('添加失败')
                            break
                        except Exception as e:
                            try:  # 已经给了这个代理三次机会了，太不争气了，从代理池中删除他
                                proxies_pool.remove(proxies['http'].split('//')[1])
                                print('remove because _chapter_:', proxies, 'len(proxies_pool):', len(proxies_pool))
                            except Exception as e:
                                if len(proxies_pool) == 0:
                                    print('当前代理池为空，运行程序前请准备足够的代理池')
                                    # 重置一下代理池
                                    queueLock.acquire()
                                    with open("zdaye_available.txt", "r") as f:
                                        proxies_pool = json.load(f)
                                    queueLock.release()
                                USER_AGENT = random.choice(USER_AGENT_LIST)
                                headers = {'user-agent': USER_AGENT}
                                proxies = random.choice(proxies_pool)
                                proxies = {"http": "http://" + proxies, "https": "http://" + proxies}
                                # print('new proxies:', proxies)
                                continue

    def download_one_picture(self, headers, proxies, i_chapter, chapter_name, one_picture):
        global proxies_pool
        page, one_picture_url = one_picture.split('|')
        # 写个死循环确保这张漫画下载完成
        this_picture_start = time.time()
        while True:
            if time.time() - this_picture_start > 0.1:  # 下载一张图片的时间过长
                ws.append((i_chapter, chapter_name, page, one_picture_url))
                print(i_chapter, chapter_name, page, one_picture_url, '下载时间过长!!')
                break
            try:
                image = requests.get(one_picture_url, headers=headers, proxies=proxies, timeout=1)
                with open(outputs + '{0:0>3}_{1:0>2}_{2}.jpg'.format(i_chapter, int(page), chapter_name), 'wb') as file:
                    file.write(image.content)
                break
            except Exception as e:
                try:
                    image = requests.get(one_picture_url, headers=headers, proxies=proxies, timeout=1)
                    with open(outputs + '{0:0>3}_{1:0>2}_{2}.jpg'.format(i_chapter, int(page), chapter_name),
                              'wb') as file:
                        file.write(image.content)
                    break
                except Exception as e:
                    try:
                        image = requests.get(one_picture_url, headers=headers, proxies=proxies, timeout=1)
                        with open(outputs + '{0:0>3}_{1:0>2}_{2}.jpg'.format(i_chapter, int(page), chapter_name),
                                  'wb') as file:
                            file.write(image.content)
                        break
                    except Exception as e:
                        try:  # 已经给了这个代理三次机会了，太不争气了，从代理池中删除它
                            proxies_pool.remove(proxies['http'].split('//')[1])
                            print('remove because *picture*:', proxies, 'len(proxies_pool):', len(proxies_pool))
                        except Exception as e:
                            if len(proxies_pool) == 0:
                                print('当前代理池为空，运行程序前请准备足够的代理池')
                                # 重置一下代理池
                                queueLock.acquire()
                                with open("zdaye_available.txt", "r") as f:
                                    proxies_pool = json.load(f)
                                queueLock.release()
                            USER_AGENT = random.choice(USER_AGENT_LIST)
                            headers = {'user-agent': USER_AGENT}
                            proxies = random.choice(proxies_pool)
                            proxies = {"http": "http://" + proxies, "https": "http://" + proxies}
                            # print('new proxies:', proxies)
                            continue


# 漫画id，想下载该网站其他漫画只需要修改此处即可,其他的不用修改
# comic_id = 12168
comic_id = 22323
# 漫画目录页，但目录只有20个，不全
contents_url = f'http://m.kuman55.com/{comic_id}/'
# 点击查看更多加载的剩余的目录
rest_contents = f'http://m.kuman55.com/bookchapter/?id={comic_id}&id2=1'
# 输出位置,默认程序所在的路径下outputs文件夹
outputs = './outputs/'
# 如果输出文件夹不存在就新建一个
if not os.path.exists(outputs):
    os.makedirs(outputs)
# 随机选择一个headers
USER_AGENT0 = random.choice(USER_AGENT_LIST)
headers0 = {'user-agent': USER_AGENT0}
response0 = requests.get(contents_url, headers=headers0)
# print(response.text)
response_etree0 = etree.HTML(response0.text)
# xpath定位
chapters = response_etree0.xpath('//ul[@id="chapterList_ul_1"]/li')
# 获取剩下的目录
rest_response = requests.get(rest_contents, headers=headers0).json()
total_chapters_num = len(chapters) + len(rest_response)
print('total_chapters_num:', total_chapters_num)
# 一个后入先出得队列存放：序号，章节名称，章节网址
chapters_name_url_queue = LifoQueue(total_chapters_num)
for i, chapter in enumerate(chapters):
    # 该章节名称
    chapter_name_ = chapter.xpath('./a/text()')[0].replace(' ', '_')
    # 该章节不完整链接
    chapter_url0 = chapter.xpath('./a/@href')[0]
    # 该章节完整链接
    chapter_url1 = 'http://m.kuman55.com' + chapter_url0
    print(total_chapters_num - i, chapter_name_, chapter_url1, 'put in queue')
    chapters_name_url_queue.put((total_chapters_num - i, chapter_name_, chapter_url1))
rest_num = len(rest_response)
for j, chapter in enumerate(rest_response):
    chapter_name_ = chapter['name'].replace(' ', '_')
    chapter_url1 = f'http://m.kuman55.com/{comic_id}/' + chapter['id'] + '.html'
    print(rest_num - j, chapter_name_, chapter_url1, 'put in queue')
    chapters_name_url_queue.put((rest_num - j, chapter_name_, chapter_url1))
queueLock = threading.Lock()
# 起10个线程
threads = []
for k in range(20):
    thread = Spider()
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()
wb.save('error.xlsx')
print('Finish')

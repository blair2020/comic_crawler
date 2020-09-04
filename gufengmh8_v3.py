# 从古风漫画网爬取漫画
# 网址：https://m.gufengmh8.com/
# 以下载《从前有座灵剑山》为例
# 网址：https://m.gufengmh8.com/manhua/congqianyouzuolingjianshan/
# 版本：v3 对v2增加多线程

import requests
import random
import json
from lxml import etree
import threading
from queue import Queue

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
            page = 1  # 初始为该章节第一页
            # 随机选择一个headers
            USER_AGENT = random.choice(USER_AGENT_LIST)
            headers = {'user-agent': USER_AGENT}
            # 先随机选择一个代理，不出意外是下载一章换一个代理
            proxies = random.choice(proxies_pool)
            # 因为不确定每个章节有多少页，写个死循环
            while True:
                comic_url = chapter_url.replace('.html', '-{}.html'.format(page))
                while True:
                    try:
                        response = requests.get(comic_url, headers=headers, proxies=proxies, timeout=4)
                        response_etree = etree.HTML(response.text)
                        image_url = response_etree.xpath('//div[@id="chapter-view"]/div[4]/div[1]/a/img/@src')[0]
                        image = requests.get(image_url, headers=headers, proxies=proxies, timeout=4)
                        signal = response_etree.xpath('//div[@id="action"]/ul/li[3]/a/@href')[0]
                        break
                    except Exception as e:
                        try:
                            response = requests.get(comic_url, headers=headers, proxies=proxies, timeout=4)
                            response_etree = etree.HTML(response.text)
                            image_url = response_etree.xpath('//div[@id="chapter-view"]/div[4]/div[1]/a/img/@src')[0]
                            image = requests.get(image_url, headers=headers, proxies=proxies, timeout=4)
                            signal = response_etree.xpath('//div[@id="action"]/ul/li[3]/a/@href')[0]
                            break
                        except Exception as e:
                            try:
                                response = requests.get(comic_url, headers=headers, proxies=proxies, timeout=4)
                                response_etree = etree.HTML(response.text)
                                image_url = response_etree.xpath('//div[@id="chapter-view"]/div[4]/div[1]/a/img/@src')[0]
                                image = requests.get(image_url, headers=headers, proxies=proxies, timeout=4)
                                signal = response_etree.xpath('//div[@id="action"]/ul/li[3]/a/@href')[0]
                                break
                            except Exception as e:  # 给了三次机会，仍然不行就删掉
                                try:
                                    proxies_pool.remove(proxies)
                                    print('remove:', proxies, 'len(proxies_pool):', len(proxies_pool))
                                except Exception as e:
                                    if len(proxies_pool) == 0:
                                        print('当前代理池为空，运行程序前请准备足够的代理池')
                                        # 重置一下代理池
                                        with open("zdaye_available.txt", "r") as f:
                                            proxies_pool = json.load(f)
                                    USER_AGENT = random.choice(USER_AGENT_LIST)
                                    headers = {'user-agent': USER_AGENT}
                                    proxies = random.choice(proxies_pool)
                                    print('new proxies:', proxies)
                                    continue
                                if len(proxies_pool) == 0:
                                    print('当前代理池为空，运行程序前请准备足够的代理池')
                                    # 重置一下代理池
                                    with open("zdaye_available.txt", "r") as f:
                                        proxies_pool = json.load(f)
                                USER_AGENT = random.choice(USER_AGENT_LIST)
                                headers = {'user-agent': USER_AGENT}
                                proxies = random.choice(proxies_pool)
                                print('new proxies:', proxies)
                                continue
                print(page, image_url, signal)
                # 保存图片
                with open(outputs + '{0:0>3}_{1:0>2}_{2}.jpg'.format(i_chapter, page, chapter_name), 'wb') as file:
                    file.write(image.content)
                # 章节停止的标志
                if signal == 'javascript:SinTheme.nextChapter();':
                    break
                page += 1


# 漫画目录页
contents_url = 'https://m.gufengmh8.com/manhua/congqianyouzuolingjianshan/'
# 输出位置
outputs = './outputs/'
# 随机选择一个headers
USER_AGENT0 = random.choice(USER_AGENT_LIST)
headers0 = {'user-agent': USER_AGENT0}
# 获取当前网页
response = requests.get(contents_url, headers=headers0)
# print(response.text)
html = response.content
html_doc = str(html, 'utf-8')
# 树化
response_etree = etree.HTML(html_doc)
# xpath定位
chapters = response_etree.xpath('//ul[@id="chapter-list-1"]/li')
print('现有章节数', len(chapters))
# 所有章节链接队列
chapters_name_url_queue = Queue(len(chapters))
for i, chapter in enumerate(chapters):
    # 该章节名称
    chapter_name_ = chapter.xpath('./a/span/text()')[0].replace(' ', '_')
    # 该章节不完整链接
    chapter_url0 = chapter.xpath('./a/@href')[0]
    # 该章节完整链接
    chapter_url1 = 'https://m.gufengmh8.com' + chapter_url0
    print(i, chapter_name_, chapter_url1, 'put in queue')
    chapters_name_url_queue.put((i, chapter_name_, chapter_url1))
# queueLock = threading.Lock()
for i in range(10):
    thread = Spider()
    thread.start()


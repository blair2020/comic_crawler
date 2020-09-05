# 更新代理池，也就是zdaye_available.txt
# 将zdaye.txt内容删除，从站大爷免费ip代理复制新的粘贴到zdaye.txt
# 网址：https://www.zdaye.com/dayProxy.html
# 加入了多线程
import os
import time
import requests
import json
import threading
from queue import Queue

# 测试代理的网址
test_url = 'http://m.kuman55.com/'
# 从浏览器粘贴的headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}


class TestOldProxies(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(TestOldProxies, self).__init__(*args, **kwargs)

    def run(self):
        global new_proxies_pool
        while True:
            if old_proxies_queue.empty():  # 如果队列为空
                break
            test_proxies = old_proxies_queue.get()
            try:
                res = requests.get(test_url, headers=headers, proxies=test_proxies, timeout=3)
                print(test_proxies, 'is good!')
                new_proxies_pool.append(test_proxies['http'].split('//')[1])
            except Exception as e:
                print('timeout or wrong,remove')


class TestProxies(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(TestProxies, self).__init__(*args, **kwargs)

    def run(self):
        global new_proxies_pool
        while True:
            if proxies_queue.empty():  # 如果队列为空
                break
            test_proxies = proxies_queue.get()
            try:
                res = requests.get(test_url, headers=headers, proxies=test_proxies, timeout=3)
                print(test_proxies, 'is good!')
                new_proxies_pool.append(proxies['http'].split('//')[1])
            except Exception as e:
                print('timeout or wrong, sorry')


# 首先对旧代理池中的代理是否还可用进行验证
old_proxies_queue = Queue(1000)
new_proxies_pool = []
if os.path.exists("zdaye_available.txt"):
    with open("zdaye_available.txt", "r") as f:
        proxies_pool = json.load(f)
    for proxy in proxies_pool:
        proxy2 = {
            "http": "http://" + proxy,
            "https": "http://" + proxy,
        }
        old_proxies_queue.put(proxy2)
    old_threads = []
    # 起50个线程
    for i in range(50):
        thread = TestOldProxies()
        thread.start()
        old_threads.append(thread)
    for thread in old_threads:
        thread.join()
else:
    print('不存在zdaye_available.txt')
new_proxies_pool = list(set(new_proxies_pool))
print('=' * 30, 'old proxies num:', len(new_proxies_pool))

# 对新的代理进行验证
proxies_queue = Queue(1000)
for line in open('zdaye.txt', 'r', encoding='UTF-8'):
    IP_PORT = line.split('@')[0]
    proxies = {
        "http": "http://" + IP_PORT,
        "https": "http://" + IP_PORT,
    }
    proxies_queue.put(proxies)
threads = []
# 起20个线程
for k in range(100):
    thread = TestProxies()
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()
new_proxies_pool = list(set(new_proxies_pool))

print('-' * 20)
print('可用代理的数量：', len(new_proxies_pool))
# 将可用的代理保存到zdaye_available.txt
with open('zdaye_available.txt', 'w') as file:
    json.dump(new_proxies_pool, file)
print('Finish')
# 读取zdaye_available.txt的方法
# with open("zdaye_available.txt", "r") as f:
#     Dict = json.load(f)
#     print(Dict)

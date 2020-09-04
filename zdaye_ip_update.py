# 更新代理池，也就是zdaye_available.txt
# 将zdaye.txt内容删除，从站大爷免费ip代理复制新的粘贴到zdaye.txt
# 网址：https://www.zdaye.com/dayProxy.html

import os
import requests
import json
# 从浏览器粘贴的headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
# 首先对旧代理池中的代理是否还可用进行验证
if os.path.exists("zdaye_available.txt"):
    with open("zdaye_available.txt", "r") as f:
        proxies_pool = json.load(f)
    for proxy in proxies_pool:
        try:
            res = requests.get("https://m.gufengmh8.com/", headers=headers, proxies=proxy, timeout=3)
            print(proxy, 'is good!')
        except Exception as e:
            print('timeout or wrong, remove proxy')
            proxies_pool.remove(proxy)
    new_proxies_pool = proxies_pool
else:
    print('不存在zdaye_available.txt')
    new_proxies_pool = []
# 对新的代理进行验证
# 序号
i = 0
for line in open('zdaye.txt', 'r', encoding='UTF-8'):
    print(i)
    i += 1
    IP_PORT = line.split('@')[0]
    proxies = {
        "http": "http://" + IP_PORT,
        "https": "http://" + IP_PORT,
    }
    try:
        res = requests.get("https://m.gufengmh8.com/", headers=headers, proxies=proxies, timeout=3)
        print(IP_PORT, 'is good!')
        new_proxies_pool.append(proxies)
    except Exception as e:
        print('timeout or wrong, sorry')
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
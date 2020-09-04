# 从站大爷免费ip代理复制粘贴到zdaye.txt，对代理进行过滤
# 网址：https://www.zdaye.com/dayProxy.html
# 在爬虫之前先建立好一个代理池，也就是zdaye_available.txt
# 如果不用代理爬虫的话，爬多了自己的ip就会被网站封掉，被封了的话就打不开该网站了
import requests
import json
# 从浏览器粘贴的headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
# 装代理的列表
proxies_pool = []
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
        proxies_pool.append(proxies)
    except Exception as e:
        print('timeout or wrong, sorry')
print('-' * 20)
print('可用代理的数量：', len(proxies_pool))
# 将可用的代理保存到zdaye_available.txt
with open('zdaye_available.txt', 'w') as file:
    json.dump(proxies_pool, file)
print('Finish')
# 读取zdaye_available.txt的方法
# with open("zdaye_available.txt", "r") as f:
#     Dict = json.load(f)
#     print(Dict)

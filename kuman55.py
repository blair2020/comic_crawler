# import requests
#
# url = 'http://m.kuman55.com/12168/'
# # 从浏览器粘贴的headers
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
# res = requests.get(url, headers=headers)
# print(res.text)

# import requests
# import json
#
# #             章节1的数据                                        章节2的数据
# url_list = ['http://m.kuman55.com/bookchapter/?id=12168&id2=1','http://m.kuman55.com/bookchapter/?id=12168&id2=4']
# #访问方式一样，只访问章节1演示
# res = requests.get(url_list[0]).json()
# res = res.json()
# for i in res:
#     print(i)

#http://m.kuman55.com/12168/+i[id] 即为每一话的链接
#还不会可以远程操作你看下

# -*- coding: utf-8 -*-
import requests
import re

id = 12168

s = requests.session()
page = s.get(f'http://m.kuman55.com/{id}/').text
page = re.findall(r'chapterList_ul_1(.*?)</ul>', page, re.S)[0]
find = re.findall(fr'<li><a href=\"\/{id}\/([0-9]*?)\.html.*?>(.*?)<\/a>', page, re.S)
list = [{'name': x[1], 'url': f'http://m.kuman55.com/{id}/{x[0]}.html'} for x in find]
data = s.get(f'http://m.kuman55.com/bookchapter/?id={id}&id2=1').json()
list2 = [{'name': x['name'], 'url': f'http://m.kuman55.com/{id}/{x["id"]}.html'} for x in data]
list.extend(list2)

for x in list:
    print(x)
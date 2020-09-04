import os
import requests
from lxml import etree
import openpyxl
# 判断一下表格是否已经存在，不存在就新建一个
if not os.path.exists('test.xlsx'):
    wb = openpyxl.Workbook()
else:
    wb = openpyxl.load_workbook('test.xlsx')
ws = wb.active
# 网址
url = 'https://www.baidu.com/'
# 从浏览器粘贴的headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
response = requests.get(url, headers=headers)
html = response.content
html_doc = str(html, 'utf-8')
# print(html_doc)
# 树化
response_etree = etree.HTML(html_doc)
first_new = response_etree.xpath('//*[@id="hotsearch-content-wrapper"]/li[1]/a/span[2]/text()')
ws.append(first_new)
wb.save('test.xlsx')

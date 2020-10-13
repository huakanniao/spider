# -*- coding: utf-8 -*-
# @Author  : xueqin
# Version  ：Python 3.7.6
# @Date    : 2020/9/25

from lxml import etree

with open('showUi@uid=77125.html', 'r', encoding='utf-8') as f:
    HTML = f.read()
HTML = HTML.strip().replace('&#xd', '')
doc = etree.HTML(HTML)
data = ''.join(doc.xpath('//*[@id="fromData"]/div[14]/div/textarea//text()'))
print(data)
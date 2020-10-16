# 58二手房信息
from  lxml import etree
import requests
url='https://cd.58.com/ershoufang/'
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
page_text=requests.get(url=url,headers=headers).text
tree=etree.HTML(page_text)
title=tree.xpath('//h2[@class="title"]/a/text()')
with open('./58.text','w',encoding='utf-8') as fp:
    for each_title in title:
        print(title)
        fp.write(each_title+'\n')


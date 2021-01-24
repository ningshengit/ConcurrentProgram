# -*- coding: utf-8 -*-
# @Date    : 2020-12-09 22:12:43
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 
# @Version : $Id$

from  scrapy import Selector
import os
import time
import re
import jieba
from bs4 import BeautifulSoup

with open("shige.html", 'r', encoding='utf-8') as fp:
    res = fp.read()


soup = BeautifulSoup(res, 'lxml')
shige_dict ={
    
}
#print(soup.title)
zs_title = soup.select('#zs_title')[0].get_text()
print(zs_title)
auther = soup.select('.niandai_zuozhe')[0].get_text().replace(' ', '')
print(auther)
content = soup.select('#zs_content')[0].get_text().replace(' ', '').replace('\n', '')
print(content)
shangxi_content = soup.select('.shangxi_content')[0].get_text().replace(' ', '').replace('\n', '')
print(shangxi_content)
shige_dict['zs_title'] = zs_title
shige_dict['auther'] = auther
shige_dict['content'] = content
shige_dict['shangxi_content'] = shangxi_content


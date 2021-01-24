# -*- coding: utf-8 -*-
# @Date    : 2021-01-23 17:56:08
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 爬取诗歌网诗歌
# @Version : $Id$

import os
import requests
import random
from bs4 import BeautifulSoup
import json

start_url = 'https://www.shicimingju.com/shicimark/tangshisanbaishou_0_0__0.html'
base_url = 'https://www.shicimingju.com/shicimark/tangshisanbaishou_{}_0__0.html'

user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
]
headers = {
          #'Accept-Encoding': 'gzip, deflate, br',
          #'accept-language': 'zh-CN,zh;q=0.9',
          'User-Agent': random.choice(user_agent_list),
          'Referer': 'https://www.shicimingju.com/shicimark/tangshisanbaishou_0_0__0.html'
}

def get_shige_content(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        #shige_dict ={}
        soup = BeautifulSoup(res.content.decode('utf-8'), 'lxml')
        zs_title = soup.select('#zs_title')[0].get_text()
        if '/' in zs_title:
            zs_title = zs_title.replace('/', '')
        #print(zs_title)
        auther = soup.select('.niandai_zuozhe')[0].get_text().replace(' ', '')
        content = soup.select('#zs_content')[0].get_text().replace(' ', '').replace('\n', '')
        #print(content)
        shangxi_content = soup.select('.shangxi_content')
        if shangxi_content:
            shangxi = shangxi_content[0].get_text().replace(' ', '').replace('\n', '')
        else:
            shangxi = "-"
        return [zs_title, auther, content, shangxi]


def save_shige(shige):
    with open(f'shige/{shige[0]}.txt', 'w', encoding='utf-8') as fp:
            fp.writelines(shige)
            fp.write('\n')

def get_shige_url(url):
    
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        temp = soup.find_all('div', attrs={'class':'card shici_card'})[0]
        urls = []
        for url in temp.select('h3 a'):
           shige_url = 'https://www.shicimingju.com' + url['href']
           urls.append(shige_url)
        return urls
    else:
        return

if __name__ == '__main__':
    urls = []
    for page in range(1, 17):
        url = base_url.format(page)
        result = get_shige_url(url)
        urls.append(result)
    shige_content = []
    for _ in urls:
        for i in range(0, 3):
            result = get_shige_content(_[i])
            shige_content.append(result)
        break
    for x in shige_content:
        save_shige(x)
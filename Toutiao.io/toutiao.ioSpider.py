# !/usr/bin/env python
# coding=utf-8
"""
@File: toutiao.ioSpider.py
@Time: 2020-02-26 21:26
@Desc:
"""
import asyncio
import re
import requests
from bs4 import BeautifulSoup

from tool_funcitons import get_article
from constant import headers


# resbonse = requests.get('https://toutiao.io/subjects/4?f=new', headers=headers)
# resbonse = requests.get('https://toutiao.io/k/gqdjjgw', headers=headers)
# print(resbonse.text)

def get_last_pag_num(id: int) -> int:
    """
    从作者第一页文章列表获取最后一页的数字
    :param id:
    :return: 最后一页数字
    """
    one_page_url = f'https://toutiao.io/subjects/{id}'
    params = {
        'f': 'new',
    }
    one_page_result = requests.get(url=one_page_url, params=params, headers=headers).text
    # print(one_page_result)
    soup = BeautifulSoup(one_page_result, 'html.parser')
    last = soup.find('li', class_='last')
    pattern = re.compile(r'.*page=(\d+).*')
    last_page_num_list = pattern.findall(str(last))
    last_pege_num = int(last_page_num_list[0]) if last_page_num_list else 1
    return last_pege_num

def get_this_page_article_url_and_source(id: int, page_num: int) -> list:
    """
    从当前页面获取文章链接和文章来源
    :param id:
    :param page_num:
    :return: [文章链接, 文章来源]
    """
    one_page_url = f'https://toutiao.io/subjects/{id}'
    params = {
        'f': 'new',
        'page': page_num
    }
    one_page_result = requests.get(url=one_page_url, params=params, headers=headers).text
    soup = BeautifulSoup(one_page_result, 'html.parser')
    contents = soup.find_all('div', class_='content')
    result = list()
    for content in contents:
        pattern_data_url = re.compile(r'.*?data-url="/posts/(\w+)">.*')
        # print(content)
        data_url = pattern_data_url.findall(str(content))[0]
        pattern_source = re.compile(r'.*?<div class="meta">\s(.*)')
        source = pattern_source.findall(str(content))[0].strip()
        print('source:', source)
        result.append([data_url, source])
    # print(result)
    return result


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    last_page_num = get_last_pag_num(id=3838)
    # get_this_page_article_url_and_source(id=1, page_num=1)
    for page_num in range(1, 1 + 1):
        this_page_article_url_and_source_list = get_this_page_article_url_and_source(id=4, page_num=page_num)
        tasks = [asyncio.ensure_future(get_article(article_url=f'https://toutiao.io/k/{article_url_and_source[0]}', source=article_url_and_source[1])) for article_url_and_source in this_page_article_url_and_source_list]
        loop.run_until_complete(asyncio.wait(tasks))
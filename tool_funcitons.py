# !/usr/bin/env python
# coding=utf-8
"""
@File: tool_funcitons.py
@Time: 2020-02-26 21:55
@Desc:
"""
import aiohttp
import re

from bs4 import BeautifulSoup

from constant import headers




def mp_weixin_qq_com(article_result: str):
    """
    解析微信公众号文章
    :param article_result:
    :return:
    """
    soup = BeautifulSoup(article_result, 'html.parser')
    # try:
    title = soup.find_all("h2", class_='rich_media_title')[0].text.strip()
    author = soup.find_all('strong', class_='profile_nickname')[0].text
    content = soup.find_all('div', class_='rich_media_content')[0].text
    print('title:', title)
    print(author)
    print(content)

source_2_func_dict = {
    'mp.weixin.qq.com': mp_weixin_qq_com
}

async def get_article(article_url: str, source: str):
    """

    :param article_url: 文章链接
    :param source: 文章来源
    :return:
    """
    print(article_url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=article_url, headers=headers) as resposne:
            article_result = await resposne.text()
            print('article_url:', article_url)
            # print(article_result)
            print(source)
            source_2_func_dict.get(source)(article_result)
            return article_result
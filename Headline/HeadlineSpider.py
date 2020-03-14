# !/usr/bin/env python
# coding=utf-8
"""
@File: HeadlineSpider.py
@Time: 2020/1/9 1:24
@Desc:
"""
import asyncio
import random
import aiohttp
import requests
import time
from constant import headers
import ujson
from bs4 import BeautifulSoup
from m_toutiao import get_as_cp_signature


async def get_article(item_id: int):
    article_url = f'https://www.toutiao.com/i{item_id}/'
    print(article_url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=article_url, headers=headers) as resposne:
            return await resposne.text()


async def clean_article_data(item_id: int) -> None:
    time.sleep(random.randint(0, 5))
    aritcle_result = await get_article(item_id=item_id)

    clean_data(aritcle_result)
    # return aritcle_result

def clean_data(aritcle_result: str) -> list:
    soup = BeautifulSoup(aritcle_result, 'html.parser')
    # print(aritcle_result)
    scripts = soup.find_all('script')
    print(scripts)

    # for script in scripts:
    #     print('=======script=======')
    #     print(len(script))
    #     print('=======script=======')


def get_all_source_item_id(user_id: int) -> None:
    loop = asyncio.get_event_loop()
    max_behot_time = 0
    all_item_id_list = list()
    has_more = True
    params = get_as_cp_signature(user_agent=headers['user-agent'], )
    while has_more:
        item_id_list, max_behot_time, has_more = get_item_id_list_and_max_behot_time(user_id=user_id, params=params)
        all_item_id_list += item_id_list
        print('user_id:', user_id)
    print(all_item_id_list)
    tasks = [asyncio.ensure_future(clean_article_data(item_id=item_id)) for item_id in all_item_id_list]
    before_time = time.time()
    loop.run_until_complete(asyncio.wait(tasks))
    after_time = time.time()
    print('协程共计耗时：', after_time - before_time)


def get_item_id_list_and_max_behot_time(user_id: int, params: dict) -> (list, int, bool):
    user_main_page = f'https://www.toutiao.com/c/user/article/?user_id={user_id}'
    res = requests.get(url=user_main_page, headers=headers, params=params)
    json_res = ujson.loads(res.text)
    print(json_res)
    data = json_res.get('data')
    max_behot_time = json_res.get('next').get('max_behot_time')
    item_id_list = list()
    for dict_info in data:
        item_id = dict_info.get('item_id')
        item_id_list.append(item_id)
    has_more = json_res.get('has_more')
    print(has_more)
    return item_id_list, max_behot_time, has_more


if __name__ == '__main__':
    user_id_list = [5772853537]
    futures = list()
    for user_id in user_id_list:
        get_all_source_item_id(user_id=user_id)

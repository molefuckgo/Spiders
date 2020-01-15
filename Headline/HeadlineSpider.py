# !/usr/bin/env python
# coding=utf-8
"""
@File: HeadlineSpider.py
@Time: 2020/1/9 1:24
@Desc:
"""
import asyncio
import time

import aiohttp
import requests
from constant import headers
import ujson


async def get_article(item_id:int):
    article_url = f'https://www.toutiao.com/i{item_id}/'
    print(article_url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=article_url, headers=headers) as resposne:
            return await resposne.text()

async def clean_article_data(item_id:int) -> None:
    print('clean_article_data')
    aritcle_result = await get_article(item_id=item_id)
    print(aritcle_result)
    # return aritcle_result

def get_all_source_item_id(user_id:int) -> None:
    loop = asyncio.get_event_loop()
    max_behot_time = 0
    all_item_id_list = list()
    has_more = True
    while has_more:
        item_id_list, max_behot_time, has_more = get_item_id_list_and_max_behot_time(user_id=user_id, max_behot_time=max_behot_time)
        all_item_id_list += item_id_list
        print('user_id:', user_id)
    print(all_item_id_list)
    tasks = [asyncio.ensure_future(clean_article_data(item_id=item_id)) for item_id in all_item_id_list]
    print('tasks', tasks)
    before_time = time.time()
    loop.run_until_complete(asyncio.wait(tasks))
    after_time = time.time()
    print('协程共计耗时：', after_time - before_time)
    for item_id in all_item_id_list:
        article_url = f'https://www.toutiao.com/i{item_id}/'
        requests.get(url=article_url, headers=headers)
    print('单线程共计耗时：', time.time() - after_time)



def get_item_id_list_and_max_behot_time(user_id:int, max_behot_time:int) -> (list, int, bool):
    user_main_page = f'https://www.toutiao.com/c/user/article/?page_type=1&user_id={user_id}&max_behot_time={max_behot_time}&count=20'
    res = requests.get(url=user_main_page, headers=headers)
    json_res = ujson.loads(res.text)
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
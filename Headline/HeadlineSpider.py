# !/usr/bin/env python
# coding=utf-8
"""
@File: HeadlineSpider.py
@Time: 2020/1/9 1:24
@Desc:
"""
import requests
from constant import headers
import ujson
from concurrent.futures import  ThreadPoolExecutor



def get_all_source_url(user_id:int) -> None:
    max_behot_time = 0
    all_item_id_list = list()
    has_more = True
    while has_more:
        item_id_list, max_behot_time, has_more = get_item_id_list_and_max_behot_time(user_id=user_id, max_behot_time=max_behot_time)
        all_item_id_list += item_id_list
    print(all_item_id_list)



def get_item_id_list_and_max_behot_time(user_id:int, max_behot_time:int) -> list:
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
    user_id_list = [110935079834]
    pool = ThreadPoolExecutor(max_workers=5)
    futures = list()
    for user_id in user_id_list:
        futures.append(pool.submit(get_all_source_url, user_id))

# !/usr/bin/env python
# coding=utf-8
"""
@File: HeadlineSpider.py
@Time: 2020/1/9 1:24
@Desc:
"""
from constant import headers
from MyThreadClass import ThreadManger
from MyThreadClass import ThreadPoolManger
import ujson
# print(ujson.loads(requests.get(url, headers=headers).text))




def get_all_source_url(user_id:int) -> None:
    max_behot_time = 0
    user_main_page = f'https://www.toutiao.com/c/user/article/?page_type=1&user_id={user_id}&max_behot_time={max_behot_time}&count=20'

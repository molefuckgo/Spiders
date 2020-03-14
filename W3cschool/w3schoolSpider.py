# !/usr/bin/env python
# coding=utf-8
"""
@File: w3schoolSpider.py
@Time: 2020-03-03 11:22
@Desc:
"""

from tool_funcitons import get_article
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from instance import py_mysql_pool

main_url = 'https://www.w3school.com.cn/'
w3c_school_head_url = 'https://www.w3school.com.cn'
HTML_CSS = w3c_school_head_url + '/h.asp'
BROSER_SIDE = w3c_school_head_url + '/b.asp'
SERVER_SIDE = w3c_school_head_url + '/s.asp'
PROGRAMMING = w3c_school_head_url + '/p.asp'
XML = w3c_school_head_url + '/x.asp'
WEB_BUILDING = w3c_school_head_url + '/w.asp'
# REFERENCE = w3c_school_head_url + '/r.asp'
total_url_list = [HTML_CSS, BROSER_SIDE, SERVER_SIDE, PROGRAMMING, XML, WEB_BUILDING]   # , REFERENCE]
# total_url_list = [HTML_CSS]


def get_tutorial_index_page(url: str) -> list:
    """
    根据*.asp获取个教程index页
    :param url: *.asp url
    :return: [**.index,]各教程index页列表
    """
    asp_html_text = requests.get(url).text
    # print(asp_html_text)
    soup = BeautifulSoup(asp_html_text, 'html.parser')
    course = BeautifulSoup(str(soup.find('div', id='course')), 'html.parser')
    for a in course.find_all('a'):
        # print(a.get('href'), a.get('title'))
        pass
    maincontent = BeautifulSoup(str(soup.find('div', id='maincontent')), 'html.parser')
    for div in maincontent.find_all('div'):
        if div.attrs == {u'id': u'maincontent'} or div.attrs == {u'id': u'foogz'}:  # foogz是广告
            continue
        if div.attrs == {u'id' : u'w3school'}:
            # print('xxxx系列教程')
            k_course_title = div.h1.text
            print(k_course_title)
            # print(div.h1)
            # print(div.h1.text)
            # print(div)
            # print(div.text)
            print('==========================')
        else:
            # print(div.h2)
            # print(div.h2.text)
            # print(div)
            # after_div = re.sub(r'"/.*?.asp"', '"替换"', str(div),)    # 站内教程index页替换
            # after_div = re.sub(r'W3School', '我们', str(after_div),)  # 替换W3说chool
            # print('after:', after_div)
            # print(div.text)
            k_course_intro = re.sub(r'W3School', '我们', str(div.text), )  # 替换W3school
            # print('after:', after_div)
            k_course_add_time = datetime.now()
            print(k_course_intro)
            print(k_course_add_time)
            print(url)
            print('==========================')
if __name__ == '__main__':
    for url in total_url_list:
        get_tutorial_index_page(url)

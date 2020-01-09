# !/usr/bin/env python
# coding=utf-8
"""
@File: GetHeadlineCookie.py
@Time: 2020-01-09 16:04
@Desc:
"""
from selenium import webdriver
import time
window=webdriver.Chrome()
window.get("https://www.toutiao.com/")
c1={u"name":u"uid_tt",u"value": u"1f46d8d4bfcbefe9bc65e11e68f7d548",u"domain":u".toutiao.com"}
c2={u"name":u"ccid",u"value": u"66c7871a52ca20abc48d678a36a501f2",u"domain":u".toutiao.com"}
c3={u"name":u"ckmts",u"value": u"PUJw85AQ,qrJw85AQ,L6Cw85AQ",u"domain":u".toutiao.com"}
c4={u"name":u"sid_tt",u"value":u"f89559a8c6f4507d2797ab84faedb6f3",u"domain":u".toutiao.com"}

window.add_cookie(c1)
window.add_cookie(c2)
window.add_cookie(c3)
window.add_cookie(c4)
window.get("https://www.toutiao.com/")
time.sleep(3)


# window.refresh()

word=window.find_element_by_xpath('//*[@id="rightModule"]/div[1]/div/div/div/input')
word.send_keys("soho")
time.sleep(2)
window.find_element_by_xpath('//*[@id="rightModule"]/div[1]/div/div/div/div/button/span').click()
time.sleep(5)
window.quit()
# html=window.page_source
# print(html)
#
# window.get_screenshot_as_file("a.png")
# page=window.page_source
# print(page)
cookies = window.get_cookies()
# print(cookies)

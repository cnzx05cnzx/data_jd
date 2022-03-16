import math
import time
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
import random
from lxml import etree
import re
import requests
import string
import json


# 根据百度搜索计算pmi，从而在候补频繁项集种抽取真正属性
def get_pmi1(word):
    try:
        url = 'https://www.baidu.com/s?wd="{}"'.format(word)
        driver.get(url)
        t = driver.find_element_by_xpath('//*[@id="tsn_inner"]/div[2]/span').text
        t = "".join(list(filter(str.isdigit, t)))
        # print(t)
    except:
        print(driver.page_source)
        t = 1
    return int(t)


def get_pmi2(word1, word2):
    try:
        word = word1 + ' ' + word2
        url = 'https://www.baidu.com/s?wd="{}"'.format(word)
        driver.get(url)
        t = driver.find_element_by_xpath('//*[@id="tsn_inner"]/div[2]/span').text
        t = "".join(list(filter(str.isdigit, t)))
    # print(t)
    except:
        print(driver.page_source)
        t = 20000000
    return int(t)


def judge_pmi(word, words):
    res = {}
    w_pmi = get_pmi1(word)
    for w in words:
        w1=w+word
        w2=word+w
        t1 = get_pmi1(w1)+get_pmi1(w2)
        t2 = get_pmi1(w)
        temp = 100000000.0 * t1 / (w_pmi * t2)
        res[w] = temp
        time.sleep(random.random())
        # print(temp)
    res = sorted(res.items(), key=lambda kv: (kv[1], kv[0]))
    print(res)


if __name__ == "__main__":
    # 设置无界面模式，也可以添加其它设置
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    # edge_options.add_argument('headless')
    edge_options.add_argument('blink-settings=imagesEnabled=false')

    # driver = webdriver.Edge(options=edge_options)
    driver = Edge(options=edge_options, executable_path='./use/MicrosoftWebDriver.exe')

    driver.get('https://www.baidu.com')

    a = "手机"
    b = ['耗电', '音效', '画质', '速度', '王者', '像素', '原神', '深蓝', '优惠券']
    # 阈值定在0.0003以上

    judge_pmi(a, b)
    driver.close()
    # print(get_pmi('手机', '画质'))

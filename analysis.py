import math
import time
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
import random
from lxml import etree
import re
import requests
import pandas as pd
import string
import json
import pkuseg


# 读取txt填充


def read_file(name):
    words = list()
    with open(name, "r", encoding='utf-8') as f:  # 打开文件
        for line in f.readlines():
            line = line.rstrip('\n')
            words.append(line)
    return words


def get_stop_words():
    # 读入停用词表
    words_list = []

    with open("./use/停用词.txt", 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines:
            words_list.append(line.strip())

    # 自定义停用词
    my_words = ["。。", "手机"]
    words_list.extend(my_words)

    return words_list


# use pkuseg splice word
def splice_word(data):
    data['cut'] = data['comment'].apply(lambda x: list(seg.cut(x)))

    # print(data.head())

    stop_words = get_stop_words()

    data['cut'] = data['comment'].apply(lambda x: [i for i in seg.cut(x) if i not in stop_words])

    # print(data.head())
    return data


def sentiment(words, data):
    res = {}
    for d in data:
        res[d] = 0.0

    sum = 0
    for index, row in words.iterrows():
        sum += 1
        temp = row['cut']
        pos = 0
        for t in temp:
            if t in data:
                i = j = pos
                while i >= 0 and j < len(temp):
                    if temp[i] in neg_words:
                        if i >= 1 and temp[i - 1] == '不':
                            res[t] += 1
                        else:
                            res[t] -= 1

                        break
                    elif temp[i] in pos_words:
                        if i >= 1 and temp[i - 1] == '不':
                            res[t] -= 1
                        else:
                            res[t] += 1

                        break
                    else:
                        i -= 1
                        j += 1
            pos += 1

    for (k, v) in res.items():
        res[k] = (1.0 * v / sum + 1) * 2.5

    print(res)


if __name__ == "__main__":
    seg = pkuseg.pkuseg()
    # 训练数据
    now_data = pd.read_csv('data/temp.csv', encoding="gbk")
    now_data = splice_word(now_data)

    # 情感词典
    pos_words = read_file('./use/postive.txt')
    neg_words = read_file('./use/negtive.txt')

    # 抽取属性集
    clu_words = ['速度', '外观', ' 音效', '屏幕', '手感', '游戏']
    sentiment(now_data, clu_words)

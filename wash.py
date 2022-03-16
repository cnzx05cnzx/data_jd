import pandas as pd
import jieba
import pkuseg


# 单纯词频统计获取抽取属性


def get_stop_words():
    # 读入停用词表
    words_list = []

    with open("use/停用词.txt", 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines:
            words_list.append(line.strip())

    # 自定义停用词
    my_words = ["。。", "手机"]
    words_list.extend(my_words)

    return words_list


# use jieba splice word
def splice_word1(data):
    data['cut'] = data['comment'].apply(lambda x: list(jieba.cut(x)))

    # print(data.head())

    stop_words = get_stop_words()

    data['cut'] = data['comment'].apply(lambda x: [i for i in jieba.cut(x) if i not in stop_words])

    print(data.head())


# use pkuseg splice word
def splice_word2(data):
    seg = pkuseg.pkuseg()
    data['cut'] = data['comment'].apply(lambda x: list(seg.cut(x)))

    # print(data.head())

    stop_words = get_stop_words()

    data['cut'] = data['comment'].apply(lambda x: [i for i in seg.cut(x) if i not in stop_words])

    # print(data.head())
    return data


# counter the frequency of the words
def counter_words(data):
    words = []

    for content in data['cut']:
        words.extend(content)

    corpus = pd.DataFrame(words, columns=['word'])
    corpus['cnt'] = 1

    # 分组统计
    g = corpus.groupby(['word']).agg({'cnt': 'count'}).sort_values('cnt', ascending=False)

    # print(g.head(20))
    return g


if __name__ == "__main__":
    pre_data = pd.read_csv('data/temp.csv', encoding="gbk")
    # pre_data['comment'] = pre_data['comment'].str.replace(r'[^\u4e00-\u9fa5]', '')

    now_data = splice_word2(pre_data)

    words = counter_words(now_data)

    # try to mark the word into their part
    pos = 0
    for index, row in words.iterrows():

        seg = pkuseg.pkuseg(postag=True)  # 开启词性标注功能
        text = seg.cut(index)  # 进行分词和词性标注
        if text[0][1] == "n":
            print(index)
        pos += 1
        if pos >= 10:
            break

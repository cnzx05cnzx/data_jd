import pandas as pd
import jieba
import pkuseg
from gensim.models import Word2Vec, KeyedVectors

# 打印候补频繁项集
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)


# 训练词向量模型

# 停用词表
def get_stop_words():
    words_list = []

    with open("use/停用词.txt", 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines:
            words_list.append(line.strip())

    # 自定义停用词
    my_words = ["。。"]
    words_list.extend(my_words)

    return words_list


# 分词
def splice_word2(data):
    seg = pkuseg.pkuseg()
    data['cut'] = data['comment'].apply(lambda x: list(seg.cut(x)))

    stop_words = get_stop_words()

    data['cut'] = data['comment'].apply(lambda x: [i for i in seg.cut(x) if i not in stop_words])

    return data


# 模型训练
def train_nodel(word):
    model = Word2Vec(word, min_count=5)
    vector = model.wv
    model.save('./w2v/word.Model')
    vector.save("./w2v/wv.wordvectors")


if __name__ == "__main__":
    # # 1.分词
    # pre_data = pd.read_csv('data/comment.csv', encoding="gbk")
    # pre_data['comment'] = pre_data['comment'].str.replace(r'[^\u4e00-\u9fa5]', '')
    # now_data = splice_word2(pre_data)
    # sentences = []
    # for index, row in now_data.iterrows():
    #     sentences.append(row['cut'])
    # # print(sentences)
    # # 2.模型训练
    # train_nodel(sentences)

    # 3.模型使用
    # texts = ['充电器', '紫色', '修饰', '能力', '充电头', '绿色', '需要', '画面', '风格', '瑕疵', '外形', '红米', '素质', '造型', '镜头', '夜景', '照片',
    #          '觉', '摄像头', '指纹', '颜色', '声效', '老铁', '小时', '品位', '现象', '强', '感觉', '品牌', '序列号', '壳', '画质', '全屏', '贼', '态度',
    #          '色彩', '特色', '字', '待机', '老年人', '外观', '给力', '老妈', '女生', '底层', '总体', '价格', '网络', '王者', '老婆', '鸡', '棒棒', '经济',
    #          '分辨率', '亮度', '经典', '大小', '小米', '关键', '尺寸', '电影', '女人', '音乐', '本色', '老人', '入门机', '档次', '网速', '手感', '后台',
    #          '原装', '出品', '眼睛', '钢琴', '壳百', '黄色', '毛病', '正品', '份量', '道理', '包装', '概念', '颜滤镜', '握感', '商品', '听筒', '视频',
    #          '技术', '会', '时间', '品质', '元神', '爸爸', '结果', '巧克力', '耳膜', '骚红色', '弧度', '大字', '外包装', '压力', '大气', '程序', '人脸',
    #          '蓝色', '智能机', '系统', '配色', '系列', '屏幕', '杠杠', '重量', '电量', '内容', '功能', '备用机', '办法', '色差', '性能', '绿屏', '耐用量',
    #          '人', '面部', '个人', '价钱', '限度', '面容', '游戏', '内存', '时代', '女朋友', '地球', '软件', '白色', '专卖店', '平面屏', '标准', '物流',
    #          '刷屏', '速度', '眼球', '中规中矩', '款', '色彩感', '音质', '好评', '清晰度', '价比', '颜值', '幕屏', '苹果', '白条', '玩意儿', '手机', '声音',
    #          '电', '送人', '性价比', '像素', '事', '原度', '细节', '父亲节', '机子', '青少年', '世纪', '质量', '助手', '电池', '大片', '卖家', '东西',
    #          '情况', '色', '优惠券', '耳机', '男生', '短板', '处理器', '深蓝', '流畅度', '问题', '效果', '需求', '黑色', '电话', '质感', '月', '字体',
    #          '音量', '棱角', '时尚', '音效', '分量', '芯片', '背板', '手']
    wv = KeyedVectors.load("./w2v/wv.wordvectors", mmap='r')
    print(wv.similarity('手机','王者'))


    # for t in texts[::-1]:
    #     try:
    #         wv.get_vector(t)
    #     except:
    #         texts.remove(t)
    #         print(t)
    #         # print('err')
    # print(texts)

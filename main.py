import csv
import json
import random
import requests
from lxml import etree
import re
import time


# 获取爬取京东商品评论，（手机）

def get_id(Url):
    id_list = []
    headers = {
        # 用的哪个浏览器
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        # 从哪个页面发出的数据申请，每个网站可能略有不同
        'referer': 'https://item.jd.com/100007299145.html',
        # 哪个用户想要看数据，是游客还是注册用户,建议使用登录后的cookie
        'cookie': 'shshshfpa=4cc164e7-8d80-5812-aa77-f756047d843d-1640516828; __'
                  'jdv=122270672|baidu|-|organic|notset|1640516828272; '
                  'shshshfpb=iBq6WT8qzB%2BZ7ZcskSYDHLA%3D%3D; __jdu=16405168282721562381715; '
                  'areaId=15; ipLoc-djd=15-1213-3411-0; PCSYCityID=CN_330000_330100_330106;'
                  ' __jdc=122270672; shshshfp=e5ef1dd244de22493ae3f3b8efe6d99d; ip_cityCode=1213; mt_xid=V2_52007VwMVV1xcUl0WShBfA2QDFlVeWltaGUkdbFVlUxICXF5TRk1ASgkZYgtAUkELAg5LVRoJUWdREwBbDFoPH3kaXQZkHxNSQVlWSx9KElkBbAYVYl9oUmobTxhVB2UGEFNUaFJcG00%3D; '
                  '__jda=122270672.16405168282721562381715.1640516828.1641356890.1641360448.4; wlfstk_smdl=9z3epkx2ncpmma6oloror6383f5hiyxr; pinId=yGPofQDgOxUi3tFwxJfOfQ; pin=jd_kAoUgKwcSqML; unick=jd_kAoUgKwcSqML; ceshi3.com=000; _tp=NS8P8co2Yv1yYzeAVY4oOw%3D%3D; _pst=jd_kAoUgKwcSqML; cn=0;'
                  ' __jdb=122270672.7.16405168282721562381715|4.1641360448; shshshsID=6edf4f3f07410deef40bc1c27f8e8f3a_3_1641361636863; '
                  'thor=4A48718821579F725C7D81C0999EA38BF115BD91FD607C0A0FA063A8D11146206D74F26A3A0D27A1A40B2B03DD9ECDCB1A3E349A1F777E949406FE43B77F878FD83DDF9AC4E28D9E6507B9D75C2B6850DC6AEF6D660C1816E67F685296C781BB89D07C193310217ACC32B1188FC02A94DC2D3A95A14839C4C22D2A88A19EEE404CA15D822BFB959B803BC4E3C52EB675FA61DEE1D804BABCA89A39AA9BBE203D; '
                  '3AB9D23F7A4B3C9B=QPZQCOPHV4PQJPRS3LZAV6JWGMTDCSTVBDXYPOG'
                  'EJBV5QLDKGVYMSEQAHMZGBCS2EMSQHTRWIQGBOUKXKDNWS43PRA'
    }
    # url = 'https://search.jd.com/search?keyword=笔记本&wq=笔记本&ev=exbrand_联想%5E&page=9&s=241&click=1'
    res = requests.get(Url, headers=headers)
    res.encoding = 'utf-8'
    text = res.text

    selector = etree.HTML(text)
    shop_list = selector.xpath('//*[@id="J_goodsList"]/ul/li')

    for slist in shop_list:
        product_id = slist.xpath('.//div[@class="p-commit"]/strong/a/@id')[0].replace("J_comment_", "")
        id_list.append(product_id)

    return id_list


# 通过json获取评论
def get_json(Url):
    data_list = []
    headers = {
        # 用的哪个浏览器
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        # 从哪个页面发出的数据申请，每个网站可能略有不同
        'referer': 'https://item.jd.com/100007299145.html',
        # 哪个用户想要看数据，是游客还是注册用户,建议使用登录后的cookie
    }

    data = requests.get(Url, headers=headers).text
    time.sleep(2)

    # 将Str数据改为字典，必须去掉最开头和最结尾后面对应的符号才可以转化为字典！
    try:
        jd = json.loads(data.lstrip('fetchJSON_comment98(').rstrip(');'))

        # 取出用户评论，但是还包含了用户ID等其他信息和奇怪的符号
        com_list = jd['comments']
        com_sum = jd['productCommentSummary']['commentCountStr']
        if com_sum.find('万') != -1:
            # 爬取的数据为字典，将评论按键值对取出
            for li in com_list:
                data_list.append(re.sub('[\s+]', '。', li['content']))

            # 数据写入csv
            write_csv(data_list)
            # print(data_list)
        else:
            print('no ' + com_sum)
    except :
        print(Url)
        return



# 数据写入csv
def write_csv(data):
    file = open(r'D:\BaiduNetdiskDownload\pyc\work\data_jd\data\comment.csv', 'a+', newline='')
    fieldnames = ['comment']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    # writer.writeheader()
    for da in data:
        writer.writerow({'comment': da})
    file.close()


if __name__ == "__main__":
    # 获取商品id存入list
    shop_id = []
    # 1 5
    for i in range(1, 5):
        shop_url = "https://list.jd.com/list.html?cat=9987%2C653%2C655&psort=4&psort=4&page={}&s=117&click=0".format(
            i * 2 - 1)
        shop_id.extend(get_id(shop_url))
        time.sleep(random.uniform(0, 1))
        print("finish shop_id: " + str(i))
        # print(len(shop_id))


    # 对商品评论数据爬取
    # shop_id = [100009077477]
    shop_com = []
    cnt = 0
    for sid in shop_id:
        base = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98"
        first = "&productId={}".format(sid)
        last = "&pageSize=10&isShadowSku=0&fold=1"

        # 1 21
        for i in range(1, 21):
            middle = "&score=0&sortType=5&page={}".format(i)
            url = base + first + middle + last
            get_json(url)

        print('finsh ' + str(cnt))
        cnt = cnt + 1
    print('complete')

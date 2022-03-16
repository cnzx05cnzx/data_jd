import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models
import pandas as pd


# 获取词向量(腾讯api 维度有点高)
def get_vector(word):
    try:
        cred = credential.Credential("AKIDMXR5WieKjriJdgS2LN8cqnUv85F8k6Ax", "XpqZ1D8m9E3bssc4F9n9E2YonVv5yaw2")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

        req = models.WordEmbeddingRequest()
        params = {
            "Text": word
        }
        req.from_json_string(json.dumps(params))

        resp = client.WordEmbedding(req)
        # print(resp.Vector)
        return resp.Vector


    except TencentCloudSDKException as err:
        print(err)


if __name__ == "__main__":
    # 打印候补频繁项集
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth', 100)

    wvs = []
    texts = ['充电器', '紫色', '修饰', '能力', '充电头', '绿色', '需要', '画面', '风格', '瑕疵', '外形', '红米', '素质', '造型', '镜头', '夜景', '照片',
             '觉', '摄像头', '指纹', '颜色', '声效', '老铁', '小时', '品位', '现象', '强', '感觉', '品牌', '序列号', '壳', '画质', '全屏', '贼', '态度']
    # for t in texts[::-1]:
    #     temp = get_vector(t)
    #     if temp:
    #         wvs.append(get_vector(t))
    #     else:
    #         texts.remove(t)
    # get_vector(word)
    print(wvs)
    print(len(texts))
    # print(len(get_vector("我")))

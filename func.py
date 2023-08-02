import json

import requests
from nicegui import ui


# 从 json 中读取 bilibili API 的 url
def get_url(what):
    json_file = "./api.json"
    with open(json_file, "r") as f:
        json_data = json.load(f)
        # API
        return json_data[str(what)]


def convert(num, what):
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608

    def dec(x):
        r = 0
        for i in range(6):
            r += tr[x[s[i]]] * 58 ** i
        return (r - add) ^ xor

    def enc(x):
        x = (x ^ xor) + add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]] = table[x // 58 ** i % 58]
        return ''.join(r)

    # 作者：mcfx
    # 链接：https://www.zhihu.com/question/381784377/answer/1099438784
    # 来源：知乎
    try:
        if what == 'av2bv':
            av_num = int(num.replace('av', ''))
            return enc(av_num)
        elif what == 'bv2av':
            return 'av' + str(dec(num))
        else:
            return 'error'
    except Exception as e:
        with ui.dialog() as dialog_convert_err, ui.card():
            ui.label("转换失败！发生错误。{0}".format(str(e)))
            ui.button("好", on_click=dialog_convert_err.close)


image_url = ''
title_text = ''


def get_video_information(av, bv):
    global image_url, title_text
    api_url = get_url("video_api")
    url = api_url.format(av, bv)
    # print('API URL: ' + url)
    API_URL = url
    # 发送GET请求到API
    response = requests.get(f"{API_URL}")

    # 检查请求是否成功
    if response.status_code == 200:
        # 将响应解析为JSON
        data = json.loads(response.text)

        image_url = data['data']['pic']
        title_text = data['data']['title']

        # 传出去
        print('PIC URL: ' + image_url)
        print('TITLE TEXT: ' + title_text)
    else:
        print("请求时发生错误。")

    return image_url, title_text

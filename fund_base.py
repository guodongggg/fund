import requests
import json


def XiongAPI(url, code=None):
    """
    request模块调用
    :param url: API地址
    :param code: 基金代码
    :return: dict
    """
    params = {
        'code': code
    }
    try:
        response = requests.get(url, params=params, timeout=3)
    except Exception as e:
        print("XiongAPI error:", e)
        return {}
    result = response.json()
    if result['code'] != 200:
        raise Exception("API接口数据异常：" + response.text)
    else:
        return result


def BaseInfo(code):
    """
    基金基础信息
    :param code: 基金代码，用，隔开
    :return: dict
    """
    code = ','.join(code)
    url = 'https://api.doctorxiong.club/v1/fund'
    return XiongAPI(url, code).get('data', [])


def stock_board():
    """
    大盘基础信息
    :return: dict
    """
    url = 'https://api.doctorxiong.club/v1/stock/board'
    return XiongAPI(url).get('data', [])


if __name__ == '__main__':
    with open('file/code_list.json', 'r') as f:
        json_data = json.load(f)
        code_list = list(json_data['test'].keys())
    fundDetail = BaseInfo(code_list)
    board = stock_board()
    for i in board:
        print(i)
    print('---')
    for i in fundDetail:
        print(i)

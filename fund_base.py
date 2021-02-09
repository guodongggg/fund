import requests
from common import get_codelist


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
    except Exception:
        print("XiongAPI请求失败")
        return {}
    result = response.json()
    try:
        if result['code'] != 200:
            raise Exception("XiongAPI接口数据异常：" + response.text)
        else:
            return result
    except Exception:
        raise Exception("XiongAPI接口异常")


def BaseInfo(code):
    """
    基金基础信息
    :param code: 基金代码，用，隔开
    :return: dict
    """
    code = ','.join(code)
    url = 'https://api.doctorxiong.club/v1/fund'
    try:
        return XiongAPI(url, code).get('data', [])
    except Exception:
        raise Exception("XiongAPI接口异常,无法调用基金基础信息")


def stock_board():
    """
    大盘基础信息
    :return: dict
    """
    url = 'https://api.doctorxiong.club/v1/stock/board'
    try:
        return XiongAPI(url).get('data', [])
    except Exception:
        raise Exception("XiongAPI接口异常，无法调用大盘基础信息")


if __name__ == '__main__':
    code_list = get_codelist('test')
    fundDetail = BaseInfo(code_list)
    board = stock_board()
    for i in board:
        print(i)
    print('---')
    for i in fundDetail:
        print(i)

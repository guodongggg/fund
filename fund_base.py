import requests
import json


def XiongAPI(url, code=None):
    params = {
        'code': code
    }
    try:
        response = requests.get(url, params=params, timeout=3)
    except Exception as e:
        print("error:", e)
        return {}
    result = response.json()
    if result['code'] != 200:
        raise Exception("API接口数据异常：" + response.text)
    else:
        return result


def BaseInfo(code):
    code = ','.join(code)
    url = 'https://api.doctorxiong.club/v1/fund'
    return XiongAPI(url, code).get('data', [])


def stock_board():  
    url = 'https://api.doctorxiong.club/v1/stock/board'
    return XiongAPI(url).get('data', [])


if __name__ == '__main__':
    with open('code_list.json', 'r') as f:
        json_data = json.load(f)
        code_list = json_data['test']    
    fundDetail = BaseInfo(code_list)
    board = stock_board()
    for i in board:
        print(i)
    print('---')
    for i in fundDetail:
        print(i)

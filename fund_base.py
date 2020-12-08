import requests
import json

def XiongAPI(url, code=None):
    params = {
        'code':code
    }
    response = requests.get(url,params = params)
    result = response.json()
    if result['code'] != 200:
        raise Exception("API接口数据异常：" + response.text)
    else:
        return result
        
def BaseInfo(code):
    code = ','.join(code)
    url = 'https://api.doctorxiong.club/v1/fund'
    return XiongAPI(url,code)['data']

def stock_board():  
    url = 'https://api.doctorxiong.club/v1/stock/board'
    return XiongAPI(url)['data']

if __name__ == '__main__':
    code_list = ['005827','163417','004997','002939','000977','519694','001218','519772','005918','161725','002984']
    fundDetail = BaseInfo(code_list)
    board = stock_board()
    print(board)
    print('---')
    print(fundDetail)

import requests

def stock():
    url = 'https://api.doctorxiong.club/v1/stock/min?code=002441'
    res = requests.get(url).json()
    changePercent = res['data']['changePercent']
    name = res['data']['name']
    print(f'{name}: {changePercent}%')
    return changePercent

if __name__ == '__main__':
    stock()

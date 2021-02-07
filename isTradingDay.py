


def isTradingDay():
    import json
    import requests
    import time
    today = time.strftime('%Y%m%d', time.localtime())
    # day = today
    day = '20210220'
    url = f'https://api.apihubs.cn/holiday/get?date={day}&workday=1&weekend=2&size=31'
    try:
        resp = requests.get(url)
        r = resp.json()
        if r['data']['list']:
          return True
        else:
          return False
    except:
        raise Exception(f'{url}接口调用失败')


print(isTradingDay())

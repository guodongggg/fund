import requests


def nasdaq():
    url = "http://hq.sinajs.cn/?rn=1609213839262&list=gb_$ndx"
    r = requests.get(url)
    response = r.text
    if r.status_code == 200:
        data = response.split('=')[1].split(',')
        nasdaq_data = {'name': data[0].strip('"'), 'code': 'nasdaq100', 'price': data[1], 'priceChange': data[4], 'expectGrowth': data[2], 'lastWeekGrowth': '-', 'lastMonthGrowth': '-', 'lastThreeMonthsGrowth': '-', 'date': ''}
        return nasdaq_data
    else:
        print(f'nasdaq return error: \n {response}')


if __name__ == '__main__':
    nasdaq_data = nasdaq()
    for k, v in nasdaq_data.items():
        print(f'{k}: {v}')

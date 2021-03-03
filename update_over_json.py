import average_growth
import json
import common
import choose_api
from pathlib import Path


def over_time(detail, board):
    """
    判断当日持仓的所有基金的合计涨幅是否超过沪深300
    :param code_list: list 基金代码列表
    :return: json文件，格式如下，HS300涨幅、持仓合计涨幅、持仓涨幅是否超过沪深300
        {
            "2020-12-31": {
                "HS300": "1.91",
                "my_position": "1.35",
                "over_take": false
            },
            "2021-01-04": {
                "HS300": "1.08",
                "my_position": "1.33",
                "over_take": true
            }
        }
        ......
    """
    # 获取日期
    try:
        date = detail[0]['netWorthDate']
    except:
        date = detail[1]['netWorthDate']
    hs300 = ''
    for i in board:
        if i['name'] == '沪深300':
            hs300 = i['changePercent']

    # 判断文件是否存在，不存在则创建
    json_file_name = 'file/bj.json'
    file = Path(json_file_name)
    file.touch(exist_ok=True)

    # 此时更新的准确净值涨幅的平均值
    avg = average_growth.average_growth(detail)['average_dayGrowth']
    print('hs300:', hs300)
    print('avg:', avg)
    # 写入文件
    with open("file/bj.json", 'r+') as f:
        try:
            data = json.load(f)
            f.seek(0, 0)
            f.truncate()
        except Exception as e:
            print(e)
            data = {}
        finally:
            print(f'获取数据: {data}')
            data[date] = {
                'HS300': hs300,
                'my_position': str(avg),
                'over_take': True if float(avg) > float(hs300) else False
            }
            print(f'更新数据: {date}:{data[date]}')
            f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
            print(f'{json_file_name} 已更新!')


if __name__ == '__main__':
    code_list = common.get_codelist('product')
    data = choose_api.choose_api(code_list)
    detail = data['detail']
    board = data['board']
    over_time(detail, board)

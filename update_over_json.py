import time
import datetime
import average_growth
import json
import fund_base
from pathlib import Path


def over_time(code_list):
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
    end_time = f"{date_today} 15:00"
    # end_time = f"2020-12-31 12:00"
    end_time_stamp = time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M'))
    now_time_stamp = time.mktime(time.strptime(date_now, '%Y-%m-%d %H:%M'))

    # 获取数据
    board = fund_base.stock_board()
    detail = fund_base.BaseInfo(code_list)
    hs300 = ''
    for i in board:
        if i['code'] == 'sz399300':
            hs300 = i['changePercent']

    # 判断文件是否存在，不存在则创建
    json_file_name = 'bj.json'
    file = Path(json_file_name)
    file.touch(exist_ok=True)

    if int(now_time_stamp) > int(end_time_stamp):
        avg = average_growth.average_growth(detail)
    else:
        print(f"{date_now} 当前未休市，更新的仅为估值数据")
        avg = average_growth.average_growth(detail, real=True)

    with open("bj.json", 'r+') as f:
        try:
            data = json.load(f)
            f.seek(0, 0)
            f.truncate()
        except Exception as e:
            print(e)
            data = {}
        finally:
            print(f'get {json_file_name} data: {data}')
            data[date_today] = {
                'HS300': hs300,
                'my_position': str(avg),
                'over_take': True if float(avg) > float(hs300) else False
            }
            print(f'update data: {data[date_today]}')
            f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
            print(f'{json_file_name} update!')


if __name__ == '__main__':
    code_list = ['005827', '163417', '001218', '001714', '162605', '001102', '161725', '002984', '004070']
    over_time(code_list)

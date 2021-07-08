import CodeListApi
import choose_api
import common
from time import sleep


def main():
    #  更新昨日盈亏
    print('获取代码列表...')
    code_list = common.get_codelist('product')
    print('获取基金详情...')
    all_fund_info = choose_api.choose_api(code_list)['detail']
    f = CodeListApi.CodeListApi()
    for fund in all_fund_info:
        dayGrowth = float(fund['dayGrowth'])
        code = fund['code']
        print(f'{code} {fund["name"]} 昨日涨幅:{dayGrowth}%')
        res = f.read(code)
        count = ''
        if res['result']:
            print(f'接口返回值：{res}')
            count = res['message']['count']
        else:
            assert 'CodeListApi接口返回值异常'
        dayGrowthMoney = int(count * float(100+dayGrowth) / 100)
        print(f'{code} {fund["name"]} 最新持仓额：{dayGrowthMoney}')
        f.update(code, dayGrowthMoney, date=common.timeTips())
        print('-'*50)
        sleep(1)
    return True


if __name__ == '__main__':
    main()
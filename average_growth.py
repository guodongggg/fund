import json
import choose_api
import common
import countMoney
import os


def average_growth(fund_data_list):
    """
    统计持仓比例下的预期总收益百分比
    :param fund_data_list: list 通过接口标准返回值
    :return: dict 预估/昨日总收益百分比，不含百分号
    """

    with open(os.path.join('file', 'code_list.json'), 'r', encoding='UTF-8') as f:
        json_data = json.load(f)
        prod_data = json_data['product']

        def growth_list(day):
            return [float(x[day])*prod_data[x['code']]['percent'] for x in fund_data_list if x['code'] in list(prod_data.keys())]

        list_expectGrowth = growth_list('expectGrowth')
        list_dayGrowth = growth_list('dayGrowth')
    average = lambda x: round(sum(x), 2)
    return {'average_expectGrowth': average(list_expectGrowth), 'average_dayGrowth': average(list_dayGrowth)}


if __name__ == '__main__':
    print('查询当前预估收益...')
    code_list = common.get_codelist('product')
    data = choose_api.choose_api(code_list)
    detail, board = data['detail'], data['board']
    average = average_growth(detail)
    average_expectGrowth = average['average_expectGrowth']
    average_dayGrowth = average['average_dayGrowth']
    print('-'*50)
    for i in detail:
        print(f"{common.aligns(i['name'],18)} {i['code']}  估值：{' '+i['expectGrowth'] if float(i['expectGrowth'])>=0 else i['expectGrowth']}%")
    print('-'*50)
    for i in board:
        if i['name'] == '上证指数' or i['name'] == '沪深300':
            print(f"{i['name']}: {i['changePercent']}%")
    print('-'*50)
    except_Money = "{:.2f}".format(countMoney.c('product') * average_expectGrowth * 0.01)
    print(f'估值涨幅: {average_expectGrowth}%  ￥:{except_Money}  昨日涨幅: {average_dayGrowth}%')


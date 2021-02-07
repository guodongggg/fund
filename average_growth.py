import json
import choose_api
from common import get_codelist
from common import aligns


def average_growth(fund_data_list):
    """
    统计持仓比例下的预期总收益百分比
    :param fund_data_list: list 通过接口标准返回值
    :return: dict 预估/昨日总收益百分比，不含百分号
    """
    with open('file/code_list.json', 'r', encoding='UTF-8') as f:
        json_data = json.load(f)
        prod_data = json_data['product']
        list_expectGrowth = [float(x['expectGrowth'])*prod_data[x['code']]['percent'] for x in fund_data_list if x['code'] in list(prod_data.keys())]
        list_dayGrowth = [float(x['dayGrowth']) * prod_data[x['code']]['percent'] for x in fund_data_list if x['code'] in list(prod_data.keys())]
    # or list_ = list(map(lambda x: float(x['expectGrowth'])*fund_precentage[x['code']], fund_data_list))
    # print(list_)
    average_expectGrowth = round(sum(list_expectGrowth), 2)
    average_dayGrowth = round(sum(list_dayGrowth), 2)
    return {'average_expectGrowth': average_expectGrowth, 'average_dayGrowth': average_dayGrowth}


if __name__ == '__main__':
    code_list = get_codelist('product')
    data = choose_api.choose_api(code_list)
    detail, board = data['detail'], data['board']
    average = average_growth(detail)
    average_expectGrowth = average['average_expectGrowth']
    average_dayGrowth = average['average_dayGrowth']
    print('-' * 50)
    for i in detail:
        print(f"{aligns(i['name'],18)} {i['code']}  估值：{i['expectGrowth']}%")
    print('-'*50)
    for i in board:
        if i['name'] == '上证指数' or i['name'] == '沪深300':
            print(f"{i['name']}: {i['changePercent']}%")
    print('-'*50)
    print('平均涨幅:', average_expectGrowth, '%')

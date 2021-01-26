import fund_base
import fund_howbuy
import nasdaq
import json


def average_growth(fund_data_list, real=False):
    """
    统计持仓比例下的预期总收益百分比
    :param fund_data_list: list 通过接口标准返回值
    :param real: boolean 判断是否为真实涨幅
    :return: str 当天总收益百分比，不含百分号
    """
    with open('file/code_list.json', 'r', encoding='UTF-8') as f:
        json_data = json.load(f)
        prod_data = json_data['product']
    if not real:
        list_ = [float(x['expectGrowth'])*prod_data[x['code']]['percent'] for x in fund_data_list if x['code'] in list(prod_data.keys())]
    else:
        list_ = [float(x['dayGrowth']) * prod_data[x['code']]['percent'] for x in fund_data_list if x['code'] in list(prod_data.keys())]
    # or list_ = list(map(lambda x: float(x['expectGrowth'])*fund_precentage[x['code']], fund_data_list))
    print(list_)
    total = round(sum(list_), 2)
    return total


if __name__ == '__main__':
    with open('file/code_list.json', 'r', encoding='UTF-8') as f:
        json_data = json.load(f)
        code_list = list(json_data['product'].keys())
    detail = fund_base.BaseInfo(code_list)

    board = fund_base.stock_board()
    if not detail:
        detail = fund_howbuy.asyncio_(code_list)
    average = average_growth(detail)  # 注意：此处调用会将nasdaq字典的自定义数据加入到了detail列表中
    if not board:
        board = fund_howbuy.stock()
    for i in detail:
        print(f"{i['name']} {i['code']} 实时估值：{i['expectGrowth']}%")
    print('---------------')
    # for i in board:
    #     if i['name'] == '上证指数' or i['name'] == '沪深300':
    #         print(f"{i['name']}: {i['changePercent']}%")
    # print('---------------')
    print('平均涨幅', average, '%')

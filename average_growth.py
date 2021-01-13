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
    # 1/13卖出nasdaq基金
    # nasdaq_data = nasdaq.nasdaq()
    # print('nasdaq_data: ',nasdaq_data)
    # fund_data_list.append(nasdaq_data)

    # for i in fund_data_list:
    #     print(i['name'], i['expectGrowth'])
    # fund_precentage = {
    #     '005827': 0.12,  # 易方达蓝筹精选混合
    #     '163417': 0.13,  # 兴全合宜混合(LOF)A
    #     '001714': 0.03,  # 工银文体产业股票A
    #     '162605': 0.12,  # 景顺长城鼎益混合LOF
    #     '001102': 0.23,  # 前海开源国家比较优势混合
    #     '161725': 0.02,  # 招商中证白酒指数分级
    #     '002984': 0.03,  # 广发中证环保ETF联接C
    #     '003494': 0.05,  # 富国天惠
    #     '004070': 0.05,  # 南方全指证券联接C
    #     'nasdaq100': 0.27  # 纳斯达克100
    #     }
    with open('file/code_list.json', 'r') as f:
        json_data = json.load(f)
        fund_percent = json_data['percent']
    if not real:
        list_ = [float(x['expectGrowth'])*fund_percent[x['code']] for x in fund_data_list]
    else:
        list_ = [float(x['dayGrowth']) * fund_percent[x['code']] for x in fund_data_list]
    # or list_ = list(map(lambda x: float(x['expectGrowth'])*fund_precentage[x['code']], fund_data_list))
    # print(list_)
    total = round(sum(list_), 2)
    return total


if __name__ == '__main__':
    with open('file/code_list.json', 'r') as f:
        json_data = json.load(f)
        code_list = json_data['product']
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
    for i in board:
        if i['name'] == '上证指数' or i['name'] == '沪深300':
            print(f"{i['name']}: {i['changePercent']}%")
    print('---------------')
    print('平均涨幅', average, '%')

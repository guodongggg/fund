import nasdaq
import fund_base
import fund_howbuy
import nasdaq


def average_growth(fund_data_list, real=False):
    nasdaq_data = nasdaq.nasdaq()
    # print('nasdaq_data: ',nasdaq_data)
    fund_data_list.append(nasdaq_data)
    # for i in fund_data_list:
    #     print(i['name'], i['expectGrowth'])
    fund_precentage = {
        '005827': 0.1,
        '163417': 0.11,
        '001218': 0.29,
        '001714': 0.03,
        '162605': 0.07,
        '001102': 0.06,
        '161725': 0.02,
        '002984': 0.02,
        '004070': 0.07,
        'nasdaq100': 0.23}
    if not real:
        list_ = [float(x['expectGrowth'])*fund_precentage[x['code']] for x in fund_data_list]
    else:
        list_ = [float(x['dayGrowth']) * fund_precentage[x['code']] for x in fund_data_list]
    # or list_ = list(map(lambda x: float(x['expectGrowth'])*fund_precentage[x['code']], fund_data_list))
    # print(list_)
    total = round(sum(list_), 2)
    return total


if __name__ == '__main__':
    code_list = ['005827','163417','001218','001714','162605','001102','161725','002984','004070']
    detail = fund_base.BaseInfo(code_list)
    board = fund_base.stock_board()
    if not detail:
        detail = fund_howbuy.asyncio_(code_list)
    average = average_growth(detail, real=False)  # 注意：此处调用会将nasdaq字典的自定义数据加入到了detail列表中
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

import nasdaq
import fund_base
import fund_howbuy


def average_growth(fund_data_list):
    nasdaq_data = nasdaq.nasdaq()
    print('nasdaq_data: ',nasdaq_data)
    fund_data_list.append(nasdaq_data)
    for i in fund_data_list:
        print(i['name'], i['expectGrowth'])
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
    list_ = [float(x['expectGrowth'])*fund_precentage[x['code']] for x in fund_data_list]
    # or list_ = list(map(lambda x: float(x['expectGrowth'])*fund_precentage[x['code']], fund_data_list))
    #print(list_)
    total = round(sum(list_), 2)
    return round(total, 2)
    
if __name__ == '__main__':
    code_list = ['005827','163417','001218','001714','162605','001102','161725','002984','004070']
    fundDetail = fund_base.BaseInfo(code_list)  # xiong API
    # fundDetail = fund_howbuy.asyncio_(code_list) # howbuy API
    print(average_growth(fundDetail),'%')
import fund_base
import fund_howbuy
import json


def choose_api(code_list):
    board = ''
    try:
        detail = fund_base.BaseInfo(code_list)
        board = fund_base.stock_board()
        if not detail:
            print("howbuy接口取基金详情")
            detail = fund_howbuy.asyncio_(code_list)
        else:
            if '968061' in code_list:
                mogen_info = fund_howbuy.asyncio_(['968061'])
                detail.insert(0, mogen_info[0])
    except:
        detail = fund_howbuy.asyncio_(code_list)
    if not board:
        print("howbuy接口取大盘详情")
        board = fund_howbuy.stock()
    return {'detail': detail, 'board': board}


if __name__ == '__main__':
    with open('file/code_list.json', 'r', encoding='UTF-8') as f:
        json_data = json.load(f)
        code_list = list(json_data['test'].keys())
    for i in choose_api(code_list)['detail']:
        print(i)
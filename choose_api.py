import fund_base
import fund_howbuy
import common
import decorate


@decorate.timer
def choose_api(code_list):
    board = ''
    try:
        detail = fund_base.BaseInfo(code_list)
        board = fund_base.stock_board()
        if not detail:
            print("主接口无返回值,调用备用接口...")
            detail = fund_howbuy.asyncio_(code_list)
        else:
            if '968061' in code_list:
                mogen_info = fund_howbuy.asyncio_(['968061'])
                detail.insert(0, mogen_info[0])
    except:
        print("主接口异常,调用备用接口...")
        detail = fund_howbuy.asyncio_(code_list)
    if not board:
        print("主接口异常,调用备用接口...")
        board = fund_howbuy.stock()
    return {'detail': detail, 'board': board}


if __name__ == '__main__':
    code_list = common.get_codelist('test')
    for i in choose_api(code_list)['detail']:
        print(i)
    for i in choose_api(code_list)['board']:
        print(i)
from flask import Flask, render_template
import fund_base
from api import API
import fund_howbuy
import average_growth
import json

app = Flask(__name__)


@app.route('/hao')
def haoym_index():
    data = API.hao()
    print(data)
    return render_template('haoym_index.html', data=data)


@app.route('/hao/<post_id>')
def haoym_detail(post_id):
    data = API.hao()
    info = ''
    for i in data:
        if i['postID'] == int(post_id):
            info = i
    print(info)
    return render_template('haoym_detail.html', info=info)


@app.route('/')
def fund():
    with open('file/code_list.json', 'r') as f:
        json_data = json.load(f)
        code_list = json_data['product']
    detail = fund_base.BaseInfo(code_list)
    board = fund_base.stock_board()
    if not detail:
        app.logger.warning("howbuy接口取基金详情")
        detail = fund_howbuy.asyncio_(code_list)
    average = average_growth.average_growth(detail)  # 注意：此处调用将nasdaq的自定义数据加入到了detail列表中
    app.logger.info('--average--: ')
    app.logger.info(average)
    if not board:
        app.logger.warning("howbuy接口取大盘详情")
        board = fund_howbuy.stock()
    app.logger.info('--board--: ')
    app.logger.info(board)
    app.logger.info('--detail--: ')
    app.logger.info(detail)
    context = {
        'board': board,
        'detail': detail,
        'average': average
    }
    return render_template('index.html', **context)


@app.route('/<code>/xxhg')
def test(code):
    import xxhg
    fundGrapper = xxhg.FundGrapper()
    # data = fundGrapper.run('004070')
    data = fundGrapper.run(code, gui=False)
    return render_template('xxhg_pic.html', data=data, code=code)


@app.route('/<code>/xalpha_cccb')
def xalpha_cccb(code):
    import xalpha as xa
    xa.set_display("notebook")
    path = 'file/code.csv'
    read = xa.record(path)
    f = xa.fundinfo(code)
    f_t = xa.trade(f, read.status)
    data = f_t.v_tradecost()
    return render_template('xalpha_cccb.html', data=data, code=code)


@app.route('/xalpha_all')
def xalpha_all():
    import xalpha as xa
    import pandas as pd
    xa.set_display("notebook")
    path = 'file/code.csv'
    read = xa.record(path)
    sysopen = xa.mul(status=read.status)
    annualized_rate = sysopen.xirrrate()  # 整体年化
    annualized_rate = round(annualized_rate*100, 2)
    v_position = sysopen.v_positions()  # 仓位饼状图（小类）
    v_position_all = sysopen.v_category_positions()  # 仓位饼状图（大类）
    v_position_history = sysopen.v_positions_history()  # 仓位水流图
    all_trade = sysopen.v_tradevolume(freq='W')  # 整体交易坐标图
    context = {
        'annualized_rate': annualized_rate,
        'v_position': v_position,
        'v_position_all': v_position_all,
        'v_position_history': v_position_history,
        'all_trade': all_trade
    }
    return render_template('xalpha_all.html', **context)


@app.route('/xalpha_all_td')
def xalpha_all_td():
    import xalpha as xa
    # import pandas as pd
    xa.set_display("notebook")
    path = 'file/code.csv'
    read = xa.record(path)
    sysopen = xa.mul(status=read.status)
    get_stock_holdings = sysopen.get_stock_holdings()
    all_info = sysopen.summary()
    stock_data = get_stock_holdings.to_html(index=False, justify='center')
    html_data = all_info.to_html(index=False, justify='center')
    html = '''
    <html>
        <body>
            <div>{html_data}</div><br />
            <div>{stock_data}</div>
        </body>
    <html>
    '''
    return html.format(html_data=html_data, stock_data=stock_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')

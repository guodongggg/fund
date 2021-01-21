from flask import Flask, render_template, request
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
    # 直接通过JavaScript获取btc的值
    # try:
    #     btc_value = btc.btc()
    # except Exception as e:
    #     print(e)
    #     btc_value = None
    with open('file/code_list.json', 'r', encoding='UTF-8') as f:
        json_data = json.load(f)
        code_list = list(json_data['product'].keys())
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

    mogen_fund = fund_howbuy.asyncio_(['968061'])  # 手动添加摩根太平洋科技
    detail.insert(0, mogen_fund[0])

    app.logger.info('--board--: ')
    app.logger.info(board)
    app.logger.info('--detail--: ')
    app.logger.info(detail)
    context = {
        'board': board,
        'detail': detail,
        'average': average,
        # 'btc_value': btc_value
    }
    return render_template('index.html', **context)


@app.route('/<code>/xxhg')
def test(code):  # 线性回归
    import xxhg
    fund_grapper = xxhg.FundGrapper()
    data = fund_grapper.run(code, gui=False)
    return render_template('xxhg_pic.html', data=data, code=code)


@app.route('/<code>/xalpha_cccb')
def xalpha_cccb(code):  # 持仓成本
    import xalpha as xa
    xa.set_display("notebook")
    path = 'file/new.csv'
    read = xa.record(path)
    f = xa.fundinfo(code)
    f_t = xa.trade(f, read.status)
    data = f_t.v_tradecost()
    return render_template('xalpha_cccb.html', data=data, code=code)


@app.route('/xalpha_all')
def xalpha_all():
    import xalpha as xa
    xa.set_display("notebook")
    path = 'file/new.csv'
    read = xa.record(path)
    sysopen = xa.mul(status=read.status)
    annualized_rate = sysopen.xirrrate()  # 整体年化
    annualized_rate = round(annualized_rate*100, 2)
    v_position = sysopen.v_positions()  # 仓位饼状图（小类）
    v_position_all = sysopen.v_category_positions()  # 仓位饼状图（大类）
    v_position_history = sysopen.v_positions_history()  # 仓位水流图
    all_trade = sysopen.v_tradevolume(freq='W')  # 整体交易坐标图
    sysclose = xa.mulfix(*sysopen.fundtradeobj, totmoney=70000)
    sysclose.bcmkset(xa.indexinfo('1399300'))  # 设置比较基准，开始对此封闭的基金投资系统进行量化评估 首位0
    close_netvalue = sysclose.v_netvalue()  # 基金组合与基准比较收益图
    max_drawdown = sysclose.max_drawdown()  # 最大回撤
    alpha = sysclose.alpha()
    beta = sysclose.beta()
    sharpe = sysclose.sharpe()
    context = {
        'annualized_rate': annualized_rate,
        'v_position': v_position,
        'v_position_all': v_position_all,
        'v_position_history': v_position_history,
        'all_trade': all_trade,
        'close_netvalue': close_netvalue,
        'max_drawdown': max_drawdown,
        'alpha': alpha,
        'beta': beta,
        'sharpe': sharpe
    }
    return render_template('xalpha_all.html', **context)


@app.route('/xalpha_all_td')
def xalpha_all_td():  # 持仓股票份额
    import xalpha as xa
    # import pandas as pd
    xa.set_display("notebook")
    path = 'file/new.csv'
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


@app.route('/zuanbuwan')
def zuanbuwan(showall=False):
    from weibo import weibo
    import os
    print('---开始爬取数据---')
    weibo.main()
    print('---爬取完毕---')
    json_path = os.path.join('weibo', 'weibo', '赚不完亏得完Ryu', '6367430139.json')
    with open(json_path, 'r', encoding='UTF-8') as f:
        data = json.load(f)
        weibo_data = data['weibo']
    sort_list = sorted(weibo_data, key=lambda x: x['created_at'], reverse=True)  # 根据创建日期排序
    # print(f'json data:{sort_list}')
    if not showall:
        sort_list = sort_list[:10]
    return render_template('zuanbuwan.html', weibo_data=sort_list)


# @app.route('/test_post/', methods=['GET', 'POST'])  # 路由
# def test_post():
#     # print('method'+request.values['method']+'text:'+request.values['text'])
#     d1 = request.args.get('method')
#     d2 = request.args.get('text')
#     d = d1+"AND"+d2
#     return "success!:"+d


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')

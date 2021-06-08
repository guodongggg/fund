from flask import Flask, render_template, request
from api import API
import average_growth
import common
import choose_api
import json
import btc
from flask import jsonify
from flask_cors import cross_origin

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
    ua = request.headers.get('User-Agent')
    mobile = common.judge_pc_or_mobile(ua)
    code_list = common.get_codelist('product')
    data = choose_api.choose_api(code_list)
    detail = data['detail']
    board = data['board']
    average = average_growth.average_growth(detail)
    average_expect = average['average_expectGrowth']
    average_dayGrowth = average['average_dayGrowth']
    app.logger.debug(f'--board--:{board}')
    app.logger.debug(f'--detail--:{detail}')
    app.logger.debug(f'--average_expect--:{average_expect}')
    app.logger.debug(f'--average_dayGrowth--:{average_dayGrowth}')
    context = {
        'board': board,
        'detail': detail,
        'average_expect': average_expect,
        'average_dayGrowth': average_dayGrowth,
        'btc': btc.btcfans('bitcoin') if not mobile else None,
        'eth': btc.btcfans('ethereum') if not mobile else None,
        'xmr': btc.btcfans('monero') if not mobile else None,
    }
    if mobile:
        return render_template('index_mobile.html', **context)
    return render_template('index.html', **context)


@app.route('/<code>/xxhg')
def xxhg(code):  # 线性回归
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


@app.route('/weibo/<user>/')
def weibo(user, showall=False):
    global sort_list
    from weibo import weibo
    import os
    username = ''

    def getinfo(username, userid, spider=True):
        print(f'当前用户：{username}')
        if spider:
            print('---开始爬取---')
            weibo.main()
            print('---爬取完毕---')
        json_path = os.path.join('weibo', 'weibo', username, '{}.json'.format(userid))
        with open(json_path, 'r', encoding='UTF-8') as f:
            data = json.load(f)
            weibo_data = data['weibo']
        sort_list = sorted(weibo_data, key=lambda x: x['created_at'], reverse=True)  # 根据创建日期排序
        # print(f'json data:{sort_list}')
        if not showall:
            sort_list = sort_list[:10]
        return sort_list
    if user == "all":
        data = {}
        data['zuanbuwan'] = getinfo("赚不完亏得完Ryu", "6367430139", spider=True)
        data['qunweiwei'] = getinfo("群伟伟", "7169812253", spider=False)
        return render_template('weibo_all.html', weibo_data=data)

    if user == "zuanbuwan":
        sort_list = getinfo("赚不完亏得完Ryu", "6367430139")
    elif user == "qunweiwei":
        sort_list = getinfo("群伟伟", "7169812253")
    return render_template('weibo.html', weibo_data=sort_list, user=username, length=len(sort_list))


@app.route('/weibo/qunweiwei/article/', methods=['post', 'get'])
def wb_article():
    import spider_wb_article
    article_url = request.args.get('url')
    article_title = request.args.get('title')[8:]
    app.logger.debug(f'article title:{article_title}')
    app.logger.debug(f'article url:{article_url}')
    try:
        article_info = spider_wb_article.article(article_url)
    except:
        return f'获取{article_url}内容失败，请检查！'
    # app.logger.debug(f'article info:{article_info}')
    return render_template('wb_article.html', article_info=article_info, article_title=article_title)

@app.route('/api/', methods=['post', 'get'])
@cross_origin()
def test():
    data = [{"name": "name1", "code": "code1"}, {"name": "name2", "code": "code2"}]
    return jsonify(data)

@app.route('/test_post/', methods=['POST'])  # 路由
@cross_origin()
def test_post():
    d = request.values
    print(request.values)
    return {"status": "success"}


if __name__ == '__main__':
    import platform
    if platform.system() == 'Windows':
        print('*Windows测试环境*')
        #webbrowser.open('http://127.0.0.1:8090')
        app.run(debug=True, host='127.0.0.1', port='8090')
    elif platform.system() == 'Linux':
        print('*Linux生产环境*')
        app.run(debug=True, host='0.0.0.0', port='80')

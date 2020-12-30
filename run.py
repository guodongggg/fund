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
    return render_template('haoym_index.html', data = data)

@app.route('/hao/<postID>')    
def haoym_detail(postID):
    data = API.hao()
    info = ''
    for i in data:
        if i['postID'] == int(postID):
            info = i
    print(info)
    return render_template('haoym_detail.html', info = info)    

@app.route('/')
def fund():
    with open('code_list.json','r') as f:
        json_data = json.load(f)
        code_list = json_data['prodect']
    detail = fund_base.BaseInfo(code_list)
    board = fund_base.stock_board()
    if not detail:
        app.logger.warning("howbuy接口取基金详情")
        detail = fund_howbuy.asyncio_(code_list)
    average = average_growth.average_growth(detail) # 注意：此处调用将nasdaq的自定义数据加入到了detail列表中
    app.logger.info('--average--: ')
    app.logger.info(average)
    if not board:
        app.logger.warning("howbuy接口取大盘详情")
        board = fund_howbuy.stock()
    app.logger.info('--board--: ')
    app.logger.info(board)
    app.logger.info('--detail--: ')
    app.logger.info(detail)
    return render_template('index.html', board=board, detail=detail, average=average)

@app.route('/jessie')
def jessie_fund():
    code_list = ['260108','163406']
    detail = fund_base.BaseInfo(code_list)
    board = fund_base.stock_board()
    return render_template('index.html', board=board, detail=detail)
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='80')


from flask import Flask, render_template
import fund_base
from api import API
import fund_howbuy

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
    code_list = ['005827','163417','519694','001218','519772','163406','001714','162605','001102']
    detail = fund_base.BaseInfo(code_list)
    board = fund_base.stock_board()
    if not detail:
        app.logger.warning("howbuy接口取基金详情")
        detail = fund_howbuy.asyncio_(code_list)
    if not board:
        app.logger.warning("howbuy接口取大盘详情")
        board = fund_howbuy.stock()
    app.logger.info('--board--: ')
    app.logger.info(board)
    app.logger.info('--detail--: ')
    app.logger.info(detail)
    return render_template('index.html', board=board, detail=detail)

@app.route('/jessie')
def jessie_fund():
    code_list = ['260108','163406']
    detail = fund_base.BaseInfo(code_list)
    board = fund_base.stock_board()
    return render_template('index.html', board=board, detail=detail)
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='80')


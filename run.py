from flask import Flask, render_template
import fund_base
from api import API

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
    code_list = ['005827','163417','004997','002939','000977','519694','001218','519772','005918','161725','002984']
    detail = fund_base.BaseInfo(code_list)
    board = fund_base.stock_board()
    return render_template('index.html', board=board, detail=detail)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='80')


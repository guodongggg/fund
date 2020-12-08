# encoding: utf-8
import requests
from getstring import get_findAll_urls

class API():
    def __init__(self):
        pass
        
    def hao():
        '''
        通过调用第三方接口，获取薅羊毛的信息
        API地址：https://api.oioweb.cn/api/doc/Newsreport.php
        '''
        url = 'https://api.oioweb.cn/api/Newsreport.php'
        response = requests.get(url)
        res = response.json()
        if res['code'] == 0:
            data = res['data']
            for index, i in enumerate(data):
                url = get_findAll_urls(i['detail'])
                #print("index：", index)
                if url:
                    i['url'] = url[0] if url else None
            return data
        else:
            raise Exception("return error: ", res['code'], res['msg'])
        
if __name__ == '__main__':
    r = API.hao()
    print(r[0])

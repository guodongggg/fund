def get_codelist(env):
    """
    读取指定json文件，返回代码列表
    :param env: porduct test others
    :return: list
    """
    import json
    file_url = './file/code_list.json'
    with open(file_url, 'r', encoding='UTF-8') as f:
        json_data = json.load(f)
        code_list = list(json_data[env].keys())
    return code_list


def aligns(string, length=20):
    """
    字符补全
    :param string:
    :param length:
    :return:
    """
    difference = length - len(string)  # 计算限定长度为20时需要补齐多少个空格
    if difference == 0:  # 若差值为0则不需要补
        return string
    elif difference < 0:
        print('错误：限定的对齐长度小于字符串长度!')
        return None
    new_string = ''
    space = '　'
    for i in string:
        codes = ord(i)  # 将字符转为ASCII或UNICODE编码
        if codes <= 126:  # 若是半角字符
            new_string = new_string + chr(codes + 65248)  # 则转为全角
        else:
            new_string = new_string + i  # 若是全角，则不转换
    return new_string + space * (difference)  # 返回补齐空格后的字符串


def isTradingDay():
    """
    判断指定日期是否为交易日
    http://www.apihubs.cn/#/holiday
    https://blog.csdn.net/u012981882/article/details/112552450
    :rtype:
    :return:
    """
    import requests
    import time
    today = time.strftime('%Y%m%d', time.localtime())
    url = f'https://api.apihubs.cn/holiday/get?date={today}&workday=1&weekend=2&size=31'
    try:
        resp = requests.get(url)
        r = resp.json()
        if r['data']['list']:
            return True
        else:
            return False
    except:
        raise Exception(f'{url}接口调用失败')


if __name__ == '__main__':
    pass

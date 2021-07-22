def count(env='product'):
    import os
    import json
    dir = os.getcwd()
    path = os.sep.join([dir, 'file', 'code_list.json'])
    print('path:',path)
    with open(path, 'r+', encoding='UTF-8') as f:
        data = json.load(f)
        prd = data[env]
        count = 0
        for key, value in prd.items():
            count += value['count']
        print(f'总持仓:￥{count}')
        return count


def get_codelist(env):
    """
    读取指定json文件，返回代码列表
    :param env: porduct test others
    :return: list
    """
    import json
    import os
    dir = os.getcwd()
    path = os.sep.join([dir, 'file', 'code_list.json'])
    with open(path, 'r', encoding='UTF-8') as f:
        json_data = json.load(f)
        code_list = list(i for i in json_data[env].keys() if json_data[env][i]['count'] != 0)  # 持仓若为0，则剔除代码
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


def isTradingDay(date=None):
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
    formatday = time.strftime('%Y/%m/%d', time.localtime())
    if date is None:
        date = today
    url = f'https://api.apihubs.cn/holiday/get?date={date}&workday=1&weekend=2&size=31'
    try:
        resp = requests.get(url, timeout=3)
        r = resp.json()
        if r['data']['list']:
            print(f'{formatday}:交易日')
            return True
        else:
            print(f'{formatday}:非交易日')
            return False
    except:
        # raise Exception(f'{url}接口调用失败')
        print(f'接口异常,默认{formatday}为交易日')
        return True


def getdate(beforeOfDay):
    """
    返回N天前的日期
    param beforeOfDay: int 指定N天前
    return: str
    """
    import datetime
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y%m%d')
    return re_date


def judge_pc_or_mobile(ua):
    import re
    """
    判断访问来源是pc端还是手机端
    :param ua: 访问来源头信息中的User-Agent字段内容
    :return:
    """
    factor = ua
    print(f'ua:{factor}')
    is_mobile = False
    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp' \
                    r'|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)' \
                    r'|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)' \
                     r'|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)' \
                     r'|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw' \
                     r'|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8' \
                     r'|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit' \
                     r'|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)' \
                     r'|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji' \
                     r'|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx' \
                     r'|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi' \
                     r'|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)' \
                     r'|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg' \
                     r'|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21' \
                     r'|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-' \
                     r'|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it' \
                     r'|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)' \
                     r'|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)' \
                     r'|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit' \
                     r'|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'

    _short_matches = re.compile(_short_matches, re.IGNORECASE)
    try:
      if _long_matches.search(factor) != None:
          is_mobile = True
      user_agent = factor[0:4]
      if _short_matches.search(user_agent) != None:
        is_mobile = True
    except:
        pass

    return is_mobile


def timeTips():
    from datetime import datetime
    now = datetime.now()
    strtime = now.strftime("%Y-%m-%d %H:%M:%S")
    return strtime


if __name__ == '__main__':
    print(get_codelist('product'))

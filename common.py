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
            new_string = new_string + chr(codes+65248) # 则转为全角
        else:
            new_string = new_string + i  # 若是全角，则不转换
    return new_string + space*(difference)  # 返回补齐空格后的字符串


if __name__ == '__main__':
    pass

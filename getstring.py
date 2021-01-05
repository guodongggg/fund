# encoding: utf-8
import re


# 自定义获取文本电子邮件的函数
def get_findAll_emails(text):
    """
    :param text: 文本
    :return: 返回电子邮件列表
    """
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
    return emails


# 自定义获取文本手机号函数
def get_findAll_mobiles(text):
    """
    :param text: 文本
    :return: 返回手机号列表
    """
    mobiles = re.findall(r"1\d{10}", text)
    return mobiles


# 自定义获取文本url函数
def get_findAll_urls(text):
    """
    :param text: 文本
    :return: 返回url列表
    """
    urls=re.findall(r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|([a-zA-Z]+.\w+\.+[a-zA-Z0-9\/_]+)",text)
    urls=list(sum(urls,()))
    urls=[x for x in urls if x!='']
    return urls


# 自定义获取获取ip地址函数
def get_findAll_ips(text):
    """
    :param text: 文本
    :return: 返回ip列表
    """
    ips = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", text)

    return ips


if __name__ == '__main__':
    content = "Please 42.121.252.58:443 contact 127.0.0.1  15988455173 us 18720071239 https://blog.csdn.net/u013421629/ at https://www.yiibai.com/ contact@qq.com for further information 1973536419@qq.com You can  also give feedbacl at feedback@yiibai.com"
    emails=get_findAll_emails(text=content)
    print(emails)
    moblies=get_findAll_mobiles(text=content)
    print(moblies)
    urls=get_findAll_urls(text=content)
    print(urls)
    ips=get_findAll_ips(text=content)
    print(ips)

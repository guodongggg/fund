import requests
import common
import traceback


def btcfans(coinname):
    """
    获取虚拟币当前的市值
    :return: str
    """
    try:
        from lxml import etree
        url = f'https://price.btcfans.com/coin/{coinname}'
        r = requests.get(url, timeout=3).text
        html = etree.HTML(r)
        price = html.xpath('/html/body/div[1]/div[3]/div/div[1]/div[2]/div[1]/div[1]/div[1]/span[2]/text()')[0]
        percent = html.xpath('/html/body/div[1]/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[2]/text()')[0]
        return {'price': price, 'percent': percent}
    except:
        return {'price': "0", 'percent': "0"}


def all():
    coinname_list = {'bitcoin', 'ethereum', 'monero'}
    for i in coinname_list:
        coin = btcfans(i)
        print(common.aligns(i.upper(), 10), common.aligns(coin['percent'], 8), coin['price'])


if __name__ == '__main__':
    all()
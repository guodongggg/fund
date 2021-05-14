import requests


def btcfans(coinname):
    """
    获取btc当前的市值
    :return: str
    """
    try:
        from lxml import etree
        url = f'https://price.btcfans.com/coin/{coinname}'
        r = requests.get(url).text
        html = etree.HTML(r)
        price = html.xpath('/html/body/div[1]/div[3]/div/div[1]/div[2]/div[1]/div[1]/div[1]/span[2]/text()')[0]
        growth = html.xpath('/html/body/div[1]/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[2]/text()')[0]
        return {'price': price, 'growth': growth}
    except:
        raise Exception(f'btcfans获取{coinname}失败')


if __name__ == '__main__':
    coinname_list = {'bitcoin', 'ethereum', 'shiba'}
    for i in coinname_list:
        coin = btcfans(i)
        print(i, coin['price'], coin['growth'])

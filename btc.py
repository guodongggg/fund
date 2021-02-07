import requests


def btc():
    url = 'https://www.usd-cny.com/btc/b.js'
    r = requests.get(url).text
    btc_value = r.split(',')[8]
    return int(btc_value[:5])


def btcfans():
    from lxml import etree
    url = 'https://price.btcfans.com/coin/bitcoin'
    r = requests.get(url).text
    html = etree.HTML(r)
    btc = html.xpath('/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div[1]/text()')[0].strip()[1:]
    return btc


if __name__ == '__main__':
    print('BTC: ', btcfans())

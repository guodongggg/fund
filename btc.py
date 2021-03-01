import requests


def btc():
    def usd_cny():
        try:
            url = 'https://www.usd-cny.com/btc/b.js'
            r = requests.get(url).text
            btc_value = r.split(',')[8]
            return int(btc_value[:5])
        except:
            raise Exception('usd_cny获取btc失败')

    def btcfans():
        try:
            from lxml import etree
            url = 'https://price.btcfans.com/coin/bitcoin'
            r = requests.get(url).text
            html = etree.HTML(r)
            btc = html.xpath('/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div[1]/text()')[0].strip()[1:]
            btc = btc.split('.')[0].replace(',', '')
            return btc
        except:
            raise Exception('btcfans获取btc失败')
    try:
        return usd_cny()
    except:
        return btcfans()


if __name__ == '__main__':
    print('BTC:', btc())

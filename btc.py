import requests


def btc():
    url = 'https://www.usd-cny.com/btc/b.js'
    r = requests.get(url).text
    btc_value = r.split(',')[8]
    return int(btc_value[:5])


if __name__ == '__main__':
    print(btc())
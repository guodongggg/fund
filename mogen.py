import requests
from lxml import etree


def get_mogent() -> dict:
    """
    高精度预估(摩根太平洋科技人民币对冲)净值涨幅
    :rtype: dict
    """
    url = 'https://fund.laykefu.com/?chInfo=ch_share__chsub_CopyLink'
    r = requests.get(url)
    html = etree.HTML(r.text)
    expectGrowth = html.xpath('//*[@id="updown"]/text()')[0].replace('%', '')[:4]
    dayGrowth = html.xpath('/html/body/section/section/div[1]/a[1]/h2/text()')[0].replace('%', '')[:4]
    return {'expectGrowth': expectGrowth, 'dayGrowth': dayGrowth}


if __name__ == '__main__':
    print(get_mogent())

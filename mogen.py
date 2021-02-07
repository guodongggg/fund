import requests
from lxml import etree


def get_mogen(timeout=5):
    """
    高精度预估(摩根太平洋科技人民币对冲)净值涨幅
    :rtype: dict
    """
    url = 'https://fund.laykefu.com/?chInfo=ch_share__chsub_CopyLink'
    try:
        r = requests.get(url, timeout=timeout)
        html = etree.HTML(r.text)
        expectGrowth = html.xpath('//*[@id="updown"]/text()')[0].replace('%', '')[:4]
        dayGrowth = html.xpath('/html/body/section/section/div[1]/a[1]/h2/text()')[0].replace('%', '')[:4]
        mogen_dict = {'expectGrowth': expectGrowth, 'dayGrowth': dayGrowth}
        print(f'摩根高精度估值：获取成功')
        return mogen_dict
    except Exception:
        raise Exception('摩根高精度估值：获取超时')


if __name__ == '__main__':
    print(get_mogen(timeout=20))


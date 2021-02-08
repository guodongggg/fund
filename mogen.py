import requests
from lxml import etree
import decorate
import common


@decorate.timer
def get_mogen():
    """
    高精度预估(摩根太平洋科技人民币对冲968061)净值涨幅
    :rtype: dict
    """
    url = 'https://fund.laykefu.com/?chInfo=ch_share__chsub_CopyLink'
    while True:
        try:
            r = requests.get(url, timeout=5)
            html = etree.HTML(r.text)
            expectGrowth = html.xpath('//*[@id="updown"]/text()')[0].replace('%', '')[:4]
            dayGrowth = html.xpath('/html/body/section/section/div[1]/a[1]/h2/text()')[0].replace('%', '')[:4]
            if common.isTradingDay():
                mogen_dict = {'expectGrowth': expectGrowth, 'dayGrowth': dayGrowth}
            else:
                mogen_dict = {'expectGrowth': expectGrowth, 'dayGrowth': expectGrowth}
            print(f'摩根高精度估值：获取成功')
            return mogen_dict
        except Exception:
            #  raise Exception('摩根高精度估值：获取超时')
            import time
            print('摩根高精度估值：获取超时,重试...')
            time.sleep(1)


if __name__ == '__main__':
    print(get_mogen())


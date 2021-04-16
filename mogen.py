import requests
from lxml import etree
import decorate
import common


@decorate.timer
def get_mogen(retry=3):
    """
    高精度预估(摩根太平洋科技人民币对冲968061)净值涨幅
    天天基金：http://overseas.1234567.com.cn/968061
    :param: retry int 重试次数
    :rtype: dict
    """
    url = 'https://fund.laykefu.com/?chInfo=ch_share__chsub_CopyLink'
    count = 0
    while True:
        try:
            r = requests.get(url, timeout=5)
            html = etree.HTML(r.text)
            expectGrowth = html.xpath('//*[@id="updown"]/text()')[0].replace('%', '')[:4]
            dayGrowth = html.xpath('/html/body/section/section/div[1]/a[1]/h2/text()')[0].replace('%', '')[:4]
            now = common.timeTips()
            print(f'[{now}]摩根高精度估值：获取成功')
            if common.isTradingDay():
                mogen_dict = {'expectGrowth': expectGrowth, 'dayGrowth': dayGrowth}
            else:
                mogen_dict = {'expectGrowth': expectGrowth, 'dayGrowth': expectGrowth}
            return mogen_dict
        except Exception:
            import time
            print(f'摩根高精度估值：获取超时,重试...')
            time.sleep(1)
        count += 1
        if count == retry:
            raise Exception('摩根高精度估值：超过请求次数,退出...')


if __name__ == '__main__':
    print(get_mogen(retry=3))


import requests
from lxml import etree
import time

class Fund:
    """
    该类为爬取https://www.howbuy.com/fund网站基金信息的爬虫
    """
    def __init__(self, code):
        self.code = code

    def ratio(self):
        """实时的增幅估值百分比"""
        url = 'https://www.howbuy.com/fund/ajax/gmfund/valuation/valuationnav.htm?jjdm={}'.format(self.code)
        response = requests.post(url)
        html = etree.HTML(response.text)
        expectGrowth = html.xpath('//li/span[3]/text()')[0].strip()
        #print(expectGrowth)
        data = {}
        data['expectGrowth'] = expectGrowth.replace('%', '')
        return data

    def growth(self):
        """最近1周，1个月，3个月的增幅"""
        url = 'https://www.howbuy.com/fund/{}'.format(self.code)
        response = requests.get(url)
        #print(response.text)
        html = etree.HTML(response.text)
        name = html.xpath('/html/body/div[2]/div[3]/div/div[2]/div/div[1]/div/div[1]/h1/text()')[0]
        value_list = html.xpath('//*[@id="nTab9_0"]/table/tr[2]/td[@class="to-right"]/span/text()')
        #print(value_list)
        lastWeekGrowth, lastMonthGrowth, lastThreeMonthsGrowth = [i.replace('%', '') for i in value_list][1:4]
        data = {}
        data['code'] = self.code
        data['name'] = name
        data['lastWeekGrowth'] = lastWeekGrowth
        data['lastMonthGrowth'] = lastMonthGrowth
        data['lastThreeMonthsGrowth'] = lastThreeMonthsGrowth
        return data

    def output(self):
        expectGrowth = self.ratio()
        growth = self.growth()
        growth.update(expectGrowth)
        return growth

class Stock():
    def __init__(self):
        pass

    def stock(self):
        url = "https://data.howbuy.com/cgi/fund/indexmarketdata.json?q=s_sh000001,s_sz399001,s_sh000300,s_sz399006"
        response = requests.get(url)
        r = response.text
        # print(r.split())
        data = []
        for i in r.split():
            tmp = {}
            info = i.split('~')
            tmp['name'], tmp['code'], tmp['price'], tmp['priceChange'], tmp['changePercent'] = info[1:6]
            data.append(tmp)
        return data


if __name__ == '__main__':
    code_list = ['005827', '163417']
    for i in code_list:
        f = Fund(i)
        print(f.output())
    s = Stock()
    print(s.stock())

from lxml import etree
import asyncio
import aiohttp
import common
import time


async def ratio(code):
    """
    并发爬取单支基金的信息
    :param code: 基金代码
    :return: dict 单支标准返回格式
    """
    conn = aiohttp.TCPConnector(ssl=False)  # 防止ssl报错
    # 实时的估值涨幅
    url_ratio = f'http://www.howbuy.com/fund/ajax/gmfund/valuation/valuationnav.htm?jjdm={code}'
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.request("GET", url=url_ratio) as resp:
            r = await resp.text()
            html = etree.HTML(r)
            tag = True
            n = 1  # 估值循环计数器
            while tag:
                if n >= 5:
                    raise Exception(f'{code}:估值数据请求失败,退出！')
                try:
                    # print(html.xpath('//li/span[3]/text()'))
                    expect_growth = html.xpath('//li/span[3]/text()')[0].strip()
                    tag = False
                except AttributeError as e:
                    print(f'{code}:估值为空:设置为0.00')
                    expect_growth = '0.00'
                    tag = False
                # print(expect_growth)
                except IndexError as e:
                    print(f'{code}:估值数据请求异常,重试...')
                    time.sleep(2)
                    n += 1
            ratio_data = {'expectGrowth': expect_growth.replace('%', '')}
            # print(ratio_data)

    # 最近1周，1个月，3个月的增幅
        url_growth = f'http://www.howbuy.com/fund/{code}'
        async with session.request("GET", url=url_growth) as resp:
            # print(response.text)
            r = await resp.text()
            html = etree.HTML(r)
            name = html.xpath('/html/body/div[2]/div[3]/div/div[2]/div/div[1]/div/div[1]/h1/text()')[0]
            value_list = html.xpath('//*[@id="nTab9_0"]/table/tr[2]/td[@class="to-right"]/span/text()')
            day_growth = html.xpath('//*[@class="shouyi-b shouyi-l b3"]/div/em/text()')[0].replace('%', '')
            last_week_growth, last_month_growth, last_three_months_growth = [i.replace('%', '') for i in value_list][1:4]
            growth_data = {
                'code': code,
                'name': name,
                'lastWeekGrowth': last_week_growth,
                'lastMonthGrowth': last_month_growth,
                'lastThreeMonthsGrowth': last_three_months_growth,
                'dayGrowth': day_growth
            }
            # print(growth_data)
    # 合并数据
    growth_data.update(ratio_data)
    return growth_data


def stock():
    """
    爬取大盘
    :return: 标准返回值
    """
    import requests
    url = "https://data.howbuy.com/cgi/fund/indexmarketdata.json?q=s_sh000001,s_sz399001,s_sh000300,s_sz399006"
    response = requests.get(url)
    r = response.text
    # print(r.split())
    stock_data = []
    for i in r.split():
        tmp = {}
        info = i.split('~')
        tmp['name'], tmp['code'], tmp['price'], tmp['priceChange'], tmp['changePercent'] = info[1:6]
        tmp['date'] = ''
        stock_data.append(tmp)
    return stock_data


def asyncio_(code_list):
    """
    并发执行爬虫
    :param code_list: list 基金代码列表
    :return: 多基金标准返回值
    """
    return_data = []
    tasks = []
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    for code in code_list:
        tasks.append(asyncio.ensure_future(ratio(code)))
    loop.run_until_complete(asyncio.wait(tasks))
    for i in tasks:
        return_data.append(i.result())
    loop.close()

    # 特殊处理摩跟太平洋科技基金
    mogen_code = '968061'
    if mogen_code in code_list:
        try:
            import mogen
            mogen_pro = mogen.get_mogen()
            for i in return_data:
                if i['code'] == mogen_code:
                    i['expectGrowth'] = mogen_pro['expectGrowth']
                    i['dayGrowth'] = mogen_pro['dayGrowth']
        except:
            print('摩根高精度估值：请求超时,切换为普通估值')
    return return_data


if __name__ == '__main__':
    s_time = time.time()
    code_list = common.get_codelist('test')
    data = asyncio_(code_list)
    for i in data:
        print(i)
    # for i in stock():
    #     print(i)
    print('用时：{:.2f}'.format(time.time()-s_time))


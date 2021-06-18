import requests
import json


# 线性回归方程
class FundGrapper:
    def threeMonth(self, days=120):
        """
        返回当前日期和三个月前日期的字典
        :param days: 距今天指定天数前的日期
        :return: dict 今天和指定日期前日期的字典
        """
        import time
        import datetime
        now = int(time.time())
        timeStruct = time.localtime(now)
        todayTime = time.strftime("%Y-%m-%d", timeStruct)

        t = (datetime.datetime.now() - datetime.timedelta(days))
        threeMonthAgo = t.strftime("%Y-%m-%d")
        data = {"todayTime": todayTime, "threeMonthAgo": threeMonthAgo}
        # print(data)
        return data

    def grabHistoryData(self, code, gui):
        if gui:
            date = self.threeMonth()
            startDate = date['threeMonthAgo']
            endDate = date['todayTime']
        else:
            date = self.threeMonth()
            startDate = date['threeMonthAgo']
            endDate = date['todayTime']
        try:
            r = requests.get("https://api.doctorxiong.club/v1/fund/detail?code=" + code + "&startDate=" + startDate + "&endDate=" + endDate)
            value = json.loads(r.text)
            return value['data']['netWorthData']
        except Exception as e:
            print(f'获取历史净值数据失败：{e}')
            return ''

    def grabRuntimeData(self, code):
        try:
            r = requests.get("https://api.doctorxiong.club/v1/fund?code=" + code)
            value = json.loads(r.text)
            return value['data'][0]
        except Exception as e:
            print(f'获取历史日期数据失败：{e}')
            return ''

    def run(self, code, gui):
        import common
        common.timeTips()
        if not gui:
            import matplotlib
            matplotlib.use('Agg')
        from matplotlib import pyplot as plt
        from matplotlib import font_manager
        import numpy as np

        font = font_manager.FontProperties(fname="static/msyh.ttf")
        #fundGrapper = FundGrapper()

        #code = "004070"
        netWorthData = self.grabHistoryData(code, gui)
        runtimeData = self.grabRuntimeData(code)
        assert netWorthData and runtimeData
        netWorthArray = np.array(netWorthData)
        #print(runtimeData)
        #print(netWorthArray)

        plt.figure(figsize=(12, 7))
        plt.title("Fund Code: " + runtimeData['code'], fontproperties=font)
        plt.xlabel("日期", fontproperties=font)
        plt.ylabel("净值", fontproperties=font)

        # 绘制净值线
        x = np.arange(0, len(netWorthData))
        y = netWorthArray[0:,1].astype(np.float)
        plt.plot(x,y)

        # 绘制极小值线
        minValueList = list()
        for index in x:
            if index <= 0 or index >= len(netWorthData) - 1:
                continue
            if y[index] < y[index - 1] and y[index] < y[index + 1]:
                minValueList.append([index, y[index]])
        minValue = np.array(minValueList)
        #print(minValue)
        minX = minValue[0:,0]
        minY = minValue[0:,1]
        plt.plot(minX, minY)

        # 极小值线性回归
        r = np.polyfit(minX, minY, 1)
        regressFunc = lambda x: x*r[0] + r[1]
        plt.plot(minX, regressFunc(minX))

        # 全部值线性回归
        partVal = len(y) - 1
        r = np.polyfit(x[0:partVal], y[0:partVal], 1)
        regressFunc = lambda x: x*r[0] + r[1]
        plt.plot(x[0:partVal], regressFunc(x[0:partVal]))

        # 图例
        plt.legend(labels=['净值', '最小值', '最小值回归', '平均值回归'], prop=font)
        plt.grid = True
        if gui:
            # 显性展示
            plt.show()
            return print('显示图片')
        else:
            import base64
            from io import BytesIO
            # 将图片转换为base64格式
            sio = BytesIO()
            plt.savefig(sio, format='png')
            base64_data = base64.encodebytes(sio.getvalue()).decode()
            plt.close()
            return base64_data


if __name__ == '__main__':
    fundGrapper = FundGrapper()
    data = fundGrapper.run('005733', gui=True)
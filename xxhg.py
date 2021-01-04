import matplotlib
matplotlib.use('Agg')
import requests
import json
from matplotlib import pyplot as plt
from matplotlib import font_manager
import numpy as np
import base64
from io import BytesIO

# 线性回归方程
class FundGrapper:
    def grabHistoryData(self, code):
        startDate = "2020-10-1"
        endDate = "2020-12-30"
        r = requests.get("https://api.doctorxiong.club/v1/fund/detail?code=" + code + "&startDate=" + startDate + "&endDate=" + endDate)
        value = json.loads(r.text)
        return value['data']['netWorthData']

    def grabRuntimeData(self, code):
        r = requests.get("https://api.doctorxiong.club/v1/fund?code=" + code)
        value = json.loads(r.text)
        return value['data'][0]

    def run(self, code):
        #fundGrapper = FundGrapper()

        #code = "004070"
        netWorthData = self.grabHistoryData(code)
        runtimeData = self.grabRuntimeData(code)
        netWorthArray = np.array(netWorthData)
        #print(runtimeData)
        #print(netWorthArray)
        plt.figure(figsize=(10, 7))
        plt.title("Fund Code: " + runtimeData['code'])
        plt.xlabel("date")
        plt.ylabel("netWorth")

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

        #图例
        chinese = font_manager.FontProperties(fname='static/msyh.ttf')
        plt.legend(labels=['净值', '最小值', '最小值回归', '平均值回归'], prop=chinese)

        plt.grid = True
        # 显性展示
        #plt.show()
        sio = BytesIO()
        plt.savefig(sio, format='png')
        data = base64.encodebytes(sio.getvalue()).decode()
        plt.close()
        return data


if __name__ == '__main__':
    fundGrapper = FundGrapper()
    data = fundGrapper.run('004070')
    print(data)
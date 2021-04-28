## 基于python flask开发的基金简单查询工具

### 1) 启动方法
>(非必须）修改new.csv,参照test.csv，首行为基金代码，其次为每支基金在指定日期内的操作，正值为买入金额，负值为赎回份额。具体项目参照[x_alpha项目](https://github.com/refraction-ray/xalpha)

>修改code_list.json文件的prodect为你自己的基金代码，修改count为每支基金的金额，执行同级目录下的update_code_list.py,自动更新持仓百分比

>执行python run.py

ps:初始化比较麻烦，我也暂时没优化，后面再说吧
### 2) web查看方法
* 打开浏览器,访问本地地址：http://127.0.0.1:8090
* 在线示例：http://106.12.49.205

### 3) 功能说明：

* 大盘指数实时情况查看
* 单支基金实时、近一周、近一月、近三月的涨跌情况
* 总持仓实际涨幅、预估涨幅
* 持仓成本图、饼状图、收益详情图（需修改new.csv)
* 线性回归图例
* 外链天天基金页面
* 外链头条大V号
* 外链微博大V号
* 外链比特币
* 外链薅羊毛页面

### 4) 展示:
![image](https://github.com/guodongggg/flask/blob/main/static/web.png)
![image](https://github.com/guodongggg/flask/blob/main/static/xxhg.png)
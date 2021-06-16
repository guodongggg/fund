import json


class CodeListApi:
    def __init__(self):
        self.f = open('file/code_list.json', 'r+', encoding='UTF-8')
        self.source = json.load(self.f)

    def create(self, code, money, fund_type="product"):
        from fund_base import BaseInfo
        data = self.source[fund_type]
        if code not in data:
            fund_info = BaseInfo([code])
            name = fund_info[0]['name']
            data[code] = {"name": name, "count": money, "percent": ""}
            self._reloadfile(data, self.source)
            print(f"{code}新增完成!")
            return {"result": True}
        else:
            print(f"{code}已存在，无法新增")
            return {"result": False}

    def read(self, code, fund_type="product"):
        data = self.source[fund_type]
        print(f"{code}查询完成！")
        try:
            return {"result": True, "message": data[code]}
        except:
            print(f"{code}不存在")
            return {"result": False}

    def update(self, code, money, fund_type="product"):
        data = self.source[fund_type]
        if code in data:
            data[code]['count'] = money
            self._reloadfile(data, self.source)
            print(f"{code}更新完成！")
            return {"result": True}
        else:
            print(f"{code}不存在，无法更新")
            return {"result": False}

    def delete(self, code, fund_type="product"):
        data = self.source[fund_type]
        try:
            data.pop(code)
            self._reloadfile(data, self.source)
            print(f"{code}删除完成！")
            return {"result": True}
        except:
            print(f"{code}不存在，无法删除")
            return {"result": False}

    def _reloadfile(self, data, source):
        count = 0
        for key, value in data.items():
            count += value['count']
        print(f'总持仓:￥{count}')
        for key, value in data.items():
            value['percent'] = float("{:.2f}".format(value['count'] / count))
        self.f.seek(0, 0)
        self.f.truncate()
        self.f.write(json.dumps(source, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    f = CodeListApi()
    # f.update("008087", 6500)
    # f.create('163406', 5000)
    # print(f.read('163406'))
    # f.delete("163406")
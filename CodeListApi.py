import json


class CodeListApi:
    def __init__(self, list_type='product'):
        self.f = open('file/code_list.json', 'r+', encoding='UTF-8')
        self.source = json.load(self.f)
        self.list_type = list_type

    def create(self, code, money):
        from fund_base import BaseInfo
        list_type = self.list_type
        data = self.source[list_type]
        if code not in data:
            fund_info = BaseInfo([code])
            name = fund_info[0]['name']
            data[code] = {"name": name, "count": int(money), "percent": ""}
            _data = self._reloadfile(data, self.source)
            print(f"{code}新增完成!")
            return {"result": True, "data": _data[list_type]}
        else:
            print(f"{code}已存在，无法新增")
            return {"result": False}

    def read(self, code):
        list_type = self.list_type
        data = self.source[list_type]
        print(f"{code}查询完成！")
        try:
            return {"result": True, "message": data[code]}
        except:
            print(f"{code}不存在")
            return {"result": False}

    def update(self, code, money):
        list_type = self.list_type
        data = self.source[list_type]
        if code in data:
            data[code]['count'] = int(money)
            _data = self._reloadfile(data, self.source)
            print(f"{code}更新完成！")
            return {"result": True, "data": _data[list_type]}
        else:
            print(f"{code}不存在，无法更新")
            return {"result": True, "data": data[list_type]}

    def delete(self, code):
        list_type = self.list_type
        data = self.source[list_type]
        try:
            data.pop(code)
            _data = self._reloadfile(data, self.source)
            print(f"{code}删除完成！")
            return {"result": True, "data": _data[list_type]}
        except:
            print(f"{code}不存在，无法删除")
            return {"result": True, "data": data[list_type]}

    # 更新持仓百分比
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
        return self.source


if __name__ == "__main__":
    f = CodeListApi()
    # print(f.update("000971", 0))
    # print(f.create('000008', 5000))
    print(f.read('000971'))
    # print(f.delete("000008"))
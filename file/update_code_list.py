import json

with open('code_list.json', 'r+', encoding='UTF-8') as f:
    data = json.load(f)
    prd = data['product']
    count = 0
    for key, value in prd.items():
        count += value['count']
    print(f'总持仓:￥{count}')
    for key, value in prd.items():
        value['percent'] = float("{:.2f}".format(value['count']/count))
    data['product'] = dict(sorted(prd.items(), key=lambda x: x[1]['count'], reverse=True))
    f.seek(0, 0)
    f.truncate()
    f.write(json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ': ')))

print('更新完成！')
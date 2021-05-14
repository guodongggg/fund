import json
import os


def c(env):
    path = os.sep.join(['file', 'code_list.json'])
    with open(path, 'r+', encoding='UTF-8') as f:
        data = json.load(f)
        prd = data[env]
        count = 0
        for key, value in prd.items():
            count += value['count']
        print(f'总持仓:￥{count}')
        return count


if __name__ == '__main__':
    c('product')
import pandas as pd


def net(code, date, fene):
    import xalpha as xa
    date = f'{date[0:4]}-{date[4:6]}-{date[6:8]}'
    fd = xa.fundinfo(code)
    netvalue = fd.price[fd.price['date'] == date].iat[0, 1]
    f = round(float(fene)/netvalue, 2)
    return f


def run():
    path = 'file/new.csv'
    df = pd.read_csv(path)
    print(df)
    code_list = df.columns
    print(code_list)
    for code in code_list[1:]:
        temp_df = df.loc[:, ['date', code]]
        for i, row in temp_df.iterrows():
            if row[1]:
                if row[1] < 0:
                    suhui = net(code, str(row[0]), row[1])
                    print(f'code:{code} {row[0]} money:{row[1]} fene:{suhui}')
                    df.loc[i, code] = suhui
    print(df)
    df.to_csv('file/out.csv', index=False)


run()
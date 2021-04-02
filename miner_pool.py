import requests

def c3pool():
    url = 'https://api.c3pool.com/miner/42cCoxX7bQbLoBnsNwQ8htCHxW91R9MacTmu96mAjCZBfbG1oHGXZwk1EJsnnkSXfg7VEL4Fmo4Qaf4AatALq1zp5B86B3W/stats'
    try:
        r = requests.get(url, timeout=5)
        hashrate = r.json()
        hashrate_kH = hashrate['hash2']/1000
        latest = "{:.2f}KH/s".format(hashrate_kH)
        return latest
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    print(c3pool())
# chrome driver url: http://npm.taobao.org/mirrors/chromedriver/
from selenium import webdriver
from lxml import etree
import platform
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
import decorate

#@decorate.timer
def article(url, retry=3):
    global chrome_driver
    currentdir = os.getcwd()
    if platform.system() == 'Windows':
        chrome_driver = 'driver\\chromedriver.exe'
    elif platform.system() == 'Linux':
        chrome_driver = 'driver/chromedriver'
    else:
        assert '不支持该系统'

    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('blink-settings=imagesEnabled=false')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(executable_path=chrome_driver, options=options)
    browser.get(url)
    locator = (By.XPATH, "//p[@align='justify']")

    tag = True
    count = 0
    while tag:
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located(locator))
            tag = False
        except Exception as e:
            count += 1
            if count == retry:
                raise Exception('无法获取内容，退出')
            print('retry...')
            time.sleep(3)

    source_page = browser.page_source
    html = etree.HTML(source_page)
    data = dict()
    data["msg"] = html.xpath("//p[@align='justify']/text()")
    data["pic"] = html.xpath("//p[@img-box='img-box']/img/@src")
    return data


if __name__ == '__main__':
    url = 'http://t.cn/A6ckJYjm'
    print(article(url))


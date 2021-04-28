from selenium import webdriver
from lxml import etree
import platform
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import decorate

#@decorate.timer
def article(url):
    global chrome_driver
    if platform.system() == 'Windows':
        chrome_driver = 'more\\chromedriver.exe'
    elif platform.system() == 'Linux':
        chrome_driver = 'more/chromedriver'
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
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located(locator))
    except:
        print("ele can't find")
    #time.sleep(5)
    source_page = browser.page_source
    html = etree.HTML(source_page)
    data = dict()
    data["msg"] = html.xpath("//p[@align='justify']/text()")
    data["pic"] = html.xpath("//p[@img-box='img-box']/img/@src")
    return data


if __name__ == '__main__':
    url = 'http://t.cn/A6cQXzQ0'
    print(article(url))


from lxml import etree
import requests


def bingPic():
    """
    获取bing的背景图片地址
    :return: url地址
    """
    bing_url = 'http://cn.bing.com'
    r = requests.get(bing_url)
    res = r.text
    html = etree.HTML(res)
    img_origin_url = html.xpath('//*[@id="bgImgProgLoad"]/@data-ultra-definition-src')
#    print(img_origin_url)
    url = img_origin_url[0].split('&')[0].replace('UHD', '1920x1080')
    img_url = f'{bing_url}/{url}&rf=LaDigue_1920x1080.jpg&pid=hp'
    return img_url


if __name__ == '__main__':
    print(bingPic())

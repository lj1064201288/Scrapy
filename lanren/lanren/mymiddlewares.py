import re, time
from selenium import webdriver
from fake_useragent import UserAgent
from scrapy.http import HtmlResponse
from scrapy import Request

class LanRenDownloadMiddlewares(object):
    def __init__(self):
        self.ug = UserAgent()

    def process_request(self, request, spider):
        if request.meta.get('chrome', True):
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('-headless')
            browser = webdriver.Chrome(chrome_options=chrome_options)
            # 设置请求头部
            request.headers.setdefault('User-Agent', self.ug.random)
            # 构建浏览器
            browser.get(request.url)
            browser.save_screenshot('1.png')

            # 获取下一页的节点
            try:
                print('请求下一页')
                button = browser.find_element_by_xpath('//*[@id="l"]/div[5]/ul/li[13]/a')
                button.click()
                time.sleep(0.5)
                browser.save_screenshot(('2.png'))
                html = browser.page_source
                return HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8')
            except Exception as e:
                print(e.args)




import time
from selenium import webdriver
from scrapy.http import HtmlResponse


class XiaoHuamiddleware(object):

    def process_request(self,request, spider):
        '''
        自定义中间件
        :param request: 请求对象
        :param spider: 请求爬虫
        :return:
        '''

        print('正在执行中间件...')
        chromeoptions = webdriver.ChromeOptions()
        chromeoptions.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=chromeoptions)
        browser.get(request.url)
        time.sleep(2)
        browser.save_screenshot('1.png')
        js = 'document.documentElement.scrollTop=10000'
        browser.execute_script(js)
        time.sleep(2)
        browser.save_screenshot('2.png')
        html = browser.page_source
        print('中间件执行完毕!')

        return HtmlResponse(url=request.url, request=request, body=html, encoding='utf-8')
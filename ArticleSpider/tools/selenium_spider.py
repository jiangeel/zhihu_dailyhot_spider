# -*-coding=utf-8-*-
__author__ = 'Eeljiang'

from selenium import webdriver
from scrapy.selector import Selector
import pickle
import time


# chrome 不加载图片
# chrome_opt = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_opt.add_experimental_option("prefs", prefs)
# browser = webdriver.Chrome(chrome_options=chrome_opt)

# PhantomJs
# browser = webdriver.PhantomJS(executable_path='/Users/eeljiang/phantomjs-2.1.1-macosx/bin/phantomjs')
# browser.get("https://www.zhihu.com/explore")
# print(browser.page_source)
# browser.quit()

# 执行 js 滚动页面
# for i in range(3):
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
#     time.sleep(1)


# browser.get("https://weibo.com")
# browser.get("https://detail.tmall.com/item.htm?spm=a230r.1.14.1.6087331e0UHPZn&id=562389491680&cm_id=140105335569ed55e27b&abbucket=9&skuId=3696699135152")
# print(browser.page_source)
#
# browser.quit()
# browser.get("https://www.oschina.net/blog")
# browser.find_element_by_css_selector("#loginname").send_keys("15957112261")
# browser.find_element_by_css_selector(".info_list.password input[name='password']").send_keys("&un7)6>WHaHCCdM")
# browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()
#

# #  chrome 无界面运行
# from pyvirtualdisplay import Display
# display = Display(visible=0, size=(800, 300))
# display.start()

browser = webdriver.Chrome()
browser.get('http://www.baidu.com')
print(browser.page_source)
print(browser.title)

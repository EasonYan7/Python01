import re

from selenium import webdriver
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)  # 参数名由chrome_options改成了options
browser.get("http://finance.sina.com.cn/realstock/company/sh000001/nc.shtml")
data = browser.page_source
print(data)

# browser.find_element_by_xpath('//*[@id="kw"]').send_keys('python')
# browser.find_element_by_xpath('//*[@id="su"]').click()

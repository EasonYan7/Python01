import re

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}


def baidu(companyName):
    url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=' + companyName
    res = requests.get(url, headers=headers).text
    p_info = '<p class="c-author">(.*?)</p>'
    p_href = '<h3 class="news-title_1YtI1"><a href="(.*?)"'
    href = re.findall(p_href, res, re.S)
    p_title = '<h3 class="news-title_1YtI1">.*?>(.*?)</a>'
    title = re.findall(p_title, res, re.S)
    p_date = '<span class="c-color-gray2 c-font-normal">(.*?)</span>'
    date = re.findall(p_date, res, re.S)
    p_source = '<span class="c-color-gray c-font-normal c-gap-right">(.*?)</span>'
    source = re.findall(p_source, res)

    for i in range(len(title)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        print(str(i + 1) + ':' + title[i] + '(' + source[i] + ' ' + date[i] + ')')
        print(href[i])


companyName = ['中国华能', '中国大唐', '中国华电', '国家能源', '中国电力']
# 公司名称亦是搜索关键字
for i in companyName:
    try:
        print(i + ' :')
        baidu(i)
        print(i + " 爬取成功")
        print('')
    except:
        print(i + " 爬取失败")
        print('')

import re
import time

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

file1 = open('/Users/sen/PycharmProjects/pythonProject/导出多家信息.csv', 'w')


# 先设立文件夹就保证了 不用每次loop都要创建一个。 w为抹除模式，a为写入

def baidu(companyName, page):
    num = (page - 1) * 10
    url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + companyName + '&pn=' + str(num)
    # rtt = 4 为最新时间为准，=1时为热点值
    res = requests.get(url, headers=headers).text

    file1.write(companyName + '第' + str(page) + '页爬取' + '\n')

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
        data = (str(i + 1) + ':' + title[i] + '(' + source[i] + ' ' + date[i] + ')')
        print(data)
        print(href[i])

        file1.write(data + '\n')
        file1.write(href[i])
        file1.write('\n')
        # 写入每个搜索的小组
    file1.write('-------------------------------------------------------------------------' + '\n')
    # 每个搜索的分界线


companyName = ['中国华能', '中国大唐', '中国华电', '国家能源', '中国电力']
# 公司名称亦是搜索关键字

for i in companyName:
    for j in range(3):
        try:
            print(i + ' :')
            baidu(i, j + 1)
            print(i + '第' + str(j + 1) + "页爬取成功")
            print('')
            time.sleep(1)
        except:
            print(i + '第' + str(j + 1) + "页爬取失败")
file1.close()

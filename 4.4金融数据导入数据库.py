import re
import requests
import pymysql

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}


def baidu(companyName):
    url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=' + companyName + '碳中和'
    # rtt = 4 为最新时间为准，=1时为热点值
    # 在 @companyName 后添加搜索关键字
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
        # 连接数据库
        db = pymysql.connect(host='localhost', user='root', password='sam0807', database='pachong', charset='utf8')

        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        cur = db.cursor()

        # 查询数据
        sql1 = 'SELECT * FROM test WHERE company = %s'
        cur.execute(sql1, companyName)
        data_all = cur.fetchall()
        title_all = []
        for j in range(len(data_all)):
            title_all.append(data_all[j][i])

        # 判断标题是否已经存在
        if title[i] not in title_all:
            sql = 'INSERT INTO test(company,title,href,date,source) VALUES(%s,%s,%s,%s,%s)'
            cur.execute(sql, (companyName, title[i], href[i], date[i], source[i]))
            db.commit()
        cur.close()
        db.close()


# 公司名称亦是搜索关键字
companyName = ['中国华能', '中国大唐', '中国华电', '国家能源', '中国电力']
for i in companyName:
    try:
        baidu(i)
    except:
        print(i + "爬取失败")

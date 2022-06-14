import pymysql as pymysql
import pymysql.cursors

# 定义变量
company = 'alibaba'
title = '测试标题'
href = '测试链接'
source = '测试来源'
date = '测试日期'

# 连接数据库
db = pymysql.connect(host='localhost', user='root', password='sam0807', database='pachong', charset='utf8')

# 插入数据
cur = db.cursor()
sql = 'INSERT INTO test(company,title,href,date,source) VALUES(%s,%s,%s,%s,%s)'
cur.execute(sql, (company, title, href, date, source))
db.commit()
cur.close()  # 关闭对话
db.close()  # 关闭数据库

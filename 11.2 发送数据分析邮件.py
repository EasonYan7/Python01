@Author: Sen Yan
 @Date: 2021/3/28

import smtplib
from email.mime.text import MIMEText
import requests
import re
import pymysql
import time

db = pymysql.connect(host='localhost', user='root', password='sam0807', database='pachong',
                     charset='utf8')
company = '中国华电'
today = time.strftime("%Y-%m-%d")  # 这边采用标准格式的日期格式

cur = db.cursor()  # 获取会话指针，用来调用SQL语句
sql = 'SELECT * FROM article WHERE company = %s'
cur.execute(sql, (company))
data = cur.fetchall()  # 提取所有数据，并赋值给data变量
print(data)
db.commit()  # 这个其实可以不写，因为没有改变表结构
cur.close()  # 关闭会话指针
db.close()  # 关闭数据库链接

# 2.利用从数据库里提取的内容编写邮件正文内容
mail_msg = []
mail_msg.append('<p style="margin:0 auto">尊敬的小主，您好，以下是最近的舆情监控报告，望查阅：</p>')  # style="margin:0 auto"用来调节行间距
mail_msg.append('<br><br>')
mail_msg.append('<p style="margin:0 auto"><b>中国华能舆情报告</b></p>')  # 加上<b>表示加粗
for i in range(len(data)):

    mail_msg.append('<p>' + '   日期： ' + data[i][3] + '      舆情分数： ' + str(data[i][5]) + '</p>')
    href = '<p style="margin:0 auto"><a href="' + data[i][2] + '">' + str(i + 1) + '.' + data[i][1] + '</a></p>'
    mail_msg.append(href)

mail_msg.append('<br>')  # <br>表示换行
mail_msg.append('<p style="margin:0 auto">Bests,</p>')
mail_msg.append('<p style="margin:0 auto">Eason</p>')
mail_msg.append('<p>' + today +'</p>')
mail_msg = '\n'.join(mail_msg)
print(mail_msg)

# 3.添加正文内容
msg = MIMEText(mail_msg, 'html', 'utf-8')

# -------------------------------------------------------------------------

usr = 'yan.1024'
psw = '!'
to = 'm'

# 2.subject
msg['Subject'] = 'TEST8'
msg['From'] = usr
msg['To'] = to

# 3.发送邮件
s = smtplib.SMTP_SSL('smtp.qiye.aliyun.com', 465)
s.login(usr, psw)
s.send_message(msg)
s.quit()

print("success!")

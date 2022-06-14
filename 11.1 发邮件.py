import smtplib
from email.mime.text import MIMEText

usr = 'yan.1024@zmcarbon.com'
psw = ''
to = 'mozzi@gmail.com'

# 1.正文
msg = MIMEText('test')

# 2.subject
msg['Subject'] = 'TEST'
msg['From'] = usr
msg['To'] = to

# 3.发送邮件

s = smtplib.SMTP_SSL('smtp.qiye.aliyun.com', 465)
s.login(usr, psw)
s.send_message(msg)
s.quit()

print("success!")

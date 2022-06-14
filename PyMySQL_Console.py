import pymysql as pymysql
import pymysql.cursors

# 连接数据库
db = pymysql.connect(host='localhost', user='root', password='sam0807', database='pachong', charset='utf8')

name = '阿里巴巴'

def delete(key):
    # 插入数据
    cur = db.cursor()
    sql = 'DELETE FROM test WHERE company = %s'
    cur.execute(sql, name)
    db.commit()
    cur.close()  # 关闭对话
    db.close()  # 关闭数据库


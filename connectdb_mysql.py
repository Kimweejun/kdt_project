import pymysql ## pip install pymysql

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='123456',
                       db = 'tabledb',
                       charset='utf8')
cursor = conn.cursor()

sql = 'SELECT * FROM usertbl'
cursor.execute(sql)

rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()

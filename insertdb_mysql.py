import pymysql

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='123456',
                       db = 'tabledb',
                       charset='utf8')
cursor = conn.cursor()
sql = 'insert into usertbl values(%s, %s, %s, %s, %s, %s, %s, %s);'

try:
    userID = input("아이디 입력 => ")
    name = input("이름 입력 => ")
    birthYear = int(input("생년월일 입력 => "))
    addr = input("주소 입력 => ")
    mobile1 = input("휴대혼번호(앞자리) 입력 => ")
    mobile2 = input("휴대혼번호(뒷자리) 입력 => ")
    height = int(input("키 입력 => "))
    mDate = input("가입날짜(2024-10-30) 입력 => ")

    cursor.execute(sql, (userID, name, birthYear, addr, mobile1, mobile2, height, mDate))
    conn.commit()

    sql = 'SELECT * FROM usertbl'
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as e:
    print("\n입력 오류!!!", e.args[0], "\n")
finally:
    cursor.close()
    conn.close()
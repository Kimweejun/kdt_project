from sangpumCLS import Sangpum
# import sqlite3
import pymysql

def connect_db():
    dbconn = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='123456',
                             db='tabledb',
                             charset='utf8')
    return dbconn

def create_table():
    dbconn = connect_db()

    dbcursor = dbconn.cursor()
    dbcursor.execute("""create table if not exists sangpum (
        code char(4) primary key, 
        irum varchar(10), 
        su int, 
        price int, 
        kumack int 
        )""")

    dbcursor.close()
    dbconn.close()


def f_menu():
    print(" *** 메뉴 ***")
    print("1. 상품정보 입력")
    print("2. 상품정보 출력")
    print("3. 상품정보 조회")
    print("4. 상품정보 수정")
    print("5. 상품정보 삭제")
    print("6. 프로그램 종료")
     
def f_input():
    obj = Sangpum()
    
    print()
    obj.input_data()
    obj.proc_kumack()

    dbconn = connect_db()
    dbcursor = dbconn.cursor()

    sql = "insert into sangpum  values (%s, %s, %s, %s, %s)"
    try:
        dbcursor.execute(sql, (obj.code, obj.irum, obj.su, obj.price, obj.kumack))
        dbconn.commit()
        print("\n상품정보 입력 성공!!\n")
    except Exception as e:
        print("\n상품정보 입력 오류!!!", e.args[0], "\n")
    finally:
        dbcursor.close()
        dbconn.close()


def f_output():
    total_kumack = 0
    
    dbconn = connect_db()
    dbcursor = dbconn.cursor()
    
    dbcursor.execute("SELECT count(*) FROM sangpum")
    cnt = dbcursor.fetchone()[0] # fetchone() :  한개의 레코드(튜플)

    if cnt == 0:
        print("\n출력할 데이터가 없습니다!!!\n")
        return;

    dbcursor.execute("SELECT * FROM sangpum order by code asc")
    res = dbcursor.fetchall()
    print("\n                   *** 상품정보 ***")
    print("======================================================")
    print("상품코드     상품명        수량        단가       판매금액")
    print("======================================================")
    for row in res:
        total_kumack += row[4]
        print("%4s       %4s       %4d       %6d    %8d"
            % (row[0], row[1], row[2], row[3], row[4]))           
    print("======================================================")
    print("\t\t\t\t\t 총판매금액 = %8d\n" % (total_kumack))
    
    dbcursor.close()
    dbconn.close()

def f_search():
    dbconn = connect_db()
    dbcursor = dbconn.cursor()

    code = input("\n조회할 상품코드을 입력하세요 : ")
    dbcursor.execute("SELECT * FROM sangpum where code = %s", (code,))
    row = dbcursor.fetchone()
    if row:
        print("\n상품코드     상품명        수량         단가      판매금액")
        print("======================================================")
        print("%4s       %4s       %4d       %6d     %8d"
              % (row[0], row[1], row[2], row[3], row[4]))
        print("======================================================\n")
    else:
        print("\n조회할 상품코드 %s가 없습니다!!\n" % code)
        
    dbcursor.close()
    dbconn.close()   

def f_update():    
    dbconn = connect_db()
    dbcursor = dbconn.cursor()
    code = input("\n수정할 상품코드를 입력하세요 : ")
    dbcursor.execute("SELECT * FROM sangpum where code = %s", code)
    row = dbcursor.fetchone()
    if row:
        obj = Sangpum()
        obj.code = row[0]
        obj.number_data()
        obj.proc_kumack()

        dbcursor.execute("update sangpum set su=%s, price=%s, kumack=%s where code=%s", \
            (obj.su, obj.price, obj.kumack, obj.code))
        dbconn.commit()
        print("\n상품코드 %s 상품정보 수정 성공!!\n" % code)
    else:
        print("\n수정할 상품코드 %s가 없습니다!!\n" % code)

    dbcursor.close()
    dbconn.close()

def f_delete():
    dbconn = connect_db()
    dbcursor = dbconn.cursor()

    code = input("\n삭제할 상품코드를 입력하세요 : ")
    dbcursor.execute("SELECT * FROM sangpum where code = %s", (code,))
    row = dbcursor.fetchone()
    if row:
        dbcursor.execute("delete from sangpum where code=%s", (code,))
        dbconn.commit()
        print("\n상품코드 %s 상품정보 삭제 성공!!\n" % code)
    else:
        print("\n삭제할 상품코드 %s가 없습니다!!\n" % code)

    dbcursor.close()
    dbconn.close()   

if __name__ == "__main__":
    create_table()
    
    while True:
        f_menu()
        
        menu = int(input("\n메뉴를 선택하세요 : "))
        
        if menu == 1:
            f_input()
        elif menu == 2:
            f_output()
        elif menu == 3:
            f_search()        
        elif menu == 4:
            f_update()        
        elif menu == 5:
            f_delete()        
        elif menu == 6:
            print("\n프로그램 종료...")
            break;
        else:
            print("\n메뉴를 다시 입력하세요!!!\n")
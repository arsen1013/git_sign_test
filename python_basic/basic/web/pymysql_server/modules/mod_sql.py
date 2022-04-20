# sql 모듈 생성
# class 생성 database 
# class 생성이 될 때 pymysql.connect 변수 생성, cursor 생성 (__init__)
# __init__ 제외한 함수 3개 생성 
# execute() -> sql, value 받아와서 sql문을 실행 
# executeAll ( ) -> sql, value 받아와서 실행을 하고 결과값을 return 
# commit() -> 데이터의 변화를 주는 sql문이 실행이 됐을 때 적용하는 commit 함수 만들기 
# execute(), executeAll( ) 함수에서 value 값은 디폴트 { }값 지정 

import pymysql 

class Database():
    def __init__(self):
        self._db = pymysql.connect(
        user = "root",
        password = "pw0426!",
        host = "localhost",
        db = "ubion",
        charset = "utf8"
        )   
        self.cursor = self._db.cursor(pymysql.cursors.DictCursor)
    
    #executeall이 아닌 execute 만 하는 경우는 어떨때 쓰는 걸까? 
    def execute(self,input_sql,input_value={}):
        self.cursor.execute(input_sql,input_value)
        
    def executeAll(self,input_sql, input_value={}):
        self.cursor.execute(input_sql,input_value)
        self.result = self.cursor.fetchall()
        return self.result

    def commit(self):
        self._db.commit()
        # self._db.close()  #일부러 뺐다고 한다 왜? 
    
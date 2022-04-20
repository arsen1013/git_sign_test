from flask import Flask, redirect, render_template, request, url_for 
#flask 라이브러리에서 FLASK 함수를 가져온다. 
import pymysql 
import modules.mod_sql 
#만든 모듈 불러오기 


app = Flask(__name__)
# __name__ : 실행파일, 내가 지금 실행시키고 있는 파일 명이 들어간다. 
# 모듈 안에 __name__이 있다. a 라는 파이썬 파일 안에 __name__이 안에 있다. 
# 그것을 b라는 파이썬 파일에서 a를 불러왔다면? 


# if __name__ = mian 일때 print 가 실행되도록 조건이 걸린다.
#  내가 실행하는 파일과 파일의 이름이 같으면 밑에있는 값이 출력된다. 
# 만약 모듈에서 불러왔을때라면 name과 main이 다르니 실행되지 않을 거다.  


#localhost로 접속했을때 
@app.route('/') 
# /는 빈 URL을 의미한다.
def index():
    #로컬 호스트에 접속 했을 때 로그인창을 띄워보자
    return render_template("index.html")

#index.html 만들고 오기 



# cd web; 
# cd pymysql_server;
# python 220311main.py 
# 실행하면 된다. 물론 실제 서버에서 열때는 vs 코드 밑에서 할 것이 아니라 명령프롬프트에서 실행해야 하긴 한다. 

#local/host/sign-up 으로 접속했을때 (기본은 get의 방식으로 받는다.url 뒤에 ? 를 붙이고 key 값과 value 값이 다 붙어서 주소와 함께 실린다. )
@app.route("/signup/",methods=["GET"])
def signup():
    return render_template("signup.html")
    #여기까지 쓰고 index.html 복사 붙여넣기 해서 똑같은 파일로 signup 이라는 명칭만 바꿔서 html 생성하기 

#여기 부터가 중요. singup 을 post 형식으로 접근했을 때. post는 메세지 안에 실려 보내기 때문에 보안상 get보다 좋지만, 속도가 느리기 때문에 정보에 따라서 혼용해서 사용함. 
@app.route("/signup/",methods=["POST"]) #signup 페이지에서 form 태그에서 제출된 post 타입은 여기서 받는다.  
def signup_2():

    _db = pymysql.connect(
    user = "root",
    password = "pw0426!",
    host = "localhost",
    db = "ubion",
    charset = "utf8"
    )   
    cursor = _db.cursor(pymysql.cursors.DictCursor)
    #cursor는 sql 쿼리문(명령어) 실행을 위한 것


    #이 8개의 변수를 웹 페이지에서 입력값을 받아왔다. 
    _id = request.form["_id"]
    _password = request.form["_password"]
    _name = request.form["_name"]
    _phone = request.form["_phone"]
    _gender = request.form["_gender"]
    _age = request.form["_age"]
    _ads = request.form["_ads"]
    _regitdate= request.form["_regitdate"]

    #쿼리문은 ''' ''' 또는 """ """로 묶어주는 것이 좋다. 줄이 길어지기 때문. 
    sql= """ 
        INSERT INTO user_info VALUES (%s, %s, %s, %s,%s, %s, %s, %s)
        
         """
    _values = [_id, _password, _name, _phone, _ads, _gender, _age, _regitdate]
    cursor.execute(sql,_values)
    _db.commit()
    _db.close() #sql 닫기 

    #request 안에 form이라는 변수가 있음 얘는 데이터 형태가 dic 형태다. key와 value로 구분되어, key값은 signup 경로에서 받은 input의 name 값을 받는다. 
    
    #회원가입한 값이 인덱스로 넘어가야 한다. 
    #print(request.form)
    return redirect(url_for('index')) 
    # 기존에 명시해둔 url로 넘어간다거나 위에 명시한 어딘가의 주소로 이동할때 사용한다. 
    # 이때 이 어디가 url_for index 함수를 요청한다ㅏ.. sing up 페이지를 제출하고 나면 def index가 실행되면서 메인 localhost로 넘어간다
    #함수는 import로 불러오자. 



@app.route("/login/",methods=["POST"])
def login():
    #DB -> SELECT문을 사용 -> index page input ID, PASSWORD 받아와서 
    #select 문으로 조회 
    #결과값이 존재하면 return "login" 존재하지 않으면 return "Fail"
    #index.html 수정, main.py수정 
    # 1. index.html에서 /login url에 post형식으로 접속 //  ID, password를 print로 출력 프론트엔드작업 
    # 2.DB에서 전체 select문을 실행하는 user_infor print() 출력 백엔드 작업 
    # 3. SELECT문에 조건식을 추가해서 데이터의 유무 판별 
    
    #2
    _id = request.form["_id"] #index page에서 딕셔너리 형태로 정보를 받으므로, 그 key 값을 [ " key "] 로 적어준다. 
    _password = request.form["_password"]
    #print(_id, _password)

    #pymysql
    _db = pymysql.connect(
    user = "root",
    password = "pw0426!",
    host = "localhost",
    db = "ubion",
    charset = "utf8"
    )   
    cursor = _db.cursor()


    # sql = """ SELECT * FROM user_info """ 
    # #전체를 다 가져와준다. 
    # cursor.execute(sql)
    # result = cursor.fetchall()
    # _db.close() 
    # #왜 commit을 안할까? 조회만 했지 데이터를 변경하지 않았으므로. 
    # #print(result)
    

    #3. 
    sql = """
        SELECT * FROM user_info WHERE ID = %s AND password = %s 
        """
    _values = [_id, _password]
    cursor.execute(sql,_values)
    result = cursor.fetchall() #데이터 받아오기 
    _db.close() 
    # print(result) 

    if result: 
        # result == Ture 가 기본값이다. 
        return "Login"
    else: 
        return "Fail"


    # return redirect(url_for('index')) #결과값이 뭐가 나오든 상관 없이 다시 인덱스로 넘어간다. 

#포트번호 지정한다. 기본 5000은 위험하다. 80이나 8080이 제일 만만하다. 웹에서 테스트페이지를 여기서 만든다고 한다. 
app.run(port="8080")
# app.run은 맨 마지막에 와야한다.중간에 삽입되면 app.run이후 코드는 실행되지 않는다. 
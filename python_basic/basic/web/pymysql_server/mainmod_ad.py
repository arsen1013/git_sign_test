from flask import Flask, redirect, render_template, request, url_for 
#flask 라이브러리에서 FLASK 함수를 가져온다. 
import modules.mod_sql 
#만든 모듈 불러오기 


app = Flask(__name__) #현재 작동중인 파일이름. 이 안에 mainmod_ad 가 들어간다. 확장자는 미포함. 




# sql에 들어갈 변수값 , 두개 인자값을 만들어 줘야 한다고 
# def execute(self,input_sql,input_value={}):
# 
#그렇게 sql 구문이 만들어 진 것이다. 

#그 다음에 모듈에 있는 클래스를 생성시켜서 그 클래스도 뭔가의 변수에 담아둔다. 왜? 변수에 저장에 시켜둘까? _db = mod_sql.Database()라고 저장하는 이유.
# mod_sql.Database().execute(sql,_values) 로 쓰면 왜 안되는 걸까? 굳이 _db.execute(sql,_values)는 안될까? 
# mod_sql.Database()를 실행함으로써 이 안에 있는 변수가 어디에 저장했는지 알 수 없기 때문이다.  
# class는 어떤 큰 공간을 만들어 두고 그 안에 변수를 지정해 두는 것인데, 클래스는 생성을 그냥 시켜버리면 어딘가에 담아두지 않으면 그게 어디인지 알 수가 없기 때문에 실행 시킬때마다 계속 새로운 클래스를 생성해가져오게 된다. 
# 그래서 이번에 만든 클래스는 어떤 변수라는 공간에 저장할게. 라고 지정하는 것이 _db라는 변수를 지정한 것이다. 
#그래서 _db = mod_sql.Database()는 말하자면, _db에 있는 클래스라고 주소를 고정시켜준다. 
# 이럼으로써 공간이 한정되었기 때문에 sql에 대해 self를 넣지 않을 수 잇었다. 어차피 이 _db안에서 변수를 저장할 수 있기 때문이다.  


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
@app.route("/signup",methods=["GET"])
def signup():
    return render_template("signup.html")

@app.route("/signup",methods=["POST"]) #signup 페이지에서 form 태그에서 제출된 post 타입은 여기서 받는다.  
def signup_2():
    #이 8개의 변수를 웹 페이지에서 입력값을 받아왔다. 
    _id = request.form["_id"]
    _password = request.form["_password"]
    _name = request.form["_name"]
    _phone = request.form["_phone"]
    _gender = request.form["_gender"]
    _age = request.form["_age"]
    _ads = request.form["_ads"]
    _regitdate= request.form["_regitdate"]
    sql = """ 
        INSERT INTO user_info VALUES (%s, %s, %s, %s,%s, %s, %s, %s)
        
         """
    _values = [_id, _password, _name, _phone, _ads, _gender, _age, _regitdate]

    _db = modules.mod_sql.Database()
    #execute 를 사용해서 실행한다.  
    _db.execute(sql,_values)
    _db.commit() #왜 커밋을 클래스 안에 같이 안 넣었을까? 따로 뺀 이유는? 변경되 값이 ㅇ없으면 commit할 필요가없다. 
    #그러나 insert update delete 중 하나를 할텐데 왜 comit을 따로 적었을까? 
    #sql을 에러가 나면 데이터 변화가 없다. 중복으로 넣는 경우가 있을 수 있기 때문임. 지금 과정에는 중복으로 넣는 코드는 아니라서 함께 넣어도 상관은 없다. 
    #executeall은 결과값을 출력해 주는 애니까 SELECT 를 쓸때, 즉 결과값을 출력하고 싶을 때 쓴다.  



    #request 안에 form이라는 변수가 있음 얘는 데이터 형태가 dic 형태다. key와 value로 구분되어, key값은 signup 경로에서 받은 input의 name 값을 받는다. 
    
    #회원가입한 값이 인덱스로 넘어가야 한다. 
    #print(request.form)
    return redirect(url_for('index')) 

    ###################################
    # 기존에 명시해둔 url로 넘어간다거나 위에 명시한 어딘가의 주소로 이동할때 사용한다. 
    # 이 경우 맨 위 def index()가 포함된 route에게 다시 질문을 던지게 된다. 
    # 이때 이 어디가 url_for index 함수를 요청한다ㅏ.. sing up 페이지를 제출하고 나면 def index가 실행되면서 메인 localhost로 넘어간다
    # 함수는 import로 불러오자. 
    #####################################


@app.route("/login",methods=["POST"])
def login():

    _id = request.form["_id"] #index page에서 딕셔너리 형태로 정보를 받으므로, 그 key 값을 [ " key "] 로 적어준다. 
    _password = request.form["_password"]
    #print(_id, _password)
  
    sql = """
        SELECT * FROM user_info WHERE ID = %s AND password = %s 
        """
    _values = [_id, _password]
    _db = modules.mod_sql.Database() #sql에서 데이터를 받아올때 기본적으로 튜플로 받아오지만, 여기선 특별히 딕셔너리로 받아오겠다고 지정했다. 
    result  = _db.executeAll(sql, _values) #이 result 안에 [{'id':'test', 'name':'고길동','핸드폰':'01099339933'},{'id':'test2', 'name':'둘리'... }] 형태로 들어온다. => 리스트로는 0에 위치하고, 그 안의 딕셔너리 키값을 불러오면 된다. 
    #지금까지 실행한 익스큐트는 실행만 한건데, 이제는 데이터 값을 패치홀로 불러들여서 리턴한다. 
    
    # print(result) 

    if result: 
        # result == Ture 가 기본값이다. 
        return render_template("Welcome.html", name = result[0]["name"], id = result[0]["ID"])
        #이 result 안에 [{ }] 형태로 들어온다. => 리스트로는 0에 위치하고, 그 안의 딕셔너리 키값을 불러오면 된다. 
    else: 
        return redirect(url_for('index')) 

#로그인 한 것과 똑같은 방식으로 불러온 다음에, 회원 정보 수정하는 입력값 받아서 수정하기 








# 1. get은
# /login페이지 (XXX님 환영합니다 나오는)
# 밑에 이제 저희가 하이퍼링크로 a태그 달았잖아요!
# 그래서 저희가 '회원정보수정'누르면 다음 페이지로 넘어가는데 이때 이 기능 이 get으로 라우트를 한것 같고요..
# 2. post는 
# 이제 '회원정보수정'누르면 나오는 그페이지에 7가지 속성이 나오잖아요! 그래서 그 7가지 속성은 form태그로 보여주니까 post로 한거 같아요..!

# 저도 이게 웹이 처음이라 이해한정도로 설명드려요 ㅠㅠ흐름은 이런느낌인거 같아요,,핳핳
# 굳이 이렇게 두번 안해도 되고 한번에 해도 된다는게 어떤 느낌인지는 알것 같아요,,, 일부로 두번 적으셨다고 하시네요,,!



#welcome에서 2가지 링크를 만들었는데 그 중 하나가 update다. 
# 그걸 하이퍼 링크를 누르면 get으로 질문을 던진다. 그 질문은..
# 그 질문은 id값도 받고, SELECT문도 실행하는 것이다. 
@app.route("/update", methods=["GET"])
def update():
    id = request.args["_id"]
    sql = """
            SELECT * FROM user_info WHERE ID = %s
            
         """
            # 바꾸기 전에 네 정보가 이렇다. 라는 식으로 한 번 더 확인시켜주기 위해서 한번 더 출력한다. 
            #회원정보 수정이니 전부 가져오고 비교하는 대상은 id가 %s 인 것
            #바꾸고 싶은 것은 바꾸고 나머지는 남기기 위해 
            #유저는 상상도못한 행동을 하기 때문에 사전에 분명하게, 유저의 익숙한 플로우를 따라서 만들어야 한다. UX다. 

            #여기서 %s는 뭘까? 뒤에 있는 변수를 차례대로 넣을 수 있는 공간이다. 스트링이냐 정수냐 실수냐에 따라서 문자가 달라지는데, 
            # mysql에서 스트링으로 넣어도 형태를 확인해서 숫자형이면 숫자로 넣기 때문에서는 %s만 넣어도 알아서 다 집어넣어줄게라고 라이브러리에서도 맘 편하게 %s를 쓰기를 권한다.


    values = [id]
    _db = modules.mod_sql.Database()
    result = _db.executeAll(sql,values)
    #여기까진 그냥 불러오기 함, singup 페이지를 복사해서 수정하자.  
    return render_template("update.html", info = result[0]) #info는 뭐지 
    #딕셔너리 형태로 info는 key, result[0]는 value로 보내준다. 이런 딕셔너리 형태로 info라는 키값으로 보내준다. 



#7 개의 값을 받아와서 정리하는 update sql 쿼리문. 
@app.route("/update",methods=["POST"]) #바디에 정보를 실어서 보낸다. request.args["_id"]를 쓰면 url에서도 받고, post로도 받을 수 있다. 
def update_2():
    _id = request.form["_id"] #프라이머리 키 기준으로  어떤 데이터를 변경할지 정해준다. readonly를 쓰면 id는 고정된다. 
    _password = request.form["_password"]
    _name = request.form["_name"]
    _phone = request.form["_phone"]
    _gender = request.form["_gender"]
    _age = request.form["_age"]
    _ads = request.form["_ads"]
    sql = """ 
        UPDATE user_info SET
        password = %s,
        name = %s,
        phone = %s,
        gender = %s,
        age = %s,
        ads = %s WHERE ID = %s """
        #프라이머리값 id 를 기준으로 
    _values = [_password, _name, _phone, _gender, _age, _ads, _id]
    _db = modules.mod_sql.Database() #클래스 생성
    _db.executeAll(sql,_values)
    _db.commit() #실제 데이터 베이스에 갱신
    return redirect('/') #redirect는 이미 지정한 곳으로 이동하는 것이 아니라 그냥 지금과 다른 어떤 주소(url)로 이동하는 것이다. 
    # 굳이 이 .py안에서 지정한 redict로 이동하는 건 아니다. 
    #return redirect(url_for('index')) 도 된다. 
    #url_for는 함수로 이동하라는거다. 



#회원 탈퇴 
#welcom.html ->. delete url로 접속 <- 로그인 한 ID 값을 같이 전송 
#delete 할 때에는 password를 칠 수 있는 페이지를 만들어(delete.html) 확인해야 한다. -> id와 password가 db에 존재하면 delete 
#존재하지 않으면 패스워드가 맞지 않습니다. 메세지를 페이지에 출력 

@app.route('/delete',methods=["GET"])
def delete():
    #welcome.html에서 /delete?_id{{id}}로 id로 받아왔다. 
    _id = request.args["_id"]
    #deleteconfirm 페이지로 이동
    return render_template("deleteconfirm.html", id = _id)   #키값은 id , values값은 _id로 내보내주기 

@app.route("/delete",methods=["POST"]) 
def delete_2():
    _id = request.form["_id"]
    _password = request.form["_password"]
    _db = modules.mod_sql.Database()  #클래스 생성
    
    #데이터의 유무만 확인
    s_sql = """
            SELECT * FROM user_info WHERE ID = %s AND password = %s 
            """
    d_sql = """ 
            DELETE FROM user_info WHERE ID = %s AND password = %s
             """
             #위에서 검증 했으니 d_ sql은 굳이 확인하지 않아도 된다. 그러면 _values_2 = [_password]로 만들어 써도 된다. 
    _values = [_id, _password]

    #실행시킨다.
    result  = _db.executeAll(s_sql, _values) 
    #여기서 S값이 존재 하면 result 에 값이 들어간다. 

    if not result :
        return "패스워드가 일치하지 않습니다. << 현장에서 이렇게 쓰면 안된다..."
    else: 
        _db.execute(d_sql, _values)
        _db.commit()
        return redirect(url_for('index'))





@app.route("/veiw", methods=["GET"])
def _veiw():
    #sql 문 -> user_info left join ads_info -> user_info ads = ads_info ads
    #columns 값은 user info 에서는 name,ads,age / ads_info 에서는 register_counter 출력하는 쿼리문 작성
    # veiw.html을 render 쿼리문의 결과값을 데이터로 같이 보내주는 코드를 작성 

    sql = """
            SELECT  
            user_info.name, user_info.ads,user_info.age,
            ads_info.register_counter
            FROM user_info 
            LEFT JOIN ads_info 
            ON user_info.ads = ads_info.ads 
            """ 
    _db = modules.mod_sql.Database()  #클래스 생성
    result  = _db.executeAll(sql) 
    #print(result)
    key = list(result[0].keys()) #딕셔너리의 키값을 리스트로 변경
    return render_template ("view.html", info = result[0:], keys = key)

        



#포트번호 지정한다. 기본 5000은 위험하다. 80이나 8080이 제일 만만하다. 웹에서 테스트페이지를 여기서 만든다고 한다. 
app.run(port="8080", debug = True )


#html 변경으로는 디버그가 되지 않으므로, html 수정 후엔 파이썬 파일을 한번 저장해주면 알아서 재실행 된다. 

# app.run은 맨 마지막에 와야한다.중간에 삽입되면 app.run이후 코드는 실행되지 않는다. 




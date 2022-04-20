from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #이렇게 하고 index.html 파일 만들기! 

@app.route('/second/')
def second():
     #_id = request.args.get("html에서 key 값을 input에 있는 name 값으로 id를 줬음")
    _id = request.args.get("id")
    _pass = request.args.get("pass")
    print(_id,_pass)
    return render_template("second.html", id = _id)

    #문자열을 보내주고 싶다면 어떻게 해야하는가? 
    # if _id == "asd" and _pass == "qwe":
    #     return render_template("second.html")
    # else: 
    #     return "로그인에 실패했습니다."

    #입력한 값 확인하는 법 

    #내가 받아온 데이터를 다시 랜더 페이지 하기 위해서는? 내가 입력한 값을 다시 받아오는 법
    #앞에 내가 사용할 수 있도록 key 값을 입력 해줘야 한다. 
    #뭔가의 변수명을 지정해준다. 
    #_id값을 보여주고 싶다면 나는 지금 ID란 이름으로 보내줄건데 이 아이디를 _id라고 보내줄 거다. 할때? 


@app.route("/third/")
def third():
    return "hello"
app.run
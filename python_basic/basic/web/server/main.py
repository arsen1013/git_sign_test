from flask import Flask

app = Flask(__name__) #파일이 실행되면 _name_이라고 자동적으로 들어가게 된다. 



##__name__이라는 하나의 클래스 or 함수 파일을 실행한거고 
# 그걸 app이라는 변수에 저장 하고, 거기서 route 라는 함수를 불러온다. 

@app.route('/') #로컬 호스트 5000번에 들어간다는 특정 URL임 
def index():
    return 'Hello, World'

@app.route('/second/')
def second():
    #구분 편하게 URL과 똑같은 이름으로 저장
    return "i wanna go home"

app.run
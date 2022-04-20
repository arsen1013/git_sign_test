
from flask import Flask, render_template, send_file 
#플라스크 라이브러리 사용해서 웹 연결 
#랜더 템플릿을 통해 html불러옴 
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO 

app = Flask(__name__)


#./ 현재 작업중인 상대 경로. |  ../ 현재 작업중인 파일의 상위 경로

#URL만들때 명령어 사용 
@app.route('/') #로컬 호스트로 즉 빈 URL은 / 
#route가 실행되면 시행될 함수,  
def index(): 
    #return "Hello" #hello 만 나오는거고 
    #render_template 상단에 적어주고 옴
    return render_template('index.html')
    #그리고 index.html 만들어줌 


@app.route('/corona/') #html만든 하이퍼링크의 경로를 만들어줌
def corona():
    #import pandas as pd 상단에 적어주고 옴 
    #corona.csv 데이터를 같은 파일 경로에 넣어줌 
    corona_df = pd.read_csv('corona.csv')

    #컬럼 가져오기 
    corona_df.columns = ["인덱스","등록일시", "사망자","확진자", "게시글번호",
                    "기준일", "기준시간", "수정일시", "누적 의심자", "누적확진률"]
    corona_df.sort_values("등록일시", inplace=True)
    corona_df["일일 확진자"] = (corona_df["확진자"]-corona_df["확진자"].shift()).fillna(0)
    corona_df["일일 사망자"] = corona_df["사망자"].diff().fillna(0)
    corona_df.drop(["인덱스","기준일","게시글번호","기준시간","수정일시"], axis=1, inplace =True)
    corona_df.reset_index(drop=True, inplace=True)
    corona_dict = corona_df.head(10).to_dict() #딕셔너리 형태로 변환, () 정리. 
    #return corona_df.to_html() 이전 초기에 띄울때 버번 
    
    #cnt = len(corona_df) #전체 값이 나옴 
    #cnt = len(corona_df).keys() #해봤자, 키값인 7개 숫자가 전부임 
    cnt = len(corona_dict["등록일시"].keys()) #딕셔너리 안의 딕셔너리의 키값의 수를 구해야함.
                                            #[등록일시][719] = 2022-3-3 의 형태에서 719개의 키값을 len 함!  


    return render_template('corona.html',result = corona_dict,cnt = cnt)#템플릿 사용할땐 이거 사용  #html을 보내서 요청에 대한 응답하는 부분 , result란 이름으로 코로나 딕셔너리란 이름으로 html을 보낸다. 
    # 코로나 html에라는 파일에서는 우리가 코로나 딕셔너리라고 하는 변수의 데이터를 보내줄거다. 
    # 그래서 코로나 딕셔너리라고 하는 파일의 데이텨 key값을 result 라고 지정해 줬으니까. html 파일 상에서 result라는 이름을 써야하낟. 
    # hmtl에서 corona_dict 을 사용할것이 아니라 result란 이름의 key 값을 사용해 줘야한다. result란 이름에 corona_dict이란 변수 내용을 배당한 거니까.
    # result는 이름이다.  cnt 라는 숫자도 하나 내보낸다 (for문을 사용하기 위해) 
 
     


# @app.route("/img/") #슬러시 빼먹지 말자
# def img():
#     #상단에 import matpltlib 설치하고 오기 
#     #send_file 설치
#     values = [1,2,3]#y축  #기존에 했던 plt.show()는 새창에 팝업 띄워주는 것. return해준 값을 보여줘야 하는데 show로 띄워지는 것 밖에 안 됐던 것 
#     plt.plot(values)
#     img_1 = BytesIO()    #plt를 한다음에 바이트로 만들기 위해서 외부 라이브러리를 가져옴 
#     plt.savefig(img_1, format="png", dpi=200) #plt를 하면서 png 포멧으로 200dpi를 해서 savefig 즉, 파일로 저장한것 
#     img_1.seek(0) #이거 넣어야 그림 출력됨. 
#     return send_file(img_1, mimetype = 'image/png')
    
#     #return으로 파일을 보내준다. 웹에 띄워주는게 아니라 파일을 보내주는 것임
#     #렌더 페이지는 페이지 데이터를 보내주겠다라는 거였음 

#     #사실 이걸 사용하기엔 예쁘게 디자인 입히기가 어려워서 json를 사용한 템플릿을 따로 사용하는 것이 좋다.
#     #웹 분야 진출자 아니라면 템플릿 쓰는 것 추천 

@app.route("/img/")
def corona_graph():
    corona_df = pd.read_csv('corona.csv')
    corona_df.columns = ["인덱스","등록일시", "사망자","확진자", "게시글번호",
                    "기준일", "기준시간", "수정일시", "누적 의심자", "누적확진률"]
    corona_df.sort_values("등록일시", inplace=True) #sort_values에서 s 빼먹지 말자... 
    corona_df["일일 사망자"] = corona_df["사망자"].diff().fillna(0)
    decide_cnt = corona_df.head(10)["일일 사망자"].values.tolist()
    state_dt = corona_df.head(10)["등록일시"].values.tolist()
    plt.plot(state_dt, decide_cnt) 
    img_2 = BytesIO()
    plt.savefig (img_2, format = "png", dpi = 200)
    img_2.seek(0)
    return send_file(img_2, mimetype = 'imgae/png')


app.run()
#app.run 도 가능. flask 로 할거면 () 없어도 상관 없음
# 단, python main.py로 할거면 ()는 꼭 붙여주기  


#이렇게 디폴트한 포트번호를 쓰면 해킹당할 수 있으니까, 


#실행할때는 set FLASK_APP=main  // flask run 
#이거 안될때는 phthon main.py 로 실행하자 

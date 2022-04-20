import pandas as pd


#메소드 : 클래스 안의 함수, 클래스 안에서 행동하는 것 
#//단순히 모든 함수가 메소드가 아니라 클래스 안의 함수다. 

class class_dt():
    def __init__(self,input_url):
        self.url = input_url
        
    def csv_read(self,inport_sort= "Country",input_inplace = True):
        self.dt = pd.read_csv(self.url)
        self.dt.sort_values(inport_sort ,inplace = input_inplace ) 
        self.dt.reset_index(drop = True, inplace = True)  
        return self.dt

    def remove_columns(self,input_list = []):
        #빈 리스트를 기본값으로 들어감 
        self.dt.drop(input_list, axis =1 ,inplace= True) 
        return self.dt

    def remove_2(self, input_s_column, inout_e_column):
        self.dt.drop(self.dt.loc[:, input_s_column : inout_e_column], axis =1, inplace =True )
        return self.dt
    

dt = class_dt('./csv/Sales Records.csv')
import pandas as pd
from tqdm import tqdm 
from haversine import haversine
from mlpckg.util_method import *

def make_test(df_all,df_target,Year_Start:int, Year_end:int):
    Year_end += 1
    df_all = latlontogps(df_all)
    df_target = latlontogps(df_target)
    

    #연도 별 dataframe 생성 
    # make dataframe per year.
    df_dict = {'year' + str(i): df_all.loc[df_all["Year"]==i].sort_values(by="Species").reset_index(drop=True) 
           for i in range(Year_Start,Year_end)}  
    
    Species_List= list(df_all.Species.unique())


    # 연도별, 종별 데이터 프레임 생성
    # make dataframe per Year, Species
    for i in Species_List:
        for j in range(Year_Start,Year_end):
            try:
                globals()['{}_{}df'.format(i.split(" ")[1],j)] = df_dict['year' + str(j)].loc[df_dict['year' + str(j)].Species==i].reset_index(drop=True)
            except:
                print(i,"Error")
    
    # 연도와 데이터프레임 인덱스, 종에 따라서  숫자가 저장될 변수들 생성 
    #ex) 예를들어 novemnotata_2007_0 이라는 변수에는 타겟 데이터프레임의 0번째 인덱스에 위치한 관측 지점 주변의 2007년에 발견된 Coccinella novemnotata들의 개수가 저장됨.
    # Create variables for storing recording numbers according to year, data frame index, and species
    #ex) For example, the variable novemnotata_2007_0 stores the number of Coccinella novemnotata discovered in 2007 around the observation point located at the 0th index of the target data frame. 
    for i in range(Year_Start,Year_end):
        for j in range(len(df_target)):
            for k in Species_List:
                globals()['{}_{}_{}'.format(k.split(" ")[1],i,j)] = 0   

    #연도, 종에 따라서 바로 위에서 생성한 변수들을 저장해놓을 리스트 생성
    # Create a list to store the variables created just above, depending on the year and Species
    for i in range(Year_Start,Year_end):
        for j in Species_List:
            globals()['{}list_{}'.format(j.split(" ")[1],i)] = []

    # 타겟 데이터프레임의 관측지점들 주변(18km)에 분포한 종들을 조사하고 위에서 생성한 변수들에 그 숫자를 저장함
    # Investigate species distributed around the observation points of the target data frame (18 km) and store the number in the variables generated above
    for i in tqdm(range(len(df_target))):
        for j in range(Year_Start,Year_end):
            for name in Species_List:
                for k in range(len(globals()['{}_{}df'.format(name.split(" ")[1],j)])):
                    if haversine(globals()['{}_{}df'.format(name.split(" ")[1],j)].gps[k], df_target.gps[i], unit='km') <= 18: ################## 18로 바꿔야함
                        globals()['{}_{}_{}'.format(name.split(" ")[1],j,i)] += 1

    # 종, 연도에 따라 리스트에 변수들 append
    # append variables into the list by species and year
    for name in Species_List:
        for j in range(Year_Start,Year_end):
            for k in range(len(df_target.gps)):
                globals()['{}list_{}'.format(name.split(" ")[1],j)].append(globals()['{}_{}_{}'.format(name.split(" ")[1],j,k)])


    # list들을 dataframe에 값으로 대입하기
    # Inserting lists into columns in a data frame
    for name in Species_List:
        for j in range(Year_Start,Year_end):
            try:
                df_target[name.split(" ")[1]+"_"+str(j)+"_18km"] = globals()['{}list_{}'.format(name.split(" ")[1],j)]
                
            #종 이름에 따라 열이 만들어집니다.
            # 종 이름이 같아 오류가 발생하는 경우도 있습니다.
            # 예외 처리 메시지를 발견한 경우 종 이름이 같은 종에 대한 열 이름을 직접 지정해야 할 수 있습니다.
            #Columns are created based on the species name. 
            # Sometimes there are cases where the error occurs because the species name is the same. 
            # If you find an exception handling message, you may need to name the column for species with the same species name.    
            except:
                print("failed!",name,len(globals()['{}list_{}'.format(name.split(" ")[1],j)]))


    # here is where you name the columns yourself.
    for i in range(Year_Start,Year_end):
        globals()['phoramaculatalist_{}'.format(i)] = globals()['maculatalist_{}'.format(i)][:len(df_target)]
        globals()['gillamaculatalist_{}'.format(i)] = globals()['maculatalist_{}'.format(i)][len(df_target):]
        globals()['boraborealislist_{}'.format(i)] = globals()['borealislist_{}'.format(i)][:len(df_target)]
        globals()['achnaborealislist_{}'.format(i)] = globals()['borealislist_{}'.format(i)][len(df_target):]

    # 실패했던 종들은 따로 코딩해줘야함.
    #You have to code the failed species separately
    name2 = ['boraborealis','achnaborealis','gillamaculata','phoramaculata']
    for name in name2:
        for j in range(Year_Start,Year_end):
            df_target[name+"_"+str(j)+"_18km"] = globals()['{}list_{}'.format(name,j)]
    

    return df_target
            


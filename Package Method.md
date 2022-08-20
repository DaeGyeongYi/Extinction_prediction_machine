# Package Method

## 1. util_method

```python
def latlontogps(frame):
    return frame
```

 데이터 프레임을 인자로 받아서 Latitude와 Longitude를 합친 튜플형태의 컬럼을 추가한 데이터 프레임을 반환함

```python
def remove_sp(frame): 
    return frame
```

데이터 프레임을 인자로 받아서 sp.으로 들어간 애들, 통계적으로 유의미한 수치 이하(30개)의 관측건수를 가진 애들, 속명만 기재된 애들을 제거한 데이터프레임을 반환함

```python
def dropdup(frame): 
    return frame
```

데이터 프레임을 인자로 받아서 gps 오차가 1보다 큰 경우, 위경도가 제대로 기록되지 않은 경우를 제거하고 'Year','Species','Latitude','Longitude'를 기준으로 중복되는 관측건수를 drop한 데이터 프레임을 반환함

```python
def select_key(num:int):
    return target_species,key
```

csv 불러오고 저장하고 할때 귀찮아서 만든 코드. 확인 후 임의로 수정해가면서 쓰는 것이 편할 것.

## 2. stat_method

```python
def custom_mulreg(olsarg:str,df,viewoption=False):
    return res, olsarg
```

다중회귀 분석을 진행하고 각 종들의 pvalues를 체크할수 있는 res를 반환

olsarg는 연속으로 다중회귀를 진행할때 들어갈 변수이름이 반환됨

olsarg : +로 이어지는 종들이름합쳐놓은것

df 데이터프레임

viewoption :TRUE면 진행된 후 결과를 볼 수 있음, FALSE면 안봄

```python
def custom_linreg(df,target_species,viewoption=False):
    return Species_list
```

단순회귀분석을 진행하고 PVALUE가 0.05이하인 종들을 리스트로 반환함

VIEWOPTION: 위오 동일

```python
def custom_vif_varlist(df,varlist:list):
    return featurelist
```

다중공선성을 확인해서 10이하의 것들만 남겨놓은 LIST를 반환함

## 3. make_test

```python
def make_test(df_all,df_target,Year_Start:int, Year_end:int):
    return df_target
```

df_all: 전체종이 들어있는 dataframe

df_target: 테스트파일을 만들고 싶은 종의 dataframe (여러종일경우 한번에 하는것을 추천함.)

year_start : 테스트파일을 위한 조사를 어느년도부터 시작할 것인지

year_end ; 테스트파일을 위한 조사를 어느년도에서 끝날 것인지

df_target에, dataframe에 연도마다 주변 조사(반경 18km)결과를 종별로 컬럼을 생성해서 반환함

## 4. make_train

```python
def make_train(df_all,df_target,target_species):
    return df_fin
```

df_all : 전체종이 들어있는 데이터 프레임

df_target: train 데이터를 만들 종의 테스트 dataframe

target_species: train 데이터를 만들 종의 이름

return: 실제로 관측이 일어났던 연도의 주변 조사 데이터가 df_target에 붙어서 반환됨

## 5. ML_method

```python
def ML(df,targetnum,varlist,varlistname:str
       ,target_species,bagnum=50,repnum=50
       ,testsize=0.1,learningrate=0.7,viewoption=False,to_csv=False):
```

df : 머신러닝 모델이 필요한 dataframe , 위의 make train 함수가 만든 dataframe을 활용하면됨

targetnum : 타겟종의 갯수

varlist: 모델에 사용될 변수 종들의 목록 (list형식으로 넣어야함)

varlistname: csv로 결과를 반환하려고할때 사용된 varlist가 어떤건지 구분하기위함 임의로 지정할것

target_species: 내가 머신에 집어넣을 종 이름

bagnum : presence보다 absence가 많으므로 비율을 맞춰줘야하는데, absence를 일부분만 뽑게됨. 데이터의 편향이 있을 수 있으므로, 다른 absence도 뽑아보는 방식으로 결정됨. 여기서 이 백을 몇번을 뽑아볼 것인지 지정하는 것

repnum: 뽑아본 bag 안에서 몇번이나 머신러닝을 반복할 것인지

testsize: 아는대로

learningrate: 아는대로

viewoption: 머신러닝 한번 돌때마다 결과를 볼것인지

to_csv: csv파일로 지정된 경로로 저장할 것인지.

return: 없음. 지정해둔 경로로 머신러닝 측정 기준을 담은 csv가 반환됨

```python
def structgen(df_target,Sourcelist):
    return df_train, df_test,train_len,test_len
```

df_target: 지금 일반화 해보는 dataframe

sourcelist : list형식으로 시민과학 데이터의 source를 입력해주면 됨


return : 모델에 들어갈 train 데이터 test데이터 train 데이터의 타겟종 개수, test데이터의 타겟종 갯수

```python
def timegen(df_target,sliceYear,target_species,option=0):
    return df_train, df_test,train_len,test_len
```

df_target: 지금 일반화해보는 dataframe

sliceYear: 어떤 년도로 자를것인지

target_species: 타겟되는 종의 이름

option:

0 =>\# 현재 vs 과거

1 = > 과거 vs 현재

return : 모델에 들어갈 train 데이터 test데이터 train 데이터의 타겟종 개수, test데이터의 타겟종 갯수

## 6. final_var_select

```python
def final_var_select(df,targetnum,varlist,target_species
                     ,bagnum=10,repnum=10,testsize=0.1,learningrate=0.7
                     ,returnsize=15,viewoption=False,to_csv=False):
```

df: 샤프 밸류 체크를 진행해볼 dataframe

targetnum : 타겟종의 갯수

varlist: 모델에 사용될 변수 종들의 목록 (list형식으로 넣어야함)

target_species: 내가 머신에 집어넣을 종 이름

bagnum : presence보다 absence가 많으므로 비율을 맞춰줘야하는데, absence를 일부분만 뽑게됨. 데이터의 편향이 있을 수 있으므로, 다른 absence도 뽑아보는 방식으로 결정됨. 여기서 이 백을 몇번을 뽑아볼 것인지 지정하는 것

repnum: 뽑아본 bag 안에서 몇번이나 머신러닝을 반복할 것인지

testsize: 아는대로

learningrate: 아는대로

returnsize: return할때 샤프밸류 몇위까지 내보내줄까를 설정하는 인자

viewoption: 머신러닝 한번 돌때마다 결과를 볼것인지

to_csv: csv파일로 지정된 경로로 저장할 것인지.

return 샤프밸류가 높은 순서대로 returnsize로 설정한 순위까지 잘려서 종이름이 list로 반환됨

## 7. AOO

```python
 def AOO(df_train,df_test,targetnum,varlist
         ,target_species,Year_start,Year_end
         ,bagnum=50,repnum=50,learningrate=0.7,judge_indicator=0.5,to_csv):
```

5_make_AOOcsv.ipynb 파일을 참고하는 것이 좋을 것입니다.

df_train: aoo를 계산하려고하는종의 train 데이터

df_test: aoo를 계산하려고하는 종의 test 데이터

targetnum: aoo를 계산하려고 하는 종의 개수

varlist: 모델에 사용될 변수 종들의 목록 (list형식으로 넣어야함)

year_start : AOO조사를 시작할 연도

year_end ; AOO조사를 끝낼 연도

to_csv: csv파일로 지정된 경로로 저장할 것인지.

bagnum : presence보다 absence가 많으므로 비율을 맞춰줘야하는데, absence를 일부분만 뽑게됨. 데이터의 편향이 있을 수 있으므로, 다른 absence도 뽑아보는 방식으로 결정됨. 여기서 이 백을 몇번을 뽑아볼 것인지 지정하는 것

repnum: 뽑아본 bag 안에서 몇번이나 머신러닝을 반복할 것인지

learningrate: 아는대로

judge_indicator: bag과 rep을 곱한것이 전체, 그중에서 몇퍼센트를 차지해야 있다로 볼것인지.

0.5면 절반 이상 있는 것으로 예측했을때, 있다고 보는것.

to_csv: csv파일을 지정된 경로로 저장할 것인지.

return: 없음. 지정된 경로로 aoo_crawling 파일을 위한 csv가 저장됨

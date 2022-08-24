# Package Method

## 1. util_method

```python
def latlontogps(frame):
    return frame
```

 데이터 프레임의 Latitude와 Longitude열의 데이터를  (lat,lon)형태로 합친 'gps' 열을 생성합니다.

`frame`: 함수의 인자로 들어갈 데이터 프레임

`return`: 함수에 따라 처리된 데이터 프레임

```python
def remove_sp(frame): 
    return frame
```

속명 까지만 기재되거나, sp.로 기재된 데이터, 총 관측건수가 30 이하인 종을 제거합니다.

`frame`: 함수의 인자로 들어갈 데이터 프레임

`return`: 함수에 따라 처리된 데이터 프레임

```python
def dropdup(frame): 
    return frame
```

gps 오차가 1000m보다 큰 데이터와 Latitude,Longitude가 제대로 기록되지 않은 데이터를 제거합니다.

['Year','Species','Latitude','Longitude']를 기준으로 중복되는 데이터들을 한개만 남기고 나머지는 제거합니다.

`frame`: 함수의 인자로 들어갈 데이터 프레임

`return`: 함수에 따라 처리된 데이터 프레임

```python
def select_key(num:int):
    return target_species,key
```

read_csv(), to_csv()를 편하게 이용하기 위해 생성한 함수입니다.

코드를 바꿔가며 사용하거나 사용하지 않아도 무방합니다.

## 2. stat_method

```python
def custom_mulreg(olsarg:str,df,viewoption=False):
    return res, olsarg
```

다중선형회귀 분석을 진행합니다.

`olsarg`: ols 함수에 인자로 들어갈, 종 이름을 '+'로 묶어놓은 string 타입의 변수

`df`:  ols 함수에 data로 들어갈 데이터프레임

`viewoption`: TRUE로 설정하면 res.summary()를 확인할 수 있습니다.



`res`: 각 종들의 pvalues를 체크하거나, 다중회귀분석의 결과를 확인하기 위해 사용합니다. ex) res.pvalues

`olsarg`: 다중회귀분석을 여러번 시행할 때, 다음 다중회귀분석에 들어갈 변수들을 반환함.

```python
def custom_linreg(df,target_species,viewoption=False):
    return Species_list
```

단순선형회귀분석을 진행합니다.

`df`: 회귀분석을 진행할 변수들이 있는 데이터 프레임

`target_species`: 종속변수가 될 종의 이름

`viewoption`: TRUE로 설정하면 각 종마다의 회귀분석 결과를 확인할 수 있습니다.

```python
def custom_vif_varlist(df,varlist:list):
    return featurelist
```

다중 공선성을 확인하여 변수들을 선정합니다.

`df`: 다중공선성을 확인하기 위한 변수들이 속한 데이터프레임

`varlist`: 다중공선성을 확인할 변수들의 리스트

`featurelist` 다중공선성이 10 이하인 변수들만을 남긴 리스트

## 3. make_test

```python
def make_test(df_all,df_target,Year_Start:int, Year_end:int):
    return df_target
```

테스트용 데이터 프레임을 생성합니다.

`df_all`: 전처리가 완료된 모든 데이터 포인트가 기록된 데이터 프레임

`df_target`: 테스트파일을 만들 종의 dataframe (여러종일경우 한번에 하는것을 추천함.)

`year_start`: 조사를 어느년도부터 시작할 것인지를 정하는 인자

`year_end`: 조사를 어느년도에서 끝낼 것인지를 정하는 인자

`return`:  테스트용 데이터 프레임이 반환됨

## 4. make_train

```python
def make_train(df_all,df_target,target_species):
    return df_fin
```

학습용 데이터 프레임을 생성합니다.

`df_all`: 전체종이 들어있는 데이터 프레임

`df_target`: 학습용 데이터를 만들 종의 테스트용 데이터 프레임

`target_species`: 학습용 데이터를 만들 종의 이름

`df_fin`: 학습용 데이터 프레임이 반환됨

## 5. ML_method

```python
def ML(df,targetnum,varlist,varlistname:str
       ,target_species,bagnum=50,repnum=50
       ,testsize=0.1,learningrate=0.7,viewoption=False,to_csv=False):
```

머신러닝을 진행합니다.

`df`: 머신러닝 모델이 필요한 dataframe (학습용 데이터 프레임)

`targetnum`: 타겟종의 갯수

`varlist`: 모델에 사용될 변수 종들의 list

`varlistname`: csv로 결과를 반환하려고할때 사용된 varlist가 어떤건지 구분하기위함. 임의로 지정할것.

`target_species`: 모델에 들어갈 타겟 종의 이름

`bagnum` : presence보다 absence가 많으므로 비율을 맞춰주기 위해서, absence를 일부분만 뽑게됨.

 데이터의 편향이 있을 수 있으므로 다른 absence bag을 몇 번이나 뽑아볼 것인지 지정하는 인자

`repnum`:  하나의 bag 안에서 몇번이나 머신러닝을 반복할 것인지 지정하는 인자

`testsize`: 머신러닝 test size

`learningrate`: 머신러닝 learningrate

`viewoption`: TRUE이면 매 머신러닝마다 그 결과를 볼 수 있음

`to_csv`: TRUE이면 머신러닝의 결과 값들을 지정된 경로에 csv로 저장함

`return`: 없음.

```python
def structgen(df_target,Sourcelist):
    return df_train, df_test,train_len,test_len
```

시민과학 데이터와 구조적 데이터간의 비교를 위해 새로운 train, test set를 생성합니다.

`df_target`: 일반화를 위해 slice해야하는 dataframe

`sourcelist`: 시민과학 데이터의 Source들을 list형식으로 입력받음

`df_train`: 일반화 과정에서 모델에 들어갈 train 데이터 

`df_test`: 일반화 과정에서 모델에 들어갈 test 데이터

`train_len`:  train 데이터의 presence개수

`test_len`:  test 데이터의 presence개수

```python
def timegen(df_target,sliceYear,target_species,option=0):
    return df_train, df_test,train_len,test_len
```

시간 상의 비교를 위해 새로운 train, test set를 생성합니다.

`df_target`: 일반화를 위해 slice해야하는 dataframe

`sliceYear`: 어떤 년도로 자를것인지

`target_species`: 현재 df_target의 presence로 설정된 종(타겟 종)

`option`:

0 =>과거의 년도를 기준으로 70퍼센트정도를 학습한 뒤, 현재의 30퍼센트를 테스트 해보는것

1 = > 현재의 년도를 기준으로 70퍼센트정도를 학습한 뒤, 과거의 30퍼센트를 테스트 해보는것

`df_train`: 일반화 과정에서 모델에 들어갈 train 데이터 

`df_test`: 일반화 과정에서 모델에 들어갈 test 데이터

`train_len`:  train 데이터의 presence개수

`test_len`:  test 데이터의 presence개수

## 6. final_var_select

```python
def final_var_select(df,targetnum,varlist,target_species
                     ,bagnum=10,repnum=10,testsize=0.1,learningrate=0.7
                     ,returnsize=15,viewoption=False,to_csv=False):
```

`df`: shap value를 확인해보려고하는 데이터프레임

`targetnum`: 타겟종의 갯수

`varlist`: 모델에 사용될 변수 종들의 list

`target_species`: 모델에 들어갈 타겟 종의 이름

`bagnum` : presence보다 absence가 많으므로 비율을 맞춰주기 위해서, absence를 일부분만 뽑게됨.

 데이터의 편향이 있을 수 있으므로 다른 absence bag을 몇 번이나 뽑아볼 것인지 지정하는 인자

`repnum`: 하나의 bag 안에서 몇번이나 머신러닝을 반복할 것인지 지정하는 인자

`testsize`: 머신러닝 test size

`learningrate`: 머신러닝 learningrate

`returnsize`: shap value 가 높은 순으로 정렬되는데, 높은 순서대로 몇번째까지 return할지 정해주는 인자.

`viewoption`: TRUE이면 매 머신러닝마다 그 결과를 볼 수 있음

`to_csv`: TRUE이면 결과 값들을 지정된 경로에 csv로 저장함

`return`: 샤프밸류가 높은 순서대로 returnsize로 설정한 순위까지 잘려서 종이름이 list로 반환됨

## 7. AOO

```python
 def AOO(df_train,df_test,targetnum,varlist
         ,target_species,Year_start,Year_end
         ,bagnum=50,repnum=50,learningrate=0.7,judge_indicator=0.5,to_csv):
```

5_make_AOOcsv.ipynb 파일을 참고하는 것이 좋을 것입니다.

`df_train`: aoo를 계산하려고하는종의 학습용 데이터

`df_test`: aoo를 계산하려고하는 종의 테스트 데이터

`targetnum`: aoo를 계산하려고 하는 종의 개수

`varlist`: 모델에 사용될 변수 종들의 list

`year_start `: AOO조사를 시작할 연도

`year_end `: AOO조사를 끝낼 연도

`to_csv`: TRUE이면 결과 값들을 지정된 경로에 csv로 저장함

`bagnum` : presence보다 absence가 많으므로 비율을 맞춰주기 위해서, absence를 일부분만 뽑게됨.

 데이터의 편향이 있을 수 있으므로 다른 absence bag을 몇 번이나 뽑아볼 것인지 지정하는 인자

`repnum`: 하나의 bag 안에서 몇번이나 머신러닝을 반복할 것인지 지정하는 인자

`learningrate`: 머신러닝 learningrate

`judge_indicato`r: bag과 rep을 곱한것이 전체, 그중에서 몇퍼센트를 차지해야 있다로 볼것인지를 결정합니다.

예를들어 이 인자의 값이 0.5면 절반 이상 있는 것으로 예측했을때 그곳에는 타겟종이 존재한다고 보는것입니다.

`to_csv`: TRUE이면 결과 값들을 지정된 경로에 csv로 저장함

`return`: 없음. 지정된 경로로 aoo_crawling 파일을 위한 csv가 저장됨

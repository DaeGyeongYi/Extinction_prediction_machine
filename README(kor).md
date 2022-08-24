# Preproceed

가장 처음 실행할 코드들이 있는 폴더 입니다.

데이터의 가공이 이루어집니다. 필요한 컬럼은  [ 'Source', 'State', 'Year', 'Species', 'Latitude', 'Longitude', 'public_positional_accuracy']  입니다.

각 컬럼들이 제대로 기재되지 않은 경우, 임의로 수정이 필요할 것입니다.

예를들어 Year이 nan값이거나 이상한 숫자가 들어가 있는 경우에는 drop해줄 수 있을 것입니다.

전처리가 이루어진 뒤에는 데이터 프레임을 db에 저장하거나 csv파일을 저장해 두는것이 좋습니다.

또한 이 과정에서 감소율을 추정해 볼 종들(Target Species)과, 이 종들이 부재하고 있는 지역을 대표하는 종(Absence)을 선정하게 됩니다.





# 1~7.ipynb

#### 1_making_test.ipynb

머신러닝에 필요한 Test set을 생성합니다.

`Year_start` 부터 `Year_end`까지, 각 데이터 포인트들의 주변 종 분포를 조사하고, 이 결과를 담은 컬럼을 생성합니다. 

예를들어 `labiculata_2007_18km` 칼럼은 2007년에, 해당 데이터 포인트의 반경 18km 이내에 Anatis labiculata 종이 몇 개 있었는지를 기록합니다.

종명이 똑같고 속명으로 구분되는 종이 있을 수 있습니다. 이런 경우 직접 컬럼명을 지정해줘야할 수 있습니다.



#### 2_scaling.ipynb

Test set을  나눈 뒤에, minmax scaling을 진행합니다.

이후 각 종들의 이름이 붙은 테스트 파일이 만들어집니다.



#### 3_making_train.ipynb

Test set을 기반으로 Train set를 만듭니다. 

데이터 포인트가 기록되었던 연도를 기반으로, 그해에 기록된 종들의 컬럼만 남깁니다.

ex) Anatis labiculata_18: 해당년도를 기준으로, 데이터포인트의 반경 18km 이내에 labiculata 종이 몇개 있었는지가 기록됩니다.



#### 4_Model_dev.ipynb

회귀분석 결과 및 다중공선성을 고려해 모델이 사용할 변수들을 선정하고, 성능을 측정해봅니다.

이후 shap_values를 통해 높은 순서대로 변수를 압축한 뒤 다시 성능을 측정해봅니다.



#### 5_make_AOOcsv.ipynb

AOO를 추산하기 위한 csv파일들을 생성합니다.



#### 6_AOO_crawling.ipynb

AOO를 추산하고 연도별 결과를 저장한 CSV파일들을 생성합니다



#### 7_generalization.ipynb

ground truth라고 할만한 것이 없으므로, 모델에 대한 간접적인 검증을 위해서 진행해보는 과정입니다.

데이터 세트의 일부만을 학습시켜서 학습한적 없는 곳의 데이터를 테스트했을 때의 성능을 체크해봅니다.






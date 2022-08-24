# Package Method

## 1. util_method

```python
def latlontogps(frame):
    return frame
```

Combine the data in the `Latitude` and `Longitude` columns to create a `gps` column. (lat,lon)

`frame`: Data frame to be inserted as an argument of the function

`return`: Processed data frames

```python
def remove_sp(frame): 
    return frame
```

Remove species with no species name, data written in sp., total observations of 30 or less.

`frame`:  Data frame to be inserted as an argument of the function

`return`: Processed data frames

```python
def dropdup(frame): 
    return frame
```

Remove data with `public_positional_accuracy` larger than 1000 and data with `Latitude` and `Longitude` not properly recorded.

Leave only one duplicate data based `['Year','Species','Latitude','Longitude']`and remove the rest.

`frame`: Data frame to be inserted as an argument of the function

`return`: Processed data frames

```python
def select_key(num:int):
    return target_species,key
```

Function created to facilitate the use of `read_csv()`, `to_csv()`.

If you are going to use it, you will need to modify the code. 

You don't have to use it if you don't need it.

## 2. stat_method

```python
def custom_mulreg(olsarg:str,df,viewoption=False):
    return res, olsarg
```

multi-linear regression analysis.

`olsarg`: Variable of type string with species name separated by '+'

`df`:  Data frame to be inserted as an argument of the function

`viewoption`: if True. You can check res.summary().



`res`: Check the pvalues of each species

Return to confirm the results of multiple regression analysis. ex) res.pvalues, res.summary

`olsarg`: When multiple regression analysis is performed, the variables to be included in the next multiple regression analysis are returned.

```python
def custom_linreg(df,target_species,viewoption=False):
    return Species_list
```

simple linear regression analysis.

`df`: Data frame to be inserted as an argument of the function

`target_species`: species name to be dependent variable

`viewoption`: If TRUE, you can see the results of each species regression analysis.

```python
def custom_vif_varlist(df,varlist:list):
    return featurelist
```

Check multicollinearity to select variables.

`df`: Data frame to be inserted as an argument of the function

`varlist`: List of variables to check multicollinearity

`featurelist`: List of variables with multicollinearity less than or equal to 10

## 3. make_test

```python
def make_test(df_all,df_target,Year_Start:int, Year_end:int):
    return df_target
```

Create data frames for test

`df_all`: Data frame with all data points recorded (need preprocess)

`df_target`: Dataframe of the species to create the test set(In case of multiple species, recommend to do it at once.)

`year_start`: a argument that determines the year in which the investigation is to begin

`year_end`: a argument that determines the year in which the investigation is to be completed

`return`:  Data frame for test

## 4. make_train

```python
def make_train(df_all,df_target,target_species):
    return df_fin
```

Create data frames for train.

`df_all`: Data frame with all data points recorded (need preprocess)

`df_target`: Data frame for test the species to create data for train

`target_species`: Dataframe of the species to create the train set

`df_fin`: Data frame for train

## 5. ML_method

```python
def ML(df,targetnum,varlist,varlistname:str
       ,target_species,bagnum=50,repnum=50
       ,testsize=0.1,learningrate=0.7,viewoption=False,to_csv=False):
```

machine learning

`df`: Data frame for train

`targetnum`: Number of target species

`varlist`: List of variables to be used in the model

`varlistname`: to_csv(), to distinguish when naming. You can use any word.

`target_species`: Species name of target species

`bagnum`: Since there is more absence than present, only a part of absence is taken to match the ratio.

Arguments that specify how many times you want to pull another absence bag because there may be bias in the data

`repnum`:  Arguments that specify how many times machine learning will be repeated in a bag

`testsize`:  test size

`learningrate`: learningrate

`viewoption`: if True, allows you to view the results every machine learning

`to_csv`: if True, Saves the resulting values of machine learning as csv in the specified path

`return`: -

```python
def structgen(df_target,Sourcelist):
    return df_train, df_test,train_len,test_len
```

Create a new train, test set for comparison between citizen science data and structured data.

`df_target`: Dataframe to slice for generalization

`sourcelist`: Sources of citizen science data are entered in list format

`df_train`: Train data to input the model during generalization

`df_test`: Test data to input the model during generalization

`train_len`: Number of target species in train data

`test_len`:  Number of target species in test data

```python
def timegen(df_target,sliceYear,target_species,option=0):
    return df_train, df_test,train_len,test_len
```

Create a new train, test set for time-based comparison.

`df_target`: Dataframe to slice for generalization

`sliceYear`: The year on which slice is based

`target_species`: Species name of target species

`option`:

0 =>\# After training about 70 percent based on the past year, test the current 30 percent

1 = > After training about 70 percent based on the current year, test 30 percent of the past

`df_train`: Train data to input the model during generalization

`df_test`: Test data to input the model during generalization

`train_len`:  Number of target species in train data

`test_len`: Number of target species in test data

## 6. final_var_select

```python
def final_var_select(df,targetnum,varlist,target_species
                     ,bagnum=10,repnum=10,testsize=0.1,learningrate=0.7
                     ,returnsize=15,viewoption=False,to_csv=False):
```

`df`: Data frame for train

`targetnum`: Number of target species

`varlist`: List of variables to be used in the model

`target_species`: Species name of target species

`bagnum`: Since there is more absence than present, only a part of absence is taken to match the ratio.

Arguments that specify how many times you want to pull another absence bag because there may be bias in the data

`repnum`:  Arguments that specify how many times machine learning will be repeated in a bag

`testsize`: test size

`learningrate`:  learning rate

`returnsize`: The shap value is sorted in the order of the highest order, and the factor determines the number of places to return.

`viewoption`: if True, allows you to view the results every machine learning

`to_csv`: if True, Saves the resulting values of machine learning as csv in the specified path

`return`: Species are returned as list in order of high shap value

## 7. AOO

```python
 def AOO(df_train,df_test,targetnum,varlist
         ,target_species,Year_start,Year_end
         ,bagnum=50,repnum=50,learningrate=0.7,judge_indicator=0.5,to_csv):
```

It would be better to refer to the file 5_make_AOOcsv.ipynb.

`df_train`: train data of species trying to calculate aoo

`df_test`: test data of species trying to calculate aoo

`targetnum`: Number of species trying to calculate aoo

`varlist`: List of variables to be used in the model

`year_start `: Year to start the AOO investigation

`year_end `: Year to end the AOO investigation

`to_csv`: TRUE이면 결과 값들을 지정된 경로에 csv로 저장함

`bagnum`: Since there is more absence than present, only a part of absence is taken to match the ratio.

Arguments that specify how many times you want to pull another absence bag because there may be bias in the data

`repnum`:  Arguments that specify how many times machine learning will be repeated in a bag

`learningrate`:  learningrate

`judge_indicator`: Determine what percentage of the number multiplied by bag and rep should be considered to exist.

For example, if the value of this factor is 0.5 and we predict that there is more than half of it, we believe that there is a target species.

`to_csv`: if True, Saves the resulting values of machine learning as csv in the specified path

`return`: -

from tqdm import tqdm
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from collections import Counter

def AOO(df_train,df_test,targetnum,varlist,target_species,Year_start,Year_end,bagnum=50,repnum=50,learningrate=0.7,judge_indicator=0.5,to_csv=False):
    hot = list(range (0, bagnum))
    pot = list(range(0, repnum))
    Year_end += 1
    for i in range(Year_start,Year_end):
            globals()['potcast_{}'.format(i)] = []
            
            
    for k in tqdm(hot):
        BOX = df_train.reset_index(drop = True).copy()
        absence_pool = BOX[targetnum:].sample(n=targetnum, random_state = k)
        Ml_pool = pd.concat([BOX[:targetnum], absence_pool])
        answer = Ml_pool.target
        Ml_pool = Ml_pool[varlist]



        for i in pot:
            X_train, X_test, y_train, y_test = train_test_split(Ml_pool, answer, test_size=0.000000000001, random_state= i)  
            xgb_wrapper = XGBClassifier(n_estimators=1000, learning_rate=learningrate, max_depth=7, objective = "binary:logistic")
            evals = [(X_test, y_test)]
            xgb_wrapper.fit(X_train, y_train, early_stopping_rounds=10, 
                                eval_metric="error", eval_set=evals, verbose=0)

            
            for year in range(Year_start,Year_end):
                nameind={}
                
                # Alert!
                # test csv를 만들때 실패했던 종들은 따로 코딩해줘야함.
                # When making test csv file, the failed species should be coded separately.
                for name in varlist: 
                    if name =='Coelophora_maculata_18':
                        nameind['phoramaculata_'+str(year)+"_18km"] = name

                    elif name =='Epilachna_borealis_18':
                        nameind['achnaborealis_'+str(year)+"_18km"] = name

                    elif name =='Coleomegilla_maculata_18':
                        nameind['gillamaculata_'+str(year)+"_18km"] = name

                    elif name =='Psyllobora_borealis_18':
                        nameind['boraborealis_'+str(year)+"_18km"] = name

                    elif name =='Olla_vnigrum_18':
                        nameind['v-nigrum_'+str(year)+"_18km"] = name
                    else:
                        nameind[(name.split("_")[1]+"_"+str(year)+"_18km")] = name

                df09 = df_test[list(nameind.keys())].reset_index(drop=True)


                df09.columns = list(nameind.values())
                preds_proba = xgb_wrapper.predict_proba(df09)
                presence_index = [i for i in range(len(preds_proba)) if preds_proba[i][1]>0.5]

                
                globals()["potcast_{}".format(year)].extend(presence_index)

    judgebythis = len(hot)*len(pot)*judge_indicator
    

    for year in range(Year_start,Year_end):
        globals()['count{}'.format(year)] = Counter(globals()['potcast_{}'.format(year)])          
        globals()['idx_{}'.format(year)] = []
        for i in globals()['count{}'.format(year)].most_common(targetnum):
            if i[1]>=judgebythis:
                globals()['idx_{}'.format(year)].append(i[0])

    df_test['occurrenceRemarks'] = 'Note'
    df_test.rename(columns={"Latitude":"latitude",
                   "Longitude":"longitude"},inplace=True)

   

    for i in range(Year_start,Year_end):
        globals()['df_{}'.format(i)]=df_test.iloc[globals()['idx_{}'.format(i)]][['latitude','longitude','Species','occurrenceRemarks','Year']].rename({'Species':'scientificname'},axis=1).reset_index(drop=True)

    df_modi = df_test[['latitude','longitude','Species','occurrenceRemarks','Year']].rename({'Species':'scientificname'},axis=1)

    # 머신은 없다고 판단했으나, 실제로는 있는 경우와 합침 (aoo니까)
    # Even in areas where machine learning predictions indicate that there is no target species, there may be target species in the actual identification record. 
    # In order to estimate AOO, we need to fix this case.

    for i in range(Year_start,Year_end):
        globals()['df_fin{}'.format(i)] = pd.concat([globals()['df_{}'.format(i)],df_modi[df_modi.Year==i]]).drop_duplicates(keep='first').reset_index(drop=True)
        print(i,"",len(globals()['df_fin{}'.format(i)]))
    if to_csv == True:
        for i in range(Year_start,Year_end):
            globals()['df_fin{}'.format(i)].to_csv("./Data/3rd_manipulated_data/forAOO/"+target_species+"_aoo"+str(i)+".csv", index = None)
        
            
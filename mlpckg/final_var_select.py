import re
from tqdm import tqdm
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

import numpy as np
import shap
from mlpckg.ML_method import get_clf_eval
from mlpckg.ML_method import get_clf_eval_num


def final_var_select(df,targetnum,varlist,target_species,bagnum=10,repnum=10,testsize=0.1,learningrate=0.7,returnsize=15,viewoption=False,to_csv=False):
    hot = list(range (0, bagnum))
    pot = list(range(0, repnum))
            
    accuracys = 0
    precisions = 0
    recalls = 0
    f1s = 0
    roc_aucs = 0

    shap_all = pd.DataFrame(columns=['name','shap_index'])

    for k in tqdm(hot):
        BOX = df.copy().sort_values(by=['target'],ascending=False).reset_index(drop=True)
        absence_pool = BOX[targetnum:].sample(n=targetnum, random_state = k)
        Ml_pool = pd.concat([BOX[:targetnum], absence_pool])
        answer = Ml_pool.target
        Ml_pool = Ml_pool[varlist]

        for i in pot:
            
            X_train, X_test, y_train, y_test = train_test_split(Ml_pool, answer, test_size=testsize, random_state= i) # 정확도는 0.1일 때 가장 높음

            xgb_wrapper = XGBClassifier(n_estimators=1000, learning_rate=learningrate, max_depth=7, objective = "binary:logistic")
            evals = [(X_test, y_test)]
            xgb_wrapper.fit(X_train, y_train, early_stopping_rounds=10, 
                                eval_metric="error", eval_set=evals, verbose=0)
            ws100_preds = xgb_wrapper.predict(X_test)
            ws100_pred_proba = xgb_wrapper.predict_proba(X_test)[:, 1]
            

            # 예측 성능 평가
            a, b, c, d, e = get_clf_eval_num(y_test, ws100_preds, ws100_pred_proba)
            accuracys = accuracys + a
            precisions = precisions + b
            recalls = recalls + c
            f1s = f1s + d
            roc_aucs = roc_aucs + e

            if viewoption ==True:
                get_clf_eval(y_test, ws100_preds, ws100_pred_proba)
            
            
            shap.initjs()
            explainer = shap.TreeExplainer(xgb_wrapper)
            shap_values = explainer.shap_values(X_train)

            vals= np.abs(shap_values).mean(0)
            feature_importance = pd.DataFrame(list(zip(X_train.columns,vals)),columns=['col_name','feature_importance_vals'])
            feature_importance.sort_values(by=['feature_importance_vals'],ascending=False,inplace=True)
            
            shap_all = pd.concat([shap_all, feature_importance])
            
        

        accuracys = 0
        precisions = 0
        recalls = 0
        f1s = 0
        roc_aucs = 0
            


    shap_all = shap_all.reset_index(drop=True)
    df_fin = shap_all[['name', 'shap_index']][0:len(varlist)].copy()


    a=0
    for i in varlist:
        try:
            df_fin['name'][a] = i
            knife = shap_all[shap_all['col_name'] == i]['feature_importance_vals'].mean()
            df_fin['shap_index'][a] = knife
            a=a+1
        except:
            pass
        

    df_fin = df_fin.sort_values(by='shap_index', ascending=False)
    df_fin


    pav=df_fin[:returnsize]
    returnlist = df_fin[:returnsize].name.values
    if to_csv == True:
        pav.to_csv('./Data/3rd_manipulated_data/shap_values/'+str(target_species) + 'shap_values_top'+str(returnsize)+'.csv')
        df_fin.to_csv('./Data/3rd_manipulated_data/shap_values/'+str(target_species) + 'shap_values.csv')

    return returnlist
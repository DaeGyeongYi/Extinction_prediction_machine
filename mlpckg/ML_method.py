from tqdm import tqdm
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import brier_score_loss
from sklearn.metrics import cohen_kappa_score
from matplotlib import pyplot as plt

from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score, roc_auc_score

import numpy as np

def get_clf_eval(y_test, pred=None, pred_proba=None):
    confusion = confusion_matrix( y_test, pred)
    accuracy = accuracy_score(y_test , pred)
    precision = precision_score(y_test , pred)
    recall = recall_score(y_test , pred)
    f1 = f1_score(y_test,pred)
    # ROC-AUC
    roc_auc = roc_auc_score(y_test, pred_proba)
    print('오차 행렬')
    print(confusion)
    # ROC-AUC print
    print('정확도: {0:.4f}, 정밀도: {1:.4f}, 재현율: {2:.4f},\
    F1: {3:.4f}, AUC:{4:.4f}'.format(accuracy, precision, recall, f1, roc_auc))



def get_clf_eval_num(y_test, pred=None, pred_proba=None):
    confusion = confusion_matrix( y_test, pred)
    accuracy = accuracy_score(y_test , pred)
    precision = precision_score(y_test , pred)
    recall = recall_score(y_test , pred)
    f1 = f1_score(y_test,pred)
    # ROC-AUC 
    roc_auc = roc_auc_score(y_test, pred_proba)
    
    return accuracy, precision, recall, f1, roc_auc



def ML(df,targetnum,varlist,varlistname:str,target_species,bagnum=50,repnum=50,testsize=0.3,learningrate=0.01,viewoption=False,to_csv=False):


    hot = list(range (0, bagnum))
    pot = list(range(0, repnum))

    df_score_all = pd.DataFrame({"accuracy":[],"precision":[], "recall":[], "f1":[], "auc":[], "brier":[], "kappa":[]})
    df_score_block = pd.DataFrame({"accuracy":[],"precision":[], "recall":[], "f1":[], "auc":[], "brier":[], "kappa":[]})

    accuracys, precisions, recalls ,f1s, roc_aucs, brier_score, kappa_score = 0,0,0,0,0,0,0

    accuracy_all=[]
    precision_all=[]
    recall_all=[]
    f1score_all=[]
    auc_all=[]
    kappa_all=[]
    brier_all=[]

    accuracy_block=[]
    precision_block=[]
    recall_block=[]
    f1score_block=[]
    auc_block=[]
    kappa_block=[]
    brier_block=[]

    hist_Ep = []


    for k in tqdm(hot):
        BOX = df.copy().sort_values(by=['target'],ascending=False).reset_index(drop=True)
        absence_pool = BOX[targetnum:].sample(n=targetnum, random_state = k)
        Ml_pool = pd.concat([BOX[:targetnum], absence_pool])
        answer = Ml_pool.target

        Ml_pool = Ml_pool[varlist]
        
        
        for i in pot:
        
            X_train, X_test, y_train, y_test = train_test_split(Ml_pool, answer, test_size=testsize, random_state= i) 
            

            xgb_wrapper = XGBClassifier(n_estimators=1000, learning_rate=learningrate, max_depth=7, objective = "binary:logistic")
            evals = [(X_test, y_test)]
            xgb_wrapper.fit(X_train, y_train, early_stopping_rounds=10, 
                                eval_metric="error", eval_set=evals, verbose=0)
            ws100_preds = xgb_wrapper.predict(X_test)
            ws100_pred_proba = xgb_wrapper.predict_proba(X_test)[:, 1]

            
            a, b, c, d, e = get_clf_eval_num(y_test, ws100_preds, ws100_pred_proba)
            accuracys = accuracys + a
            precisions = precisions + b
            recalls = recalls + c
            f1s = f1s + d
            roc_aucs = roc_aucs + e

            f = brier_score_loss(y_test, ws100_pred_proba)
            g = cohen_kappa_score(ws100_preds, y_test)
            brier_score = brier_score + f
            kappa_score = kappa_score + g

            accuracy_all.append(a)
            precision_all.append(b)
            recall_all.append(c)
            f1score_all.append(d)
            auc_all.append(e)
            brier_all.append(f)
            kappa_all.append(g)

            if viewoption == True:
                get_clf_eval(y_test, ws100_preds, ws100_pred_proba)

            hist_Ep.append(a)

        accuracy_block.append(accuracys/len(pot))
        precision_block.append(precisions/len(pot))
        recall_block.append(recalls/len(pot))
        f1score_block.append(f1s/len(pot))
        auc_block.append(roc_aucs/len(pot))
        kappa_block.append(kappa_score/len(pot))
        brier_block.append(brier_score/len(pot))

        accuracys = 0
        precisions = 0
        recalls = 0
        f1s = 0
        roc_aucs = 0
        brier_score = 0
        kappa_score = 0

    num_bins = 20 # 
    plt.hist(hist_Ep, num_bins)
    plt.show()

    sum(hist_Ep)/len(hist_Ep)

    df_score_all['accuracy']=accuracy_all
    df_score_all['precision']=precision_all
    df_score_all['recall']=recall_all
    df_score_all['f1']=f1score_all
    df_score_all['auc']=auc_all
    df_score_all['brier']=brier_all
    df_score_all['kappa']=kappa_all

    df_score_block['accuracy']=accuracy_block
    df_score_block['precision']=precision_block
    df_score_block['recall']=recall_block
    df_score_block['f1']=f1score_block
    df_score_block['auc']=auc_block
    df_score_block['brier']=brier_block
    df_score_block['kappa']=kappa_block

    if to_csv==True:
        df_score_all.to_csv("./Data/3rd_manipulated_data/score_bag_output/"+str(target_species)+'_'+varlistname+"_scores_all_insect_only.csv")
        df_score_block.to_csv("./Data/3rd_manipulated_data/score_bag_output/"+str(target_species)+'_'+varlistname+"_scores_block_insect_only.csv")

    print(df_score_all.describe())





def structgen(df_target,Sourcelist):
    source =Sourcelist.copy()
    Sourceindex=[]
    for i in source:
        Sourceindex.extend(list(df_target[df_target.Source==i].index))
    
    df_train = df_target.iloc[Sourceindex].reset_index(drop=True)
    df_test = df_target.drop(Sourceindex)

    
    train_len = len(df_train[df_train.target==1])
    test_len = len(df_test[df_test.target==1])

    return df_train, df_test,train_len,test_len



def timegen(df_target,sliceYear,target_species,option=0):


    if option==0:
        # 현재 vs 과거
        years=pd.DataFrame(df_target[df_target.Species_18 == target_species].Year.value_counts())
        print("recommend this 0.70~0.80",years[years.Year.index < sliceYear].sum()/len(df_target[df_target.Species_18 == target_species].index))
        sliceindex = df_target[df_target.Year < sliceYear].index


        df_train = df_target.iloc[sliceindex].reset_index(drop=True)
        df_test = df_target.iloc[list(set(df_target.index)-set(df_target.iloc[sliceindex].index))].reset_index(drop=True)

        train_len = len(df_train[df_train.target==1])
        test_len = len(df_test[df_test.target==1])

        return df_train, df_test,train_len,test_len

    elif option == 1:
        #과거 vs 현재
        years=pd.DataFrame(df_target[df_target.Species_18 == target_species].Year.value_counts())

        print("recommend this 0.70~0.80",years[years.Year.index > sliceYear].sum()/len(df_target[df_target.Species_18 == target_species].index))
        
        pot = df_target[df_target.Year > sliceYear].index


        df_train = df_target.iloc[pot].reset_index(drop=True)
        df_test = df_target.iloc[list(set(df_target.index)-set(df_target.iloc[pot].index))].reset_index(drop=True)


        train_len = len(df_train[df_train.target==1])
        test_len = len(df_test[df_test.target==1])

        return df_train, df_test,train_len,test_len
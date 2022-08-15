from xmlrpc.client import boolean
from statsmodels.formula.api import ols
import pandas as pd
from scipy.stats import *
from statsmodels.stats.outliers_influence import variance_inflation_factor

def custom_mulreg(olsarg:str,df,viewoption=False):
    res = ols('target ~ ' + olsarg, data=df).fit()
    
    if viewoption == True:
        print(res.summary())

        green_moss = pd.DataFrame(res.pvalues)
        green_moss = green_moss[green_moss[0] < 0.05]
        green_moss.drop(['Intercept'], inplace=True)

        add_p1 = list(green_moss.index)

        olsarg = ' + '.join(add_p1)
        print(len(olsarg.split("+")))

        return res, olsarg
        
    green_moss = pd.DataFrame(res.pvalues)
    green_moss = green_moss[green_moss[0] < 0.05]
    green_moss.drop(['Intercept'], inplace=True)

    add_p1 = list(green_moss.index)

    olsarg = ' + '.join(add_p1)

    return res, olsarg




def custom_linreg(df,target_species,viewoption=False):
    c92 = df.copy()

    jazz = list(set(df.columns.to_list()) - set(['target','Species_18', str(target_species+str('_18'))]))

    Species_list = []
    for i in jazz:
        model = stats.linregress(c92[i], c92['target'])
        if viewoption ==True:
            print(i)
            print("\n model: ", model)
            print("기울기: ", model.slope)
            print("절편: ", model.intercept) 
            print("상관계수: ", model.rvalue) 
            print("p값: ", model.pvalue)
            print("표준오차: ", model.stderr)
            print()
            print()
        
        if model.pvalue < 0.05:
            Species_list.append(i)

    return Species_list



def custom_vif_varlist(df,varlist:list):
    varialist = varlist.copy()
    X = df[varialist]


    vif = pd.DataFrame()
    vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif["features"] = X.columns
    
    try:
        vif.loc[vif['VIF Factor'] < 10]
    except:
        pass

    for i in vif.index:
        if vif['VIF Factor'][i] > 10:
            vif.drop(index = i)
            
    featurelist = vif.features.tolist()

    return featurelist

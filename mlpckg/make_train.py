import pandas as pd
from tqdm import tqdm 
from mlpckg.util_method import *



def make_train(df_all,df_target,target_species):
    #All species name list
    name_list = list(df_all.Species.unique())
    for i in range(len(name_list)):
        name_list[i] = name_list[i]+"_18"
    
    #add columns [year, species, latitude, longitude, source]
    column_name = list(df_all.columns)+name_list
    
    #final dataframe for return
    df_fin = pd.DataFrame(columns = column_name )
    
    for j in tqdm(range(2007,2022)):
        col_index = [cols for cols in df_target.columns if str(j) in cols]
        col_index = list(df_all.columns) + col_index
        df_tmp = df_target[col_index]
        df_tmp = df_tmp[df_tmp.Year == j]
        

        # modify name for ML model
        for col in range(len(col_index)):
            for k in name_list:               
                if str(j) not in col_index[col]:
                    pass 


                # Alert!
                # test csv를 만들때 실패했던 종들은 따로 코딩해줘야함.
                # When making test csv file, the failed species should be coded separately.
                elif col_index[col] =='boraborealis_'+str(j)+'_18km':
                    col_index[col] = 'Psyllobora borealis_18'
                elif col_index[col] =='achnaborealis_'+str(j)+'_18km':
                     col_index[col] = 'Epilachna borealis_18'
                elif col_index[col]=='gillamaculata_'+str(j)+'_18km':
                    col_index[col] = 'Coleomegilla maculata_18'
                elif col_index[col] =='phoramaculata_'+str(j)+'_18km':
                    col_index[col] = 'Coelophora maculata_18'
                elif col_index[col].split("_")[0] in k:
                    col_index[col]=k
                    
        df_tmp.columns = col_index
        df_fin = pd.concat([df_fin,  df_tmp ])
        
        
    df_fin = df_fin.reset_index(drop=True)
    
    
    return df_fin
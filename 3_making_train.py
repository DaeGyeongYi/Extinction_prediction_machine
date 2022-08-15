import pandas as pd
from mlpckg.make_train import *
from mlpckg.util_method import *
df_all = pd.read_csv("./Data/1st_manipulated_data/_all_coccinellid.csv",index_col=0)
df_all = remove_sp(df_all)


it = ['Adalia bipunctata' , 'Coccinella novemnotata',
 'Coccinella transversoguttata' , 'Hippodamia parenthesis' ]

for name in it:
    df_target = pd.read_csv("./Data/2nd_manipulated_data/20220808_"+name.split()[1][:5]+"_test_minmax.csv")

    df_fin = make_train(df_all =df_all ,df_target=df_target)

    df_fin.to_csv("./20220808_"+name.split()[1][:5]+"_train_minmax.csv", index=False)
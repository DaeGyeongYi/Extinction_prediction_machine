# 실제 테스트 minmax 스케일 (종별로 나누어서)
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#test csv,including all species.
df=pd.read_csv("./Data/2nd_manipulated_data/20220807_final_test_all.csv")


#target species(presence) name.
it = ['Adalia bipunctata' , 'Coccinella novemnotata',
 'Coccinella transversoguttata' , 'Hippodamia parenthesis' ]


#make csv
for i in it:
    df_copy = df.copy()
    target_species=i
    df_copy = df_copy[(df_copy.Species==target_species)|(df_copy.Species=='Coccinella septempunctata')|(df_copy.Species=='Harmonia axyridis')].reset_index(drop=True)
    print(df_copy.Species.unique())
    scaler = MinMaxScaler()
    scaler.fit(df_copy.iloc[:,9:])


    df_tmp = pd.DataFrame(scaler.transform(df_copy.iloc[:,9:]), columns=df_copy.iloc[:,9:].columns, index=list(df_copy.index.values))

    df_fin = pd.concat([df_copy.iloc[:,:8],df_tmp],axis=1).reset_index(drop=True)


    df_fin.to_csv("20220808_"+target_species.split()[1][:5]+"_test_minmax.csv", index=False)
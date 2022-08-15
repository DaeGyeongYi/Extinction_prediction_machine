import pandas as pd
from mlpckg.make_test import *

df_all = pd.read_csv("./Data/1st_manipulated_data/_all_coccinellid.csv")
df_absence = pd.read_csv("./Data/1st_manipulated_data/absence_only.csv")
df_presence = pd.read_csv("./Data/1st_manipulated_data/presence_only.csv")

df_all = df_all[[ 'Source', 'State', 'Year', 'Species', 'Latitude',
       'Longitude', 'public_positional_accuracy']]

df_absence = df_absence[[ 'Source', 'State', 'Year', 'Species', 'Latitude',
       'Longitude', 'public_positional_accuracy']]

df_presence = df_presence[[ 'Source', 'State', 'Year', 'Species', 'Latitude',
       'Longitude', 'public_positional_accuracy']]

df_target = pd.concat([df_presence,df_absence]).reset_index(drop=True)



Year_start = 2007
Year_end = 2021


df_fin = make_test(df_all=df_all,df_target=df_target,Year_Start=Year_start,Year_end=Year_end)



df_fin.to_csv("./20220807_final_test_all.csv.csv", index=False)
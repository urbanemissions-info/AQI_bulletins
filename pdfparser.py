
# !pip install camelot-py
import os
import sys
import camelot
import pandas as pd
from time import time
init = time()
#f_path = sys.argv[1]
f_path = os.getcwd() +'/data/2023/AQI_Bulletin_20230815.pdf' # Example

tables = camelot.read_pdf(f_path, pages = "1-end")

df_list = []
# Uncomment following lines to process mid-2015 and onwards
for i in range(0,len(tables),2):
    df = tables[i].df
    df.columns = df.iloc[0].values
    df = df.iloc[1:]
    df_list.append(df)
###########################################################
# Uncomment following lines to process before mid-2015 
# for i in range(0,len(tables)):
#     if len(df.columns)==7:
#         df = df.drop(columns=[0,6]).iloc[1:]
#         df.columns = df.iloc[0].values
#         df = df.iloc[1:]
#         df = df[df['City'] != '']
#         df_list.append(df)
#     elif len(df.columns)==6:
#         df = df.drop(columns=[0,5]).iloc[1:]
#         df.columns = df.iloc[0].values
#         df = df.iloc[1:]
#         df = df[df['City'] != '']
#         df_list.append(df)
###########################################################
final_df = pd.concat(df_list)

# Capturing pollutants and saving residues to log to check for missed pollutants
def parse_pollutants(x):
#     print(x)
    x = x.replace(',','').replace('\n','')
    poll_pairs = [['OZONE',''],
                  ['PM','2.5'], ['PM','10'],
                  ['CO',''], ['NH','3'], ['NO','2'], ['SO','2'], 
                  ['O','3']]
    polls = []
    for f, s in poll_pairs:
        if f in x and s in x:
            polls.append(f+s)
            x = x.replace(f,'',1).replace(s,'',1)
    with open(f_path.replace('.pdf','.log'), 'a') as fl:
        fl.write(x)
    return ', '.join(sorted(polls))

final_df.columns = [i.replace('\n',' ').replace('  ',' ') for i in final_df.columns]
final_df = final_df.rename(columns={'Prominent Polluta nt':'Prominent Pollutant', 
                                    'Based on number of stations':'Based on number of monitoring stations'}) # Handling Naming issues
final_df['Prominent Pollutant'] = final_df['Prominent Pollutant'].apply(lambda x: parse_pollutants(x))

save_path = f_path.replace('.pdf', '.csv')
# print('Saving to', save_path)
final_df.to_csv(save_path, index=None)

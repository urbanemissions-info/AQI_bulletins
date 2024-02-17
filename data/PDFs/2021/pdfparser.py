
# !pip install camelot-py
import sys
import camelot
import pandas as pd
from time import time
init = time()
f_path = sys.argv[1]
# f_path = './AQI_Bulletin_20210107.pdf' # Example

tables = camelot.read_pdf(f_path, pages = "1-end")

df_list = []
for i in range(0,len(tables),2):
    df = tables[i].df
    df.columns = df.iloc[0].values
    df = df.iloc[1:]
    df_list.append(df)

final_df = pd.concat(df_list)

# Minor corrections
def parse_pollutants(x):
    lst = x.split(',')
    if len(lst)==1:
        return lst[0].replace('\n','').strip()
    else:
        prefix = [i.replace('\n','').strip() for i in lst[:-1]] + [lst[-1].split('\n')[0].strip()]
        suffix_raw = [i.strip() for i in lst[-1].split('\n')[1:]]
#         print(lst, prefix, suffix_raw)
        i = 0
        suffix = []
        for p in prefix:
            if p != 'CO':
                suffix.append(suffix_raw[i])
                i += 1
            else:
                suffix.append('')
        return ', '.join([i+j for i,j in zip(prefix, suffix)])
final_df['Prominent Pollutant'] = final_df['Prominent Pollutant'].apply(lambda x: parse_pollutants(x))
final_df.columns = [i.replace('\n',' ') for i in final_df.columns]

save_path = sys.argv[1].replace('.pdf', '.csv')
# print('Saving to', save_path)
final_df.to_csv(save_path, index=None)

import pandas as pd
import glob
import os
from datetime import datetime


csvs = glob.glob(os.getcwd() + "/data/CSVs/**/*.csv")

dfs = []

for csv in csvs:
    date = csv[-12:-4]
    # Convert the date string to datetime object
    date_obj = datetime.strptime(date, '%Y%m%d')
    # Format the datetime object as 'YYYY-MM-DD'
    formatted_date = date_obj.strftime('%Y-%m-%d')

    df = pd.read_csv(csv)
    df = df.rename(columns={'Based on Number of Monitoring Stations':'Based on number of monitoring stations'}) # Handling Naming issues

    df['date'] = formatted_date
    dfs.append(df)

master_df = pd.concat(dfs)

# CLEAN 'Based on number of monitoring stations' column
# Replace non-numeric characters in column 'Based on number of monitoring stations' with ''
master_df['Based on number of monitoring stations'] = master_df['Based on number of monitoring stations'].replace('#', '', regex=True)
master_df['Based on number of monitoring stations'] = master_df['Based on number of monitoring stations'].apply(lambda x: str(x).split(' ')[0] if 'station' in str(x).lower() else str(x))
master_df['Based on number of monitoring stations'] = master_df['Based on number of monitoring stations'].apply(lambda x: str(x).split(' ')[0] if 'data' in str(x).lower() else str(x))

master_df['No. Stations'] = master_df['Based on number of monitoring stations'].astype(str) + master_df['No. of Stations Participated/ Total Stations'].astype(str)
master_df['No. Stations'] = master_df['No. Stations'].replace('nan','', regex=True)
master_df['No. Stations'] = master_df['No. Stations'].apply(lambda x: str(x).split('/')[0])
master_df['No. Stations'] = master_df['No. Stations'].apply(lambda x: str(x).replace('+', ''))


master_df = master_df[['date', 'City','No. Stations', 'Air Quality', 'Index Value', 'Prominent Pollutant']]
master_df = master_df.sort_values(by='date')
master_df.to_csv(os.getcwd() + '/data/Processed/AllIndiaBulletins_Master_cleaned.csv', index=False)



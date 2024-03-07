import pandas as pd
import glob as glob
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv(os.getcwd() + '/data/Processed/AllIndiaBulletins_Master.csv')
df['date'] = pd.to_datetime(df['date'])

df['No. Stations'] = df['No. Stations'].apply(lambda x: str(x).replace('(', ' '))
df['No. Stations'] = df['No. Stations'].apply(lambda x: str(x).split(' ')[0])
df.replace('', np.nan, inplace=True)
df = df.dropna()
df['No. Stations'] = df['No. Stations'].astype(float)


# NUMBER OF CITIES WITH STATIONS
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

df['#stations/city'] = pd.cut(df['No. Stations'], [0, 1, 5, 10, 50], labels=['1s', '2-5s', '6-10s', '10s+'])

grouped_data = df.groupby(['year', 'month', '#stations/city'])['City'].nunique().reset_index()
grouped_data['date'] = grouped_data['year'].astype(str) + '-' + grouped_data['month'].astype(str)
grouped_data['date'] = pd.to_datetime(grouped_data['date'], format='%Y-%m')
grouped_data = grouped_data.pivot_table(index=['date'], columns='#stations/city', values='City').reset_index()
grouped_data['date'] = grouped_data['date'].dt.strftime('%Y%b')
grouped_data.plot(x='date',
                  kind='bar', stacked=True,
                  figsize=(15,10))
selected_ticks = [0] + list(range(12, grouped_data['date'].shape[0], 12))  # First, 13th, 26th, etc.
plt.xticks(selected_ticks, fontweight='bold', rotation=0, fontsize=15)
plt.yticks(fontweight='bold', fontsize=15)
plt.xlabel('Date', fontweight='bold', fontsize=20)
plt.ylabel('No. of Cities', fontweight='bold', fontsize=20)
plt.title('Number of Cities with Monitoring Stations', fontsize=25, fontweight='bold')
legend_properties = {'weight':'bold', 'size':15}
plt.legend(['1s', '2-5s', '6-10s', '10s+'], title = '#stations/city',
           prop=legend_properties, title_fontproperties=legend_properties)
#plt.gca().xaxis.set_major_locator(plt.MaxNLocator(9))  # Set maximum number of ticks
plt.tight_layout()

plt.savefig(os.getcwd() + '/plots/monitor_track/monitoredcities_stacked.png')

# plt.figure(figsize=(15, 10))
# plt.bar(grouped_data['date'].dt.strftime('%Y%b'), grouped_data['City'], color='blue')
# plt.xlabel('Month')
# plt.ylabel('Number of Cities')
# plt.title('Number of Cities with Monitoring Stations')
# plt.gca().xaxis.set_major_locator(plt.MaxNLocator(9))  # Set maximum number of ticks
# plt.tight_layout()
# plt.savefig(os.getcwd() + '/plots/monitor_track/monitoredcities.png')
# plt.close()


# NUMBER OF STATIONS
grouped_data = df.groupby(['date'])['No. Stations'].sum().reset_index()
grouped_data['date'] = pd.to_datetime(grouped_data['date'], format='%Y-%m')
grouped_data['month'] = grouped_data['date'].dt.month
grouped_data['year'] = grouped_data['date'].dt.year
grouped_data = grouped_data.groupby(['year', 'month'])['No. Stations'].max().reset_index()
grouped_data['date'] = grouped_data['year'].astype(str) + '-' + grouped_data['month'].astype(str)
grouped_data['date'] = pd.to_datetime(grouped_data['date'], format='%Y-%m')

plt.figure(figsize=(15, 10))
plt.bar(grouped_data['date'].dt.strftime('%Y%b'), grouped_data['No. Stations'], color='blue')
plt.title('Number of Stations', fontsize=25, fontweight='bold')
selected_ticks = [0] + list(range(12, grouped_data['date'].shape[0], 12))  # First, 13th, 26th, etc.
plt.xticks(selected_ticks, fontweight='bold',fontsize=15)
plt.yticks(fontweight='bold', fontsize=15)
plt.xlabel('Date', fontweight='bold', fontsize=20)
plt.ylabel('No. of Stations', fontweight='bold', fontsize=20)

plt.tight_layout()
plt.savefig(os.getcwd() + '/plots/monitor_track/stations.png')
plt.close()

exit()


csvs = glob.glob(os.getcwd() + "/data/CSVs/**/*.csv")
city = 'Delhi'

dfs = []

for csv in csvs:
    date = csv[-12:-4]
    # Convert the date string to datetime object
    date_obj = datetime.strptime(date, '%Y%m%d')
    # Format the datetime object as 'YYYY-MM-DD'
    formatted_date = date_obj.strftime('%Y-%m-%d')

    df = pd.read_csv(csv)
    df = df.rename(columns={'Based on Number of Monitoring Stations':'Based on number of monitoring stations'}) # Handling Naming issues

    
    df = df[df['City'] == city]
    df['date'] = formatted_date
    dfs.append(df)

master_df = pd.concat(dfs)
# Replace non-numeric characters in column 'Based on number of monitoring stations' with ''
master_df['Based on number of monitoring stations'] = master_df['Based on number of monitoring stations'].replace('#', '', regex=True)
master_df['Based on number of monitoring stations'] = master_df['Based on number of monitoring stations'].apply(lambda x: str(x).split(' ')[0] if 'station' in str(x).lower() else str(x))
master_df['Based on number of monitoring stations'] = master_df['Based on number of monitoring stations'].apply(lambda x: str(x).split(' ')[0] if 'data' in str(x).lower() else str(x))

master_df['No. Stations'] = master_df['Based on number of monitoring stations'].astype(str) + master_df['No. of Stations Participated/ Total Stations'].astype(str)
master_df['No. Stations'] = master_df['No. Stations'].replace('nan','', regex=True)
master_df['No. Stations'] = master_df['No. Stations'].apply(lambda x: str(x).split('/')[0])
master_df['No. Stations'] = master_df['No. Stations'].apply(lambda x: str(x).replace('+', ''))
#master_df['No. Stations'] = master_df['No. Stations'].apply(lambda x: int(x))

master_df = master_df[['date', 'No. Stations', 'Air Quality', 'Index Value', 'Prominent Pollutant']]


#
master_df = master_df.sort_values(by='date')

master_df.to_csv('check.csv')
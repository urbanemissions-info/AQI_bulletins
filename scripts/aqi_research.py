import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

df = pd.read_csv(os.getcwd() + '/data/Processed/AllIndiaBulletins_Master0.csv')
df['No. Stations'] = df['No. Stations'].apply(lambda x: str(x).replace('(', ' '))
df['No. Stations'] = df['No. Stations'].apply(lambda x: str(x).replace('!', ' '))
df['No. Stations'] = df['No. Stations'].apply(lambda x: str(x).split(' ')[0])
df.replace('', np.nan, inplace=True)
df = df.dropna()

df['date'] = pd.to_datetime(df['date'])
df['No. Stations'] = df['No. Stations'].astype(float)
df['year'] = df['date'].dt.year

# 1. total unique cities being monitored by year 
unique_cities_per_year = df.groupby('year')['City'].nunique()
unique_cities_per_year.to_csv(os.getcwd() + '/data/Results/unique_cities_per_year.csv')
unique_cities_per_year.plot(x='year',
                            kind='bar',
                            figsize=(15,10))

plt.xticks(fontweight='bold', rotation=0, fontsize=15)
plt.yticks(fontweight='bold', fontsize=15)
plt.xlabel('Year', fontweight='bold', fontsize=20)
plt.ylabel('No. of Cities', fontweight='bold', fontsize=20)
plt.title('Number of Cities with Monitoring Stations', fontsize=25, fontweight='bold')
plt.tight_layout()
plt.savefig(os.getcwd() + '/plots/Results/unique_cities_per_year.png')
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('check.csv')
df = df.dropna()
df['date'] = pd.to_datetime(df['date'])
df['No. Stations'] = df['No. Stations']
df['No. Stations'] = df['No. Stations'].astype(int)

df['Prominent Pollutant'] = df['Prominent Pollutant'].replace('OZONE', 'O3', regex=True)
# Extract month and year from the Date column
df['Month'] = df['date'].dt.month
df['Year'] = df['date'].dt.year

# Word to count occurrences
pollutants = ['PM2.5', 'PM10','O3', 'CO', 'NO2']

# Count occurrences of the pollutant in each month across all years
results = []
for pollutant in pollutants:
    result = df[df['Prominent Pollutant'].str.contains(pollutant)].groupby(['Year', 'Month'])['Prominent Pollutant'].apply(lambda x: x.str.count(pollutant)).reset_index(name='Count')
    result = result.groupby(['Year', 'Month'])['Count'].sum().reset_index()
    result['pollutant'] = pollutant
    results.append(result)

master = pd.concat(results)

master = master.pivot_table(index=['Year', 'Month'], columns='pollutant', values='Count', fill_value=0).reset_index()

master.to_csv('pollutants_monthly.csv', index=False)
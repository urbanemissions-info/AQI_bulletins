import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

df = pd.read_csv(os.getcwd() + '/data/Processed/AllIndiaBulletins_Master.csv')

df['date'] = pd.to_datetime(df['date'])

# Clean No. of Stations
df['No. Stations'] = df['No. Stations'].apply(lambda x: str(x).replace('(', ' '))
df['No. Stations'] = df['No. Stations'].apply(lambda x: str(x).split(' ')[0])
df.replace('', np.nan, inplace=True)
df = df.dropna()
df['No. Stations'] = df['No. Stations'].astype(float)

#
df['#stations/city'] = pd.cut(df['No. Stations'], [0, 1, 5, 10, 50], labels=['1s', '2-5s', '6-10s', '10s+'])

pivoted = df.pivot_table(index='#stations/city', columns='Air Quality', aggfunc='size')
pivoted = pivoted.div(pivoted.sum(axis=1), axis=0) * 100

pivoted = pivoted.reset_index()
# Set custom colors
aqi_colors = ['#00b050', '#669900', '#f2f542', '#f59042', '#ff0000', '#753b3b']

pivoted.to_csv(os.getcwd() + '/data/Processed/aqi_frequency_city.csv')
pivoted.plot(x='#stations/city',
             kind='bar', stacked=True,
             color=aqi_colors,
             figsize=(10,7))

plt.xlabel('#stations/city', fontweight='bold', fontsize=15)
plt.ylabel('Percentage of AQI records', fontweight='bold', fontsize=15)

plt.xticks(fontweight='bold',fontsize=12)
plt.yticks(fontweight='bold', fontsize=12)

plt.title('Frequency of AQI across cities of different monitoring capacities', fontsize=20, fontweight='bold')
legend_properties = {'weight':'bold', 'size':12}
plt.legend(['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe'], title = 'AQI',
           prop=legend_properties, title_fontproperties=legend_properties)
#plt.gca().xaxis.set_major_locator(plt.MaxNLocator(9))  # Set maximum number of ticks
plt.tight_layout()

plt.savefig(os.getcwd() + '/plots/aqi_frequency_city.png')
plt.close()
#HISTOGRAAMS
for year in range(2015,2024):
    for month in range(1,13):
        df_month = df[(df['date'].dt.year == year) & (df['date'].dt.month == month)]

        # Plotting the histogram
        plt.figure(figsize=(10,7))
        plt.hist(df_month['Index Value'], edgecolor='black', density=True)  # Adjust the number of bins as needed
        plt.xlim(0,500)
        plt.ylim(0,0.013)
        plt.title('Histogram of AQI values', fontweight='bold', fontsize=20)
        plt.xlabel('Value', fontweight='bold', fontsize=15)
        plt.ylabel('Frequency', fontweight='bold', fontsize=15)
        

        plt.xticks(fontweight='bold',fontsize=12)
        plt.yticks(fontweight='bold', fontsize=12)

            # Add year - month annotation
        bbox_props = dict(boxstyle="square,pad=0.3", fc="white", ec="black", lw=1)
        plt.text(450, 0.012,
             '{}-{}'.format(year, month),
             fontsize=20, fontweight='bold', color='black',
             ha='center', va='center',
             bbox=bbox_props)



        # Show plot
        plt.savefig(os.getcwd() + '/plots/histograms/histogram_{}_{}.png'.format(year, month))
        plt.close()

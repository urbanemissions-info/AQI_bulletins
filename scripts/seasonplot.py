import pandas as pd
import matplotlib.pyplot as plt
import os 

df_pivot = pd.read_csv('data/samplepm25.csv')
#df_pivot.columns = df_pivot.head(1)
#df_pivot = df_pivot.iloc[1:,:]
df_pivot = df_pivot.set_index('pm25')
df_pivot = df_pivot.T
df_pivot =df_pivot*100
print(df_pivot)

df_pivot.plot(figsize=(16, 8),
        #color=[color_dict.get(x) for x in df_pivot.columns],
        linewidth = 3)

plt.xticks(fontweight='bold', rotation=0, fontsize=15)
plt.yticks(fontweight='bold', fontsize=15)
plt.xlabel('Month', fontweight='bold', fontsize=20)
plt.ylabel('Occurence rate (%)', fontweight='bold', fontsize=20)
plt.title('PM2.5 Occurence rate by Month', fontsize=25, fontweight='bold')
plt.tight_layout()
# Remove legend box
plt.legend()
plt.savefig(os.getcwd() + '/plots/pm25_occurencerate.png')
plt.close()

exit()

color_dict = {
              2019: '#808080',
              2020: '#ff0000',
              2021: '#4ea72e',
              2022: '#4e95d9',
              2023: '#215f9a',
              2024: '#3B3F44'
              }

df_pivot.plot(figsize=(16, 8),
        color=[color_dict.get(x) for x in df_pivot.columns],
        linewidth = 3)

plt.title('Mean TROPOMI Columnar Density of {} for {}'.format(pollutant, airshed_on_plot), fontsize=20)
plt.xlabel('Date', fontsize=15)
plt.ylabel('Unit: molecules/${m^2}$ * ${10^{20}}$', fontsize=17)
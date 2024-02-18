import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('pollutants_monthly.csv')
# Group by Year and Month and sum the pollutant concentrations
grouped_df = df.groupby(['Year', 'Month']).sum().reset_index()

# Create a stacked bar plot for each month
months = grouped_df['Month'].unique()
num_months = len(months)

fig, axs = plt.subplots(num_months, 1, figsize=(10, 5 * num_months))

for i, month in enumerate(months):
    month_data = grouped_df[grouped_df['Month'] == month]
    axs[i].bar(month_data['Year'], month_data['CO'], label='CO', color='blue')
    axs[i].bar(month_data['Year'], month_data['PM2.5'], bottom=month_data['CO'], label='PM25', color='green')
    axs[i].bar(month_data['Year'], month_data['PM10'], bottom=month_data['CO'] + month_data['PM2.5'], label='PM10', color='red')
    axs[i].bar(month_data['Year'], month_data['O3'], bottom=month_data['CO'] + month_data['PM2.5'] + month_data['PM10'], label='PM10', color='red')
    axs[i].bar(month_data['Year'], month_data['NO2'], bottom=month_data['CO'] + month_data['PM2.5'] + month_data['PM10'] + month_data['O3'], label='PM10', color='red')
    axs[i].set_title(f'Month {month}')
    axs[i].set_ylabel('Concentration')
    axs[i].legend()

plt.xlabel('Year')
plt.tight_layout()
plt.show()


fig, ax = plt.subplots(figsize=(10, 6))

# Create bottom variable for stacking
bottom = None

for month in months:
    month_data = grouped_df[grouped_df['Month'] == month]
    ax.bar(month_data['Year'], month_data['CO'], bottom=bottom, label='CO')
    axs.bar(month_data['Year'], month_data['PM2.5'], bottom=month_data['CO'], label='PM25')
    axs.bar(month_data['Year'], month_data['PM10'], bottom=month_data['CO'] + month_data['PM2.5'], label='PM10')
    axs.bar(month_data['Year'], month_data['O3'], bottom=month_data['CO'] + month_data['PM2.5'] + month_data['PM10'], label='PM10')
    axs.bar(month_data['Year'], month_data['NO2'], bottom=month_data['CO'] + month_data['PM2.5'] + month_data['PM10'] + month_data['O3'], label='PM10')
    
    
    if bottom is None:
        bottom = [0] * len(month_data)
    bottom = [bottom[i] + month_data.iloc[i, 2:].sum() for i in range(len(month_data))]

ax.set_xticks(grouped_df['Year'].unique())
ax.set_xticklabels(grouped_df['Year'].unique())
ax.set_ylabel('Concentration')
ax.set_title('Monthly Pollutant Concentrations')
ax.legend()
plt.tight_layout()
plt.show()
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('check.csv')
df = df.dropna()
df['date'] = pd.to_datetime(df['date'])
df['No. Stations'] = df['No. Stations']
df['No. Stations'] = df['No. Stations'].astype(int)

# Create a figure and axis objects
fig, ax1 = plt.subplots()

# Plot Num_Stations as a bar plot
ax1.bar(df['date'], df['Index Value'], color='red', label='No. Stations')
ax1.set_xlabel('date')
ax1.set_ylabel('AQI', color='red')
ax1.tick_params('y', colors='red')

# Create a twin axis for AQI
ax2 = ax1.twinx()
ax2.plot(df['date'], df['No. Stations'], color='blue', marker='o', label='AQI')
ax2.set_ylabel('No. Stations', color='blue')
ax2.tick_params('y', colors='blue')

# Set title and legend
plt.title('No. Stations and AQI Over Time - Delhi')
fig.legend(loc='upper left')

# Rotate x-axis labels for better readability (optional)
plt.xticks(rotation=45)

plt.show()
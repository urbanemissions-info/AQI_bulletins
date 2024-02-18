import numpy as np
import july
from july.utils import date_range

import pandas as pd
import matplotlib.pyplot as plt
import calplot
from matplotlib.colors import ListedColormap, BoundaryNorm

import os
import sys

dates = date_range("2020-01-01", "2020-12-31")
data = np.random.randint(0, 14, len(dates))


july.heatmap(dates, data, title='Github Activity', cmap="github")
plt.show()

exit()

df = pd.read_csv(os.getcwd() + '/data/Processed/AllIndiaBulletins_Master.csv')
df = df[df['City']=='Delhi']

df['date'] = pd.to_datetime(df['date'])
df = df[df.date.dt.year == 2020]
df.set_index('date', inplace=True)

# Define the colormap ranges and colors
aqi_ranges = [0, 50, 100, 200, 300, 400, 500]
aqi_colors = ['#00b050', '#669900', '#f2f542', '#f59042', '#ff0000', '#c00000']

# Create a custom discrete colormap for AQI
cmap = ListedColormap(aqi_colors)
norm = BoundaryNorm(aqi_ranges, cmap.N, clip=True)

july.heatmap(df.index, df['Index Value'], title='AQI', cmap="github")

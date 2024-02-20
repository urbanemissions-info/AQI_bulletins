import pandas as pd
import matplotlib.pyplot as plt
import calplot
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.cm import ScalarMappable
import os
import sys
import numpy as np
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

if len(sys.argv) !=2:
    print("Usage: scripts/cal_heatmaps.py city_name")
    sys.exit(0)

city = sys.argv[1]
from PIL import Image

def join_images_vertically(image1_path, image2_path, output_path):
    # Open images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    
    # Determine the width and height of the output image
    width = max(image1.width, image2.width)
    height = image1.height + image2.height
    
    # Create a new blank image with the calculated dimensions
    new_image = Image.new("RGB", (width, height))
    
    # Paste the first image at the top
    new_image.paste(image1, (0, 0))
    
    # Paste the second image below the first one
    new_image.paste(image2, (0, image1.height))
    
    # Save the result
    new_image.save(output_path)

df = pd.read_csv(os.getcwd() + '/data/Processed/AllIndiaBulletins_Master.csv')
df = df[df['City']==city]

print(df.head())
df['date'] = pd.to_datetime(df['date'])

##
df['No. Stations'] = df['No. Stations'].apply(lambda x: str(x).replace('(', ' '))
df['No. Stations'] = df['No. Stations'].apply(lambda x: str(x).split(' ')[0])
df.replace('', np.nan, inplace=True)
df = df.dropna()

df['No. Stations'] = df['No. Stations'].astype(float)

result = df.groupby(df.date.dt.year)['No. Stations'].mean().reset_index()
num_years = result.date.nunique()
#print(result)
#df = df[df.date.dt.year == 2020]
df.set_index('date', inplace=True)

## CALENDAR HEATMAP
# Define the colormap ranges and colors
aqi_ranges = [0, 50, 100, 200, 300, 400, 500]
aqi_colors = ['#00b050', '#669900', '#f2f542', '#f59042', '#ff0000', '#753b3b']

# Create a custom discrete colormap for AQI
cmap = ListedColormap(aqi_colors)
norsm = BoundaryNorm(aqi_ranges, cmap.N, clip=True)

# Define the conditions for each category
conditions = [
    (df['Index Value'] <= 50),
    (df['Index Value'] > 50) & (df['Index Value'] <= 100),
    (df['Index Value'] > 100) & (df['Index Value'] <= 200),
    (df['Index Value'] > 200) & (df['Index Value'] <= 300),
    (df['Index Value'] > 300) & (df['Index Value'] <= 400),
    (df['Index Value'] > 400)
]

categories = [1, 2, 3, 4, 5, 6]
df['AQI'] = np.select(conditions, categories, default='outlier')
df['AQI'] = df['AQI'].astype(int)

calplot.calplot(df['AQI'],
                yearascending = True,
                colorbar = False,

                yearlabels = True,
                yearlabel_kws = {'fontsize': 30, 'color': 'black', 'fontname':'sans-serif'},

                suptitle = city,
                suptitle_kws = {'fontsize': 40, 'x': 0.5, 'y': 0.995, 'fontweight':'bold', 'fontname':'sans-serif'},
                
                cmap=cmap,

                linecolor = 'white', linewidth = 1,
                edgecolor = 'black',

                #textformat = '{:.0f}', textfiller = '-', textcolor = 'black'

                figsize=(20,num_years*3.67)
                )
# Iterate over each subplot and set xtick labels to bold
for ax in plt.gcf().get_axes():
    fontsize = 28
    fontweight = 'bold'
    fontproperties = {'weight' : fontweight, 'size' : fontsize}
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontdict = fontproperties)
    #ax.tick_params(axis="x", labelsize=28, weight='bold')
#plt.xticks(fontweight='bold', fontsize=28)

plt.savefig(os.getcwd() + '/plots/{}_calendarhm.png'.format(city))
plt.close()


plt.figure(figsize=(20,7))  
plt.bar(result.date, result['No. Stations'], )
plt.title('Number of stations per day', fontsize=25, fontweight='bold')
plt.xticks(result.date, fontweight='bold', fontsize=20)
plt.yticks(fontweight='bold', fontsize=20)

plt.xlabel('Year', fontsize=20)
plt.savefig(os.getcwd() + '/plots/{}_stations.png'.format(city))



# Example usage:
join_images_vertically(os.getcwd() + '/plots/{}_calendarhm.png'.format(city),
                       os.getcwd() + '/plots/{}_stations.png'.format(city),
                       os.getcwd() + "/plots/final/{}_calendarhm_stations.png".format(city))
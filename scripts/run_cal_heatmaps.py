import pandas as pd
import os
import subprocess
from tqdm import tqdm 
import glob
cities = pd.read_csv(os.getcwd() + '/data/Processed/CityCounts.csv')['City']

done = glob.glob(os.getcwd() + "/plots/final/*.png")
done_cities = []
for f in done:
    city_done = f.split('/')[-1].split('_')[0]
    done_cities.append(city_done)

cities = [city for city in cities if city not in done_cities]

print(cities)

for city in tqdm(cities[1:]):
    print(city)
    print('*** ------------------------------------------- ***')
    command = ["python", "scripts/cal_heatmaps.py", city]
    subprocess.run(command)
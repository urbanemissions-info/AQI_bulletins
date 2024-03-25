# AQI_bulletins

## Codes
1. `pdfparser.py`: Extracted tables from all AQI bulletins from 2015.
2. `clean.py`: Cleans all CSVs extracted and creates `AllIndiaBulletins_Master.csv`. Then manually cleaned `City` column for duplicates. (Chihuahua problem)
3. `cal_heatmaps.py`: Creates calendar heatmaps for each city. 

## Research Questions
1. total unique cities by year 
2. total unique cities by month

3. total number of monitoring stations by year
4. total number of monitoring stations by month
5. Average number of monitoring stations per city by year (I am assuming this is the same as point 3/ point 1)
6. Average number of monitoring stations per city by month (I am assuming this is the same as point 4/point 2)
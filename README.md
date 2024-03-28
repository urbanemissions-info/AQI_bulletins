# Daily AQI Bulletins

This repository contains analysis of AQI Daily bulletins released by the Central Pollution Control Board (CPCB) since 2015. These daily bulletins can be currently obtained here: [CPCB Daily AQI Bulletins](https://cpcb.nic.in/AQI_Bulletin.php)

The data contains (available) day-wise `city-average AQI value`, `AQI category`, and `conditional pollutant` information. This data for all cities can be obtained in the  `AllIndiaBulletins_master.csv` from `data/Processed` folder.

Calendar plot of the AQI values is produced for each city, along with the average number of stations reporting AQI value in each year.

City wise AQI bulletins CSV and calendar plots can be obtained on UrbanEmissions website: [Link](https://urbanemissions.info/india-air-quality/india-ncap-aqi-indian-cities-2015-2023/)

## Codes
1. `pdfparser.py`: Extracted tables from all AQI bulletins from 2015.
2. `clean.py`: Cleans all CSVs extracted and creates `AllIndiaBulletins_Master.csv`. Then manually cleaned `City` column for duplicates. (Chihuahua problem)
3. `cal_heatmaps.py`: Creates calendar heatmaps for each city. 
4. `aqi_research.py`: Creates CSVs and plots that answers a few research questions as follows:

    1. total unique cities by year 
    2. total unique cities by month
    3. total number of monitoring stations by year
    4. total number of monitoring stations by month
    5. Average number of monitoring stations per city by year 
    6. Average number of monitoring stations per city by month

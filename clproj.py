# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 11:00:42 2021

@author: clare
"""

# import pandas, numpy and matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Import Valencia weather data
val_data = pd.read_csv(r"C:\Users\clare\OneDrive\Documents\Clare\Cert in Introductory Data analytics\Weather data\Val_data.csv", skiprows=24)
print(val_data.info())

#change data from " " to nan
val_data = val_data.replace(r'\s+', np.nan, regex=True).replace(' ', np.nan)
print(val_data.info())

count_missing = val_data.isnull().sum()
print(count_missing[0:26])

val_data = val_data.fillna(0)
check_val_data = val_data.isnull().sum()
print(check_val_data[0:26])
print(val_data.info())

#convert rain from object to float
val_data["rain"] = pd.to_numeric(val_data["rain"], downcast="float")
print(val_data.info())

dub_data = pd.read_csv(r"C:\Users\clare\OneDrive\Documents\Clare\Cert in Introductory Data analytics\Weather data\Dub_airport_weather_data_July.csv", skiprows=25)
print(dub_data.info())

#merge files
weather_data = dub_data.merge(val_data, 
                              how="outer", 
                              on="date", 
                              suffixes=("_dub", "_val"))
print(weather_data.info())

print(weather_data[["rain_dub", "rain_val"]].head())

#Create subset of weather data just showing rainfall data
rain_data = weather_data[["date", "rain_dub", "rain_val"]]
print(rain_data.head())

print(rain_data.describe())

#correct date formate attempt 2
dates = pd.to_datetime(rain_data.date, format="%d-%b-%Y")
print(dates)

#assign new date format to date column and set it as the index
rain_data = (rain_data.assign(date=dates).set_index("date"))
print(rain_data)

#Group data by year
annual_rain_data = rain_data.groupby(pd.Grouper(freq='A')).sum()
print(annual_rain_data.head())

#Add a 20 year moving average field for Valencia and Dublin
annual_rain_data['SMA_20_Dub'] = annual_rain_data["rain_dub"].expanding(min_periods=20).mean()
annual_rain_data['SMA_20_Val'] = annual_rain_data["rain_val"].expanding(min_periods=20).mean()
print(annual_rain_data.head(21))
    









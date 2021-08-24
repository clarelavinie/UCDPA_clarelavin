# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 15:00:50 2021

@author: clare
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

val_data_temp = pd.read_csv(r"C:\Users\clare\OneDrive\Documents\Clare\Cert in Introductory Data analytics\Weather data\Dub_airport_weather_data_July.csv", skiprows=25)
print(val_data_temp.head())

#try to change date format
val_data_temp["date"] = pd.to_datetime(val_data_temp["date"])
print(val_data_temp.head())
print(val_data_temp.info())

val_data_temp["date"] - pd.offsets.DateOffset(years=100)
val_data_temp["date"] -= pd.offsets.DateOffset(years=100)
print(val_data_temp.head())

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

rain_data = weather_data[["date", "rain_dub", "rain_val"]]
print(rain_data.head())

print(rain_data.describe())

#correct date format
#import datetime
#rain_data["date"] = pd.to_datetime(rain_data["date"])#
#print(rain_data.head())#
#print(rain_data.min())#
#print(rain_data.max())#

#Correct years from 1942 to 1970
#removed code as doesn't work

#create cumulative rainfall for Valencia and Dublin Airport
#correct date formate attempt 2
dates = pd.to_datetime(rain_data.date, format="%d-%b-%Y")
print(dates)

#assign new date format to date column and set it as the index
rain_data = (rain_data.assign(date=dates).set_index("date"))
print(rain_data)

#Going to split the data to compare in 25 year periods
rain_data_25_one = rain_data.loc['1946-01-01':'1970-12-31']
print(rain_data_25_one.describe())

#25 years from 1971 to 1995
rain_data_25_two = rain_data.loc['1971-01-01':'1995-12-31']
print(rain_data_25_two.describe())

#25 years from 1996 to 2020
rain_data_25_three = rain_data.loc['1996-01-01':'2020-12-31']
print(rain_data_25_three.describe())

#add a column to see if a day had any rainfall in Dublin Airport
result = []
for value in rain_data["rain_dub"]:
    if value > 0.0:
        result.append(1)
    else:
        result.append(0)
       
rain_data["raindays_dub"] = result   
print(rain_data)


#add a column to see if a day had any rainfall in Valencia
result = []
for value in rain_data["rain_val"]:
    if value > 0.0:
        result.append(1)
    else:
        result.append(0)
        
rain_data["raindays_val"] = result
print(rain_data)

rain_data.sum(axis=0)



# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 15:00:50 2021

@author: clare
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Import data for Valencia
val_data_temp = pd.read_csv(r"C:\Users\clare\OneDrive\Documents\Clare\Cert in Introductory Data analytics\Weather data\Dub_airport_weather_data_July.csv", skiprows=25)
print(val_data_temp.head())

#try to change date format
val_data_temp["date"] = pd.to_datetime(val_data_temp["date"])
print(val_data_temp.head())
print(val_data_temp.info())

val_data_temp["date"] - pd.offsets.DateOffset(years=100)
val_data_temp["date"] -= pd.offsets.DateOffset(years=100)
print(val_data_temp.head())

#Import weather data for Valencia
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
dates = pd.to_datetime(rain_data.date, infer_datetime_format=True)
print(dates)

#assign new date format to date column and set it as the index
rain_data = (rain_data.assign(date=dates).set_index("date"))
print(rain_data)


#add a column to indicate if rain day in Dublin Airport
result = []
for value in rain_data["rain_dub"]:
    if value > 0.2:
        result.append(1)
    else:
        result.append(0)
       
rain_data["raindays_dub"] = result   
print(rain_data)


#add a column to indicate if rain day in Valencia
result = []
for value in rain_data["rain_val"]:
    if value > 0.2:
        result.append(1)
    else:
        result.append(0)
        
rain_data["raindays_val"] = result
print(rain_data)

rain_data.sum(axis=0)

#add a column to indicate if heavy rain day in Valencia
result = []
for value in rain_data["rain_val"]:
    if value > 10.0:
        result.append(1)
    else:
        result.append(0)
        
rain_data["heavyraindays_val"] = result
print(rain_data)
    
#add a column to indicate if heavy rain day in Dublin Airport
result = []
for value in rain_data["rain_dub"]:
    if value > 10.0:
        result.append(1)
    else:
        result.append(0)
       
rain_data["heavyraindays_dub"] = result   
print(rain_data)

rain_data.sum(axis=0)

#create a month and year column
rain_data["month"] = rain_data.index.month
rain_data["year"] = rain_data.index.year
print(rain_data.head())

#Group data by year
annual_rain_data = rain_data.groupby("year").sum()
annual_rain_data = annual_rain_data.iloc[:-1,:]
print(annual_rain_data.head())
print(annual_rain_data.info())

#Add a 20 year moving average field for Valencia and Dublin
annual_rain_data['MA_20_Dub'] = annual_rain_data["rain_dub"].expanding(min_periods=20).mean()
annual_rain_data['MA_20_Val'] = annual_rain_data["rain_val"].expanding(min_periods=20).mean()
print(annual_rain_data.head(21))


#plot the yearly rainfall amounts
timeline = annual_rain_data()
fig, ax = plt.subplots()
ax.plot(timeline.index, timeline["rain_dub"], label='Dub')
ax.plot(timeline.index, timeline["rain_val"], label='Val')
ax.plot(timeline.index, timeline["MA_20_Val"], label='20yr MA Val', linestyle='dashed')
ax.plot(timeline.index, timeline["MA_20_Dub"], label='20yr MA Dub', linestyle='dashed')
ax.set_xlabel('Year')
ax.set_ylabel('Annual Rainfall (mm)')
ax.set_title("Annual Rainfall, 1942 to 2020: Valencia and Dublin stations")
plt.legend()
plt.show()

#Group rainfall days by year
fig, ax = plt.subplots()
ax.plot(annual_rain_data.index, annual_rain_data["rain_dub"], label='Dub')
ax.plot(annual_rain_data.index, annual_rain_data["rain_val"], label='Val')
ax.plot(annual_rain_data.index, annual_rain_data["MA_20_Val"], label='20yr MA Val', linestyle='dashed')
ax.plot(annual_rain_data.index, annual_rain_data["MA_20_Dub"], label='20yr MA Dub', linestyle='dashed')
ax.set_xlabel('Year')
ax.set_ylabel('Annual Rainfall (mm)')
ax.set_title('Annual Rainfall, 1942 to 2020: Valencia and Dublin stations')
plt.legend()
plt.show()

#compare heavy rain days to rain days
fig, ax = plt.subplots()
ax.plot(annual_rain_data.index, annual_rain_data["heavyraindays_dub"], label='Heavy raindays Dub')
ax.plot(annual_rain_data.index, annual_rain_data["heavyraindays_val"], label='Heavy raindays Val')
ax.plot(annual_rain_data.index, annual_rain_data["raindays_dub"], label='Total raindays Dub')
ax.plot(annual_rain_data.index, annual_rain_data["raindays_val"], label='Total raindays Val')
ax.set_xlabel('Year')
ax.set_ylabel('Raindays')
ax.set_title('Rainfall Days and Heavy Rainfall Days, 1942 - 2020')
plt.legend()
plt.show()

#group data by season
rain_data["month"] = rain_data.index.month
print(rain_data.head())



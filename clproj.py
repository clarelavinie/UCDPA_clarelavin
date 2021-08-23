# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 11:00:42 2021

@author: clare
"""

# import pandas, numpy and matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#import Valentia weather data file val_data.csv, ignoring the first 24 rows
val_data = pd.read_csv(r"C:\Users\clare\OneDrive\Documents\Clare\Cert in Introductory Data analytics\Weather data\Val_data.csv", skiprows=24)
print(val_data.head())

#View column names and data types of each
print(val_data.info())

#checking the number of rows and columns
print(val_data.shape)

#check for blank cells in rain column
check_for_NaN = val_data["rain"].isnull().values.any()
print(check_for_NaN)

#change data from " " to nan
val_data = val_data.replace(r'\s+', np.nan, regex=True).replace(' ', np.nan)

#check for NaN again
check_for_NaN = val_data["rain"].isnull().values.any()
print(check_for_NaN)

count_missing = val_data.isnull().sum()
print(count_missing[0:26])

val_data = val_data.fillna(0)
check_val_data = val_data.isnull().sum()
print(check_val_data[0:26])
print(val_data.info())

#convert rain from object to float
val_data["rain"] = pd.to_numeric(val_data["rain"], downcast="float")
print(val_data.info())

#import Dublin airport weather file Dub_airport_weather_data_July.csv to create dub_data
dub_data = pd.read_csv(r"C:\Users\clare\OneDrive\Documents\Clare\Cert in Introductory Data analytics\Weather data\Dub_airport_weather_data_July.csv", skiprows=25)
print(dub_data.head())

#view column names and data types of each
print(dub_data.info())

#checking the nubers of rows and columns
print(dub_data.shape)

#check for blank cells in rain column
check_Dub_for_Nan = dub_data["rain"].isnull().values.any()
print(check_Dub_for_Nan)

#merge files
weather_data = dub_data.merge(val_data, 
                              how="outer", 
                              on="date", 
                              suffixes=("_dub", "_val"))
# print first few lines of weather_data
print(weather_data.head())

# print shape of weather_data
print(weather_data.shape)

#print info on dataframe
print(weather_data.info())

# create a file with only rainfall data
rain_data = weather_data[["date", "rain_dub", "rain_val"]]
print(rain_data.head())

#describe file data
print(rain_data.describe())

print(rain_data.info())

#correct date format
dates = pd.to_datetime(rain_data.date)
print(dates)

rain_data = (rain_data.assign(date=dates).set_index("date"))












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

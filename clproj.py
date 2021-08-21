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

#convert date from object to datetime format
val_data["date"] = pd.to_datetime(val_data["date"], format='%d-%m-%y')
val_data["date"] = val_data["date"].mask(val_data["date"].dt.year > 2021, 
                                         val_data["date"] - pd.offsets.DateOffset(years=100))
print(val_data.head())












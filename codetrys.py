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






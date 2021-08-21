# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 11:00:42 2021

@author: clare
"""

# import pandas, numpy and matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#import val_data.csv, ignoring the first 24 rows
val_data = pd.read_csv(r"C:\Users\clare\OneDrive\Documents\Clare\Cert in Introductory Data analytics\Weather data\Val_data.csv", skiprows=24)
print(val_data.head())

#View column names and data types of each
print(val_data.info())

#checking the number of rows and colums
print(val_data.shape)

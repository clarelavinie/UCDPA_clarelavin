# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 11:00:42 2021

@author: clare
"""

# import pandas, numpy and matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Import weather data for Valentia and check info and shape
val_data = pd.read_csv(r"C:\Users\clare\OneDrive\Documents\Clare\Cert in Introductory Data analytics\Weather data\Val_data.csv", skiprows=24)
print(val_data.info())
print(val_data.shape)

#change data from " " to NaN
val_data = val_data.replace(r'\s+', np.nan, regex=True).replace(' ', np.nan)
print(val_data.info())

#count missing data in dataset
count_missing = val_data.isnull().sum()
print(count_missing[0:26])

#replace NaN with 0
val_data = val_data.fillna(0)
check_val_data = val_data.isnull().sum()
print(check_val_data[0:26])
print(val_data.info())

#convert rain column type from object to float
val_data["rain"] = pd.to_numeric(val_data["rain"], downcast="float")
print(val_data.info())

#import weather data for Dublin airport and check info and shape
dub_data = pd.read_csv(r"C:\Users\clare\OneDrive\Documents\Clare\Cert in Introductory Data analytics\Weather data\Dub_airport_weather_data_July.csv", skiprows=25)
print(dub_data.info())
print(dub_data.shape)

#Check for missing data in weather data for Dublin Airport
count_missing_dub = dub_data.isnull().sum()
print(count_missing_dub[0:26])


#merge files and check 
weather_data = dub_data.merge(val_data, 
                              how="outer", 
                              on="date", 
                              suffixes=("_dub", "_val"))
print(weather_data.info())
print(weather_data[["rain_dub", "rain_val"]].head())

#create new file with rain data only
rain_data = weather_data[["date", "rain_dub", "rain_val"]]
print(rain_data.head())
print(rain_data.describe())


#correct date format
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


#add a column to indicate if rain day in Valentia
result = []
for value in rain_data["rain_val"]:
    if value > 0.2:
        result.append(1)
    else:
        result.append(0)
        
rain_data["raindays_val"] = result
print(rain_data)

rain_data.sum(axis=0)

#add a column to indicate if heavy rain day in Valentia
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

#Add a 20 year moving average field for Valentia and Dublin
annual_rain_data['MA_20_Dub'] = annual_rain_data["rain_dub"].expanding(min_periods=20).mean()
annual_rain_data['MA_20_Val'] = annual_rain_data["rain_val"].expanding(min_periods=20).mean()
print(annual_rain_data.head(21))

    
#Add a 20 year moving average field for Valentia and Dublin on heavy rain day columns
annual_rain_data['MA_20_Dub_h'] = annual_rain_data["heavyraindays_dub"].expanding(min_periods=20).mean()
annual_rain_data['MA_20_Val_h'] = annual_rain_data["heavyraindays_val"].expanding(min_periods=20).mean()
print(annual_rain_data.head(21))

#Add a 20 year moving average field for Valentia and Dublin for rain day columns
annual_rain_data['MA_20_Dub_n'] = annual_rain_data["raindays_dub"].expanding(min_periods=20).mean()
annual_rain_data['MA_20_Val_n'] = annual_rain_data["raindays_val"].expanding(min_periods=20).mean()
print(annual_rain_data.head(21))

#plot the yearly rainfall amounts
fig, ax = plt.subplots()
ax.plot(annual_rain_data.index, annual_rain_data["rain_dub"], marker="o", label='Dub')
ax.plot(annual_rain_data.index, annual_rain_data["rain_val"], marker="s", label='Val')
ax.plot(annual_rain_data.index, annual_rain_data["MA_20_Val"], label='20yr MA Val', linestyle='dashed')
ax.plot(annual_rain_data.index, annual_rain_data["MA_20_Dub"], label='20yr MA Dub', linestyle='dashed')
ax.set_xlabel('Year')
ax.set_ylabel('Annual Rainfall (mm)')
ax.set_title('Annual Rainfall, 1942 to 2020: Valentia and Dublin stations')
plt.legend()
plt.show()

#show heavy rain days to rain days Valentia
fig, ax = plt.subplots(2, 1, sharex=True)
fig.suptitle("Rainfall Days and Heavy Rainfall Days, 1942 - 2020, Valentia Station")
ax[0].plot(annual_rain_data.index, annual_rain_data["heavyraindays_val"], marker="s", color="r")
ax[0].plot(annual_rain_data.index, annual_rain_data["MA_20_Val_h"], label='20yr MA Val Heavy raindays', linestyle='dashed', color="c")
ax[0].set_ylabel("Heavy Rain Days\nDays Rain >=10mm")
ax[0].legend()
ax[1].plot(annual_rain_data.index, annual_rain_data["raindays_val"], marker="s", color="b")
ax[1].plot(annual_rain_data.index, annual_rain_data["MA_20_Val_n"], label='20yr MA Val Raindays', linestyle='dashed', color="g")
ax[1].set_ylabel("Rain Days\nDays Rain >=0.2mm")
ax[1].legend()
plt.show()

#show heavy rain days to rain days Dublin
fig, ax = plt.subplots(2, 1, sharex=True)
fig.suptitle("Rainfall Days and Heavy Rainfall Days, 1942 - 2020, Dublin Station")
ax[0].plot(annual_rain_data.index, annual_rain_data["heavyraindays_dub"], marker="o", color="g")
ax[0].plot(annual_rain_data.index, annual_rain_data["MA_20_Dub_h"], label='20yr MA Dub Heavy raindays', linestyle='dashed', color="r")
ax[0].set_ylabel("Heavy Rain Days\nDays Rain >=10mm")
ax[0].legend()
ax[1].plot(annual_rain_data.index, annual_rain_data["raindays_dub"], marker="o", color="m")
ax[1].plot(annual_rain_data.index, annual_rain_data["MA_20_Dub_n"], label='20yr MA Dub Raindays', linestyle='dashed', color="b")
ax[1].set_ylabel("Rain Days\nDays Rain >=0.2mm")
ax[1].legend()
plt.show()

#Create season column
SeasonDict = {12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring", 6: "Summer", 7: "Summer", \
              8: "Summer", 9: "Autumn", 10: "Autumn", 11: "Autumn"}
rain_data["Season"] = rain_data["month"].map(SeasonDict)
print(rain_data)

#groupby year and season to create new dataframe for each season for Valentia
rain_by_season = rain_data.pivot_table(index="year", columns="Season", values="rain_val", aggfunc=np.sum)
rain_by_season = rain_by_season.iloc[:-1:,]
print(rain_by_season)


#group data by season and create plots for each season
fig, ax = plt.subplots(2, 2)
fig.suptitle("Rainfall by Season (mm), 1942 - 2020, Valentia Station")
ax[0, 0].plot(rain_by_season.index, rain_by_season["Winter"], color="r")
ax[0, 0].set_ylabel("Rainfall")
ax[0, 0].set_title("Winter")
ax[0, 1].plot(rain_by_season.index, rain_by_season["Spring"], color="g")
ax[0, 1].set_title("Spring")
ax[1, 0].plot(rain_by_season.index, rain_by_season["Summer"], color="b")
ax[1, 0].set_ylabel("Rainfall")
ax[1, 0].set_title("Summer")
ax[1, 1].plot(rain_by_season.index, rain_by_season["Autumn"], color="c")
ax[1, 1].set_title("Autumn")
plt.show()








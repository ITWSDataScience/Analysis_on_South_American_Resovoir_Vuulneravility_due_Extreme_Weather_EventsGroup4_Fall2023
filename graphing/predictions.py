import pandas as pd
import os
import matplotlib.pyplot as plt 
import json
from statistics import mean 
import numpy as np

from sklearn.linear_model import LinearRegression
import netCDF4 as nc
from geopy import distance


RESERVOIRS = ["Gu","So","Tu","Ap","Il","Fu","Se","Tr","Ne","Ch","It",
             "Si", "Gr", "Pr", "Ve", "Yg", "Ba", "Bo", "Br",
             "Ho", "Ju"]
RESERVOIRS_ID = [7,10,13,29,31,40,41,46,50,51,53,60,65,67,69,81,84,87,95,115,128]
YEARS = [2000,2001,2002,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]
POPULATIONS = [304000,309000,314000,319000,323000,328000,333000,338000,343000,348000,
               354000,359000,364000,370000,375000,381000,386000,392000,397000,402000,
               408000]
NUMS_RESERVOIRS = len(RESERVOIRS)
YEAR_TO_PREDICT = [2050]

## replace with your local file
PRECIPITATIONS_DIRECTORY = '/Users/tommy/Downloads/Precipitation Datasets'
EVAPORATION_DIRECTORY = '/Users/tommy/Downloads/Reservoir Dataset/reservoir.json' 

PRECIPITATION_PER_RESERVOIR = {} ## reservoir -> precipitation
EVAPORATION_PER_RESERVOIR = {} ## reservoir -> evaporation
EXPECTED_VOLUME_CHANGE_PER_RESERVOIR = {}
ACTUAL_VOLUME_CHANGE_PER_RESERVOIR = {}

"""
Step 1. We calculate the amount of water coming into the reservoirs through precipitation. 
"""
for filename in os.listdir(PRECIPITATIONS_DIRECTORY):
    f = os.path.join(PRECIPITATIONS_DIRECTORY, filename)
    if os.path.isfile(f):
        df = pd.read_csv(f, header=9)
        rain_each_year = []
        for year in YEARS:
            rain_for_that_year = 0
            rows = df.loc[df['YEAR'] == year]["ANN"]
            for row in rows:
                rain_for_that_year+=row
            rain_each_year.append(round(rain_for_that_year,4))
        PRECIPITATION_PER_RESERVOIR[filename] = rain_each_year

testing = "65_GrandeReservoir_2000_2022.csv"
testingid = testing.split("_")[0]
# print(testingid)
# print(PRECIPITATION_PER_RESERVOIR[testing])
# print(len(PRECIPITATION_PER_RESERVOIR[testing]))

## get delta volume of precipitation
year_volume_delta = {}
for i in range(1,len(YEARS)):
    year_start_end = YEARS[i]
    volume_delta = PRECIPITATION_PER_RESERVOIR[testing][i] - PRECIPITATION_PER_RESERVOIR[testing][i-1]
    year_volume_delta[year_start_end] = round(volume_delta,4)
# print(year_volume_delta)

## MODEL TRAINING
# x = 
# y = 
# model = LinearRegression()
# model.fit(x,y)
# y_pred = model.predict(np.array(YEAR_TO_PREDICT).reshape((-1,1)))
# print(y_pred)
# x = np.array(list(year_volume_delta.keys()))
# y = np.array(list(year_volume_delta.values()))

# print(x)
# print(y)
# plt.plot(x,y,'ob')
# plt.show()

"""
Step 2. We calculate how much water is lost from the reservoirs due to evaporation. 
"""
file = open(EVAPORATION_DIRECTORY)
data = json.load(file)

evaperation_per_resvior = []
storage_change_per_resvior = []
for resvior in RESERVOIRS_ID:
    evaperation_per_year = []
    storage_change_per_year = []
    for year in range(23):
        evaperation_per_month = []
        if data[str(resvior)][year*12+0][5] > 0 and data[str(resvior)][year*12+11][5] > 0: 
            lake_storage_bgn_of_year = data[str(resvior)][year*12+0][5]
            lake_storage_end_of_year = data[str(resvior)][year*12+11][5]
            storage_change_per_year.append(lake_storage_end_of_year - lake_storage_bgn_of_year)      
        for month in range(12):
            if data[str(resvior)][year*12+month][6] > 0:
                evaperation_per_month.append(data[str(resvior)][year*12+month][6])
        evaperation_per_year.append(mean(evaperation_per_month))
    
    storage_change_per_resvior.append(mean(storage_change_per_year))
    evaperation_per_resvior.append(mean(evaperation_per_year))
    EVAPORATION_PER_RESERVOIR[resvior] = evaperation_per_resvior
    ACTUAL_VOLUME_CHANGE_PER_RESERVOIR[resvior] = storage_change_per_resvior

# print(evaperation_per_resvior)
# print(len(evaperation_per_resvior))

"""
Step 3. We will use these values to calculate the expected change in the reservoirs's volume.
"""
for key, value in PRECIPITATION_PER_RESERVOIR.items():
    temp = []
    tempid = int(key.split("_")[0])
    for i in range(len(value) - 1):
        temp.append( value[i] - EVAPORATION_PER_RESERVOIR[tempid][i] )
    EXPECTED_VOLUME_CHANGE_PER_RESERVOIR[key] = temp
    # print("for key " + key )
    # print("the expected was ")
    # print(EXPECTED_VOLUME_CHANGE_PER_RESERVOIR[key])
    # print("the actual was ")
    # print(ACTUAL_VOLUME_CHANGE_PER_RESERVOIR[tempid])

# t = np.array(list(year_volume_delta.keys()))
# data1 = np.array(list(EXPECTED_VOLUME_CHANGE_PER_RESERVOIR[testing]))
# data2 = np.array(list(ACTUAL_VOLUME_CHANGE_PER_RESERVOIR[int(testingid)]))

# lines = plt.plot(t, data1, t, data2, 'o')
# plt.setp(lines[0], linewidth=4)
# plt.setp(lines[1], linewidth=2)

# plt.legend(('Expected', 'Actual'),
#            loc='upper right')

# plt.title(testing)
# plt.tight_layout()  # otherwise the right y-label is slightly clipped
# plt.show()

# print(EXPECTED_VOLUME_CHANGE_PER_RESERVOIR)
"""
Step 4. Compare this to the actual change in the reservoirs’ volume to estimate how much of the water is being taken out for human use.
"""
def getClosestIndex(population, lat, lon):
    return (np.abs(population['latitude'][:] - lat).argmin(), np.abs(population['longitude'][:]-lon).argmin())

# data = nc.Dataset('/Users/tommy/Downloads/Population Dataset/gpw_v4_population_density_adjusted_rev11_2pt5_min_1_5.nc')
# genDataset = data.variables['UN WPP-Adjusted Population Density, v4.11 (2000, 2005, 2010, 2015, 2020): 2.5 arc-minutes'][:]
# print(data.variables.keys())
# print(getClosestIndex(data, 180, -91))
# print(genDataset.shape)
# # get longitude index value, latitude
# print(data.variables['longitude'][1])
# print(data.variables['latitude'][1])

def findPopulationData(data, lat, lon, dist=100):
    origLatIndex, origLongIndex = getClosestIndex(data, lat, lon)
    totalPop = [0, 0, 0, 0, 0]
    checks = [0, 0, 0, 0]
    processedSize = 0
    processedData = set()
    dataToProcess = []
    dataToProcess.append((origLatIndex, origLongIndex))
    while len(dataToProcess) > 0:
        # processedSize += 1
        # if processedSize % 10 == 0:
        #     print(processedSize)
        # if processedSize % 10 == 0:
        #     break
        latIndex, lonIndex = dataToProcess.pop()
        if (latIndex, lonIndex) in processedData:
            continue
        processedData.add((latIndex, lonIndex))
        # checksTime = time.time()
        if latIndex < 0 or latIndex >= genDataset.shape[1] or lonIndex < 0 or lonIndex >= genDataset.shape[2]:
            continue
        if distance.distance((data.variables['latitude'][origLatIndex], data.variables['longitude'][origLongIndex]), (data.variables['latitude'][latIndex], data.variables['longitude'][lonIndex])).km > dist:
            continue
        # checks[0] += time.time() - checksTime
        # checksTime = time.time()
        for i in range(5):
            currItem = genDataset[i][latIndex][lonIndex]
            if currItem > 0:
                totalPop[i] += currItem
        # checks[1] += time.time() - checksTime
        # checksTime = time.time()
        for i in range(-1, 2):
            for j in range(-1, 2):
                dataToProcess.append((latIndex + i, lonIndex + j))
        # checks[2] += time.time() - checksTime
        # checksTime = time.time()
    return totalPop
"""
Step 5. Use the population density data of the regions surrounding the reservoir to calculate the water use per capita of each reservoir.
"""
diff = []
for i in range (len(EXPECTED_VOLUME_CHANGE_PER_RESERVOIR[testing])):
    diff.append(round(EXPECTED_VOLUME_CHANGE_PER_RESERVOIR[testing][i] - ACTUAL_VOLUME_CHANGE_PER_RESERVOIR[int(testingid)][i])  )

print(POPULATIONS)
print(diff)

POPULATIONS_STRING = []
for i in range(len(POPULATIONS)):
    POPULATIONS_STRING.append(str(POPULATIONS[i]/1000))

# plt.bar(POPULATIONS[0:3],diff[0:3], color='g')
# plt.show()


data = {'C':20, 'C++':15, 'Java':30, 
        'Python':35}
courses = list(POPULATIONS_STRING[0:10])
values = list(diff[0:10])
  
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(courses, values, color ='maroon', 
        width = 0.4)
 
plt.xlabel("Population (*1000 scale)")
plt.ylabel("Volume delta ")
plt.title("Volume delta per population")
plt.show()
import pandas as pd
import os
import matplotlib.pyplot as plt 
import json
from statistics import mean 
import numpy as np
directory = ''
 
# reserviors = ["Guri","Sobradinho","Tucurui","Aperea","ILha Solteira","Furnas","Serra De Masa","Tres Marias","Negro","Chocon","Itaparica",
#              "Sao Simao", "Grande", "Promissao", "Agua Vermelha", "Lago Del Rio Yguaza", "Los Barreales", "Barra Bonita", "Lago Das Brisas",
#              "Hondo", "Junin"]


reserviors = ["Gu","So","Tu","Ap","Il","Fu","Se","Tr","Ne","Ch","It",
             "Si", "Gr", "Pr", "Ve", "Yg", "Ba", "Bo", "Br",
             "Ho", "Ju"]


rain_for_each_resvoir = []

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        df = pd.read_csv(f, header=9)
        years = [2000,2001,2002,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]
        rain_for_all_time = 0
        for year in years:
            rows = df.loc[df['YEAR'] == year]["ANN"]
            rain_for_that_year = 0
            # print(rows)
            for row in rows:
                # print(row)
                rain_for_that_year+=row
        rain_for_all_time+=rain_for_that_year
    
    rain_for_each_resvoir.append(rain_for_all_time/23)


# fig = plt.figure(figsize = (10, 5))
 
directory2 = ''
file = open(directory2)
data = json.load(file)

resvior_ids = [7,10,13,29,31,40,41,46,50,51,53,60,65,67,69,81,84,87,95,115,128]
evaperation_per_resvior = []
storage_change_per_resvior = []
for resvior in resvior_ids:
    evaperation_per_year = []
    storage_change_per_year = []
    for year in range(23):
        evaperation_per_month = []
        
        if data[str(resvior)][year*12+0][5] > 0 and data[str(resvior)][year*12+11][5] > 0: 
            lake_storage_bgn_of_year = data[str(resvior)][year*12+0][5]
            lake_storage_end_of_year = data[str(resvior)][year*12+11][5]
            storage_change_per_year.append(lake_storage_end_of_year - lake_storage_bgn_of_year)
            print(lake_storage_bgn_of_year)
            print(lake_storage_end_of_year)
            print("ran")
        
        
        for month in range(12):
            # print(data[str(resvior)][year*12+month])
            if data[str(resvior)][year*12+month][6] > 0:
                evaperation_per_month.append(data[str(resvior)][year*12+month][6])
        evaperation_per_year.append(mean(evaperation_per_month))
    
    print(storage_change_per_year)
    storage_change_per_resvior.append(mean(storage_change_per_year))
    evaperation_per_resvior.append(mean(evaperation_per_year))



# x_axis =  np.arange(len(reserviors)) 


# plt.bar(x_axis - 0.2, rain_for_each_resvoir, 0.2, label = 'rate of precipitation',  color ='blue')
# plt.bar(x_axis, evaperation_per_resvior, 0.2, label = 'rate of evaporation',  color ='orange')


# # plt.bar(features2, base_sep, color ='blue', 
# #         width = 0.4)
# # plt.bar(features2, ten_sep, color ='yellow', 
# #         width = 0.4)
# # plt.bar(features2, fifty_sep, color ='yellow', 
# #         width = 0.4)
 
# plt.xticks(x_axis, reserviors)
 
# plt.xlabel("reserviors")
# plt.ylabel("mm/day")
# plt.title("Rate of precipitation vs. Rate of evaporation")

# plt.legend()
# plt.savefig('fig.png')
# plt.show()

# fig = plt.figure()

# ax = fig.add_axes([0,0,1,1])
# # Creating plot
# plt.xlabel("reserviors")
# plt.ylabel("mm/day")

# bp = plt.boxplot([rain_for_each_resvoir,evaperation_per_resvior])

# plt.savefig('fig2.png')


print(mean(rain_for_each_resvoir))

print(mean(evaperation_per_resvior))




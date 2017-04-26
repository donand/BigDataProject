# -- coding: utf-8 --
"""
Created on Thu Apr 13 18:15:03 2017

@author: ghion
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gmplot
from sklearn.cluster import DBSCAN
from sklearn import metrics
import matplotlib.pyplot as plt

df = pd.read_csv("../phone.csv")

cellnames= df.squareid.unique() #quante celle sono
singlecell= df[df['squareid']==cellnames[0]]
var=singlecell.iloc[0]
days = singlecell.day.unique()
totalactivities= sum(df['activity'])
#counts=(len(df[df['squareid']==x]) for x in cellnames)

aggr= df.groupby(['squareid','timeslot','day','lat','lon'])
roman=aggr.sum()

aggrdf=pd.DataFrame(data=roman.index )
aggrdf=pd.DataFrame(aggrdf[0].tolist())
aggrdf.columns =['squareid','timeslot','day','lat','lon']
aggrdf = aggrdf.assign(activity=roman['activity'].values)

#adesso levo i giorni e riaggrego
aggrdf_hour=aggrdf.drop('day' , axis=1)
aggrdf_hour= aggrdf.groupby(['squareid','timeslot','lat','lon'])
roman2=aggrdf_hour.sum()

aggrdf_hour=pd.DataFrame(data=roman2.index )
aggrdf_hour=pd.DataFrame(aggrdf_hour[0].tolist())
aggrdf_hour.columns =['squareid','timeslot','lat','lon']
aggrdf_hour = aggrdf_hour.assign(activity=roman2['activity'].values)

#aggrdf_hour.to_csv(open("Data/phone_aggregated_by_timeslot.csv", 'w'), index = False)

ACT_THRESH=1000
lat_0=[]
lat_1=[]
lat_2=[]
lat_3=[]
lon_0=[]
lon_1=[]
lon_2=[]
lon_3=[]
aggrdf_tmp=aggrdf_hour[aggrdf_hour['activity']>ACT_THRESH]


def appendpoint(lat,lon,row):
    for i in range(0,int(row[5]/1500)):
        lat.append(row[3])
        lon.append(row[4])

for row in aggrdf_hour.itertuples():
    if(row[2]==0):
            appendpoint(lat_0,lon_0,row)
    if(row[2]==1):
            appendpoint(lat_1,lon_1,row)
    if(row[2]==2):
            appendpoint(lat_2,lon_2,row)
    if(row[2]==3):
            appendpoint(lat_3,lon_3,row)
            

#lat=[row[3]for row in aggrdf_hour.itertuples() if row[5]>ACT_THRES]
#lon=[row[4]for row in aggrdf_hour.itertuples() if row[5]>ACT_THRES]
R=30
gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 11)
gmap.heatmap(lat_0, lon_0,radius=R)
gmap.draw("phone_by_hour_0.html")

gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 11)
gmap.heatmap(lat_1, lon_1,radius=R)
gmap.draw("phone_by_hour_1.html")

gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 11)
gmap.heatmap(lat_2, lon_2,radius=R)
gmap.draw("phone_by_hour_2.html")

gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 11)
gmap.heatmap(lat_3, lon_3,radius=R)
gmap.draw("phone_by_hour_3.html")


'''
for i in range(0,len(cellnames)):
   lat=df[df['squareid']==cellnames[i]].iloc[0].lat
   lon=df[df['squareid']==cellnames[i]].iloc[0].lon
   tot_activity_per_cell.append([cellnames[i], sum(df[df['squareid']==cellnames[i]].activity),lat,lon ])
   

df2 = pd.DataFrame(tot_activity_per_cell)
df2.columns=['id','activity','lat','lon']
df2= df2.sort_values('activity', ascending=False)

#Qui plotto la mappa
gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 13)
lat= [x[2] for x in tot_activity_per_cell]
lon= [x[3] for x in tot_activity_per_cell]

#gmap.plot(lat, lon, 'cornflowerblue', edge_width=2)
#gmap.scatter([45.482291], [9.187500], '#3B0B39', size=40, marker=False)
#gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
gmap.heatmap(lat, lon)

gmap.draw("mymap.html")
'''
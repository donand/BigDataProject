# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 18:15:03 2017

@author: ghion
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gmplot

df = pd.read_csv("./Data/fuorisalone_2016_phone-data/phone.csv")

cellnames= df.squareid.unique() #quante celle sono
singlecell= df[df['squareid']==cellnames[0]]
var=singlecell.iloc[0]
days = singlecell.day.unique()
totalactivities= sum(df['activity'])
sorteddf= df.sort_values('squareid')
sorteddf.to_csv("./Data/fuorisalone_2016_phone-data/phonesorted.csv",index=False)
#counts=(len(df[df['squareid']==x]) for x in cellnames)


tot_activity_per_cell= []
for i in range(0,len(cellnames)):
   lat=df[df['squareid']==cellnames[i]].iloc[0].lat
   lon=df[df['squareid']==cellnames[i]].iloc[0].lon
   tot_activity_per_cell.append([cellnames[i], sum(df[df['squareid']==cellnames[i]].activity),lat,lon ])

df2 = pd.DataFrame(tot_activity_per_cell)
df2.columns=['id','activity']
df2= df2.sort_values('activity', ascending=False)

#Qui plotto la mappa
gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 13)
lat= [x[2] for x in tot_activity_per_cell]
lon= [x[3] for x in tot_activity_per_cell]
gmap.plot(lat, lon, 'cornflowerblue', edge_width=2)
#gmap.scatter([45.482291], [9.187500], '#3B0B39', size=40, marker=False)
#gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
gmap.heatmap([45.482291], [9.187500])

gmap.draw("mymap.html")
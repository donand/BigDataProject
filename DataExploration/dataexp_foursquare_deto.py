# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 11:37:10 2017

@author: Riccardo
"""

import pandas as pd
import csv
import numpy as np
import gmplot

dataset = pd.read_csv('Data/fuorisalone_foursquare-history-2016-04.csv', converters={'history.date': lambda x: x.replace('T',''), 'history.date': lambda x: x.replace('Z','')})
dataset['history.date']=pd.to_datetime(dataset['history.date'],format='%Y-%m-%dT%H:%M')

dataset.describe()

aggr = dataset.groupby(['location.city','history.date'])

dataset.index = dataset['history.date']
date_aggr = pd.groupby(dataset,by=[dataset.index.day,'location.city'])
#to visualize tab with day/city/checkins
date_aggr.sum()

mask = (dataset['history.date'] > pd.to_datetime('11-04-2016',format='%d-%m-%Y')) & (dataset['history.date'] <= pd.to_datetime('17-04-2016',format='%d-%m-%Y'))
df_slice = dataset[mask]

lats_fuori = df_slice['loc.1']
longs_fuori = df_slice['loc.0']

mask2 = (dataset['history.date'] < pd.to_datetime('11-04-2016',format='%d-%m-%Y')) | (dataset['history.date'] >= pd.to_datetime('17-04-2016',format='%d-%m-%Y'))
df_slice2 = dataset[mask2]
lats = df_slice2['loc.1']
longs = df_slice2['loc.0']

gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 13)
gmap.heatmap(lats[:], longs[:], radius = 50, threshold = 1, opacity = 0.5, dissipating= True)
#gmap.scatter(lats[:1000],longs[:1000], '#3B0B39', size=40, marker=False)
gmap.draw("4square.html")

gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 13)
gmap.heatmap(lats_fuori[:], longs_fuori[:], radius = 50, threshold = 1, opacity = 0.5, dissipating= True)
#gmap.scatter(lats[:1000],longs[:1000], '#3B0B39', size=40, marker=False)
gmap.draw("4square_fuorisalone.html")


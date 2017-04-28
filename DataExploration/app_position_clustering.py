# -- coding: utf-8 --
"""
Created on Mon Apr 24 18:00:07 2017

@author: Riccardo
"""

import pandas as pd
import json
from pandas.io.json import json_normalize
import gmplot
import gmaps
import numpy as np
import math
from sklearn.cluster import DBSCAN
from sklearn import metrics
import matplotlib.pyplot as plt


DEG_DIST_LAT = 111142
DEG_DIST_LON = 78100
COLORS_HC = ['#f44336','#76ff03','ffff00','0091ea','9c27b0','827717','e65100','000000','ffffff','795548','#7df9ff',"ffabcd","abcdef","befcdf"]
COLORS_LAB = ['red','blue','green','purple','black','yellow','orange','pink','white','brown','grey','cyan','violet','lime','aquamarine','coral','crimson']

df_position = pd.read_csv("Data/fuorisalone_2016_anonymous_appdata/anon_db/position.csv",encoding="latin1")
df_position['date']=pd.to_datetime(df_position['date'])


def cluster_by_time(start_time, end_time, eps, min_samples, filename):
    mask = (df_position['date'] > pd.to_datetime('11-04-2016',format='%d-%m-%Y')) &\
    (df_position['date'] <= pd.to_datetime('18-04-2016',format='%d-%m-%Y')) &\
    (df_position.date.dt.hour < end_time) & (df_position.date.dt.hour >= start_time) &\
    (df_position.latitude > 45.443041) & (df_position.longitude > 9.133225) &\
    (df_position.latitude < 45.500763) & (df_position.longitude < 9.252532)
    sliced = df_position[mask]
    sliced = sliced[['latitude','longitude']].reset_index()
    sliced = sliced.drop('index',axis = 1)
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(sliced)
    labels = db.labels_
    max_color = int("FFFFFF",16)
    colors = [hex(i*max_color/(labels.max() + 1)) for i in range(1, labels.max() + 2)]
    gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 13)
    for label in range(0, labels.max() + 1):
        gmap.scatter(sliced['latitude'][pd.Series(labels) == label], sliced['longitude'][pd.Series(labels) == label], COLORS_HC[label], size=10, marker=False)
        print 'Cluster ' + str(label) + ' ' + str(labels.tolist().count(label))
        plt.scatter(sliced['longitude'][pd.Series(labels) == label], sliced['latitude'][pd.Series(labels) == label], color = COLORS_LAB[label])
    gmap.draw("DataExploration/MapPlots/" + filename)
    plt.show()
    
cluster_by_time(0, 6, 0.0015, 300, 'clust_0_6.html')
    
cluster_by_time(6,12, 0.0015, 500, 'clust_6_12.html')

cluster_by_time(12, 18, 0.0015, 500, 'clust_12_18.html')

cluster_by_time(18, 24, 0.0015, 500, 'clust_18_24.html')
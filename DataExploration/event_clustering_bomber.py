# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:23:30 2017

@author: ghion
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gmplot
from sklearn.cluster import DBSCAN
from sklearn import metrics
import matplotlib.pyplot as plt

COLORS_HC = ['#f44336','#76ff03','ffff00','0091ea','9c27b0','827717','e65100','000000','ffffff','795548','#7df9ff']
COLORS_LAB = ['red','blue','green','purple','black','yellow','orange','pink','white','brown','grey','cyan','violet','lime','aquamarine','coral','crimson','red','blue','green','purple','black','yellow','orange','pink','white','brown','grey','cyan','violet','lime','aquamarine','coral','crimson','red','blue','green','purple','black','yellow','orange','pink','white','brown','grey','cyan','violet','lime','aquamarine','coral','crimson','red','blue','green','purple','black','yellow','orange','pink','white','brown','grey','cyan','violet','lime','aquamarine','coral','crimson']


df = pd.read_csv("Data/fuorisalone_2016_anonymous_appdata/anon_db/event_locations.csv")
gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 13)
gmap.scatter(df['latitude'].tolist(), df['longitude'].tolist(), 'k', marker=False)
gmap.draw('events.html')

sliced= df.drop('id_event',axis=1)
#(eps=0.0019, min_samples=3) 34 clust 34
db = DBSCAN(eps=0.0016, min_samples=5).fit(sliced)
#eps=0.0016, min_samples=5 23 clust 220 outl
#eps=0.0017, min_samples=5 21 clust 208 outl
labels = db.labels_
max_color = int("FFFFFF",16)
colors = [hex(int(i*max_color/(labels.max() + 1))) for i in range(1, labels.max() + 2)]
gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 13)
for label in range(-1, labels.max() + 1):
    gmap.scatter(sliced['latitude'][pd.Series(labels) == label], sliced['longitude'][pd.Series(labels) == label], colors[label], size=10, marker=False)
    print('Cluster ' + str(label) + ' ' + str(labels.tolist().count(label)))
    plt.scatter(sliced['longitude'][pd.Series(labels) == label], sliced['latitude'][pd.Series(labels) == label],  color = COLORS_LAB[label])
gmap.draw("DataExploration/MapPlots/" + 'event_clustering.html')
plt.show()

df['cluster'] = labels

  
  
outliers= df[df.cluster == -1].copy()
sliced = outliers[['latitude','longitude']].reset_index(drop=True)
db_out = DBSCAN(eps=0.0062, min_samples=5).fit(sliced)


labels = db_out.labels_
max_color = int("FFFFFF",16)
colors = [str('#') + str(hex(int(i*max_color/(labels.max() + 1)))) for i in range(1, labels.max() + 2)]
gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 13)
for label in range(-1, labels.max() + 1):
    gmap.scatter(sliced['latitude'][pd.Series(labels) == label], sliced['longitude'][pd.Series(labels) == label], colors[label], size=50, marker=False)
    print('Cluster ' + str(label) + ' ' + str(labels.tolist().count(label)))
    plt.scatter(sliced['longitude'][pd.Series(labels) == label], sliced['latitude'][pd.Series(labels) == label],  color = COLORS_LAB[label])
gmap.draw("DataExploration/MapPlots/" + 'event_clustering.html')
plt.show()

outliers['cluster'] = labels - (max(labels) + 1)

#pd.options.mode.chained_assignment = None  # default='warn'
#df[df.cluster == -1]['cluster'] = outliers['cluster']

df.drop(df[df.cluster == -1].index,inplace=True)
#outliers.drop(['latitude','longitude'],axis=1,inplace=True)

#df = pd.merge(df, outliers, left_on = 'id_event', right_on = 'id_event', how = 'left', suffixes = ('', '_out'))
#df = df.drop(['latitude_y', 'longitude_x'], axis = 1)
res= pd.concat([df,outliers])
res.to_csv("Data/fuorisalone_2016_anonymous_appdata/anon_db/event_clustered.csv",index=False)
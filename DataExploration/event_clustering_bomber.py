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
COLORS_LAB = ['red','blue','green','purple','black','yellow','orange','pink','white','brown','grey','cyan','violet','lime','aquamarine','coral','crimson','red','blue','green','purple','black','yellow','orange','pink','white','brown','grey','cyan','violet','lime','aquamarine','coral','crimson']


df = pd.read_csv("Data/fuorisalone_2016_anonymous_appdata/anon_db/event_locations.csv")
gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 13)
gmap.scatter(df['latitude'].tolist(), df['longitude'].tolist(), 'k', marker=False)
gmap.draw('events.html')

sliced= df.drop('id_event',axis=1)
#(eps=0.0019, min_samples=2) 34 clust 34
db = DBSCAN(eps=0.0019, min_samples=2).fit(sliced)

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
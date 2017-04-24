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
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

#TODO
#Read CSV ----
#position dataframe

df_position['date']=pd.to_datetime(df_position['date'], unit = 'ms')
mask_1 = (df_position['date'] > pd.to_datetime('11-04-2016',format='%d-%m-%Y')) & (df_position['date'] <= pd.to_datetime('18-04-2016',format='%d-%m-%Y')) & (df_position.date.dt.hour < 6)

slice_1 = df_position[mask_1]
slice_1 = slice_1[['latitude','longitude']].reset_index()

db = DBSCAN(eps=0.6, min_samples=100).fit(slice_1)

labels = db.labels_

max_color = int("FFFFFF",16)
colors = [hex(i*max_color/(labels.max() + 1)) for i in range(1, labels.max() + 2)]

gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 13)
for label in range(labels.max() + 1):
    gmap.scatter(slice_1['latitude'][pd.Series(labels) == label], slice_1['longitude'][pd.Series(labels) == label], colors[label], size=40, marker=False)
gmap.draw("position.html")
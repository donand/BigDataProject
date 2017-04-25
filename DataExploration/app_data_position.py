# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 15:36:34 2017

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

timeslots = {0 : {start : 0, end : 6}, 1 : {start : 6, end : 12}, 2 : {start : 12, end : 18}, 3 : {start : 18, end : 24}}

df_position = pd.read_csv("Data/fuorisalone_2016_anonymous_appdata/anon_db/position.csv", encoding = 'latin1')
event = pd.read_csv("", encoding = 'latin1')

def count_pos(timeslot, latitude, longitude):
    mask = (np.sqrt(((df_position['latitude'].map(lambda x: x - latitude)) * DEG_DIST_LAT)**2 + ((df_position['longitude'].map(lambda x: x - longitude)) * DEG_DIST_LON)**2) < 150) &\
    (df_position['date'] > pd.to_datetime('11-04-2016',format='%d-%m-%Y')) &\
    (df_position['date'] <= pd.to_datetime('18-04-2016',format='%d-%m-%Y')) &\
    (df_position.date.dt.hour < timeslots[timeslot][end]) &\
    (df_position.date.dt.hour >= timeslots[timeslot][start])
    return len(df_position[mask])

event['position_count'] = pd.Series([count_pos(row['timeslot'],row['latitude'],row['longitude']) for index, row in event.iterrows()])
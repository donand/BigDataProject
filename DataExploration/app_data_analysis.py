# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 16:12:19 2017

@author: Riccardo
"""

import pandas as pd
import json
from pandas.io.json import json_normalize
import gmplot
import gmaps
import numpy as np
import math

DEG_DIST_LAT = 111142
DEG_DIST_LON = 78100

df = pd.read_json("C:\Users\Riccardo\Documents\GitHub\BigDataProject\Data\fuorisalone_2016_anonymous_appdata\anon_db\event.json")
event_list = []
with open('Data/fuorisalone_2016_anonymous_appdata/anon_db/events_analytic.json') as f:
    text = f.read()
    for line in text.split('\n'):
        try:
            event_list.append(json.loads(line))
        except:
            pass
df_event = json_normalize(event_list)

position_list = []
with open('Data/fuorisalone_2016_anonymous_appdata/anon_db/position.json') as f:
    text = f.read()
    for line in text.split('\n'):
        try:
            position_list.append(json.loads(line))
        except:
            pass
df_position = json_normalize(position_list)
del position_list
del text

lats = df_position[df_position.latitude > 45.428129]
lats = lats[lats.latitude < 45.497044]
longs = lats['longitude']
lats = lats['latitude']
test = df_event.to_dict()

gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 13)
gmap.heatmap(lats[:], longs[:], radius = 50, threshold = 1, opacity = 0.5, dissipating= True)
#gmap.scatter(lats[:1000],longs[:1000], '#3B0B39', size=40, marker=False)
gmap.draw("position.html")


agenda_list = []
with open('Data/fuorisalone_2016_anonymous_appdata/anon_db/agenda_analytics.json') as f:
    text = f.read()
    for line in text.split('\n'):
        agenda_list.append(json.loads(line))
df_agenda_analytics = json_normalize(agenda_list)


tmp['date']=pd.to_datetime(df_event['date'], unit = 'ms').normalize()

df_event['event'].value_counts()

aggr = df_event.groupby([pd.DatetimeIndex(df_event['date']).normalize(),'event'])

df_event.index = df_event['date']
date_aggr = pd.groupby(df_event,by=[df_event.index.day,'event'])

zones = {"Brera" : {'latitude': 45.472879, 'longitude' : 9.185288, 'radius': 750}, 
         "Tortona":{'latitude': 45.452803, 'longitude' : 9.166398, 'radius': 750},
         "Quadrilatero":{'latitude': 45.466730, 'longitude' : 9.197431, 'radius': 500},
         "Lambrate":{'latitude': 45.484270, 'longitude' :  9.242877, 'radius': 750},
         }

def belong_to(latitude, longitude):
    for zone in zones.keys():
        if math.sqrt((abs(zones[zone]['latitude'] - latitude) * DEG_DIST_LAT)**2 + (abs(zones[zone]['longitude'] - longitude) * DEG_DIST_LON)**2) < zones[zone]['radius']:
            return zone
    return None

df_position['zone'] = pd.Series([belong_to(row['latitude'],row['longitude'] )for index, row in df_position[['latitude', 'longitude']].iterrows()])







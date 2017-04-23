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

df = pd.read_json("C:\Users\Riccardo\Documents\GitHub\BigDataProject\Data\fuorisalone_2016_anonymous_appdata\anon_db\event.json")
event_list = []
with open('Data/fuorisalone_2016_anonymous_appdata/anon_db/events_analytic.json') as f:
    text = f.read()
    for line in text.split('\n'):
        event_list.append(json.loads(line))
df_event = json_normalize(event_list)

position_list = []
with open('Data/fuorisalone_2016_anonymous_appdata/anon_db/position.json') as f:
    text = f.read()
    for line in text.split('\n'):
        position_list.append(json.loads(line))
df_position = json_normalize(position_list)

lats = df_position['latitude']
longs = df_position['longitude']


gmap = gmplot.GoogleMapPlotter(45.4822916634, 9.1875001735, 13)
#gmap.heatmap(lats[:], longs[:], radius = 50, threshold = 1, opacity = 0.5, dissipating= True)
gmap.scatter(lats[:200],longs[:200], '#3B0B39', size=40, marker=False)
gmap.draw("position.html")


agenda_list = []
with open('Data/fuorisalone_2016_anonymous_appdata/anon_db/agenda_analytics.json') as f:
    text = f.read()
    for line in text.split('\n'):
        agenda_list.append(json.loads(line))
df_agenda_analytics = json_normalize(agenda_list)






for lat, lng in zip(lats[:20], longs[:20]):
    print (lat, lng)
    
m = gmaps.Map()
m.add_layer(gmaps.heatmap_layer([(lat, lng) for lat,lng in zip(lats[:200],longs[:200])]))


tmp['date']=pd.to_datetime(df_event['date'], unit = 'ms').normalize()

df_event['event'].value_counts()

aggr = df_event.groupby([pd.DatetimeIndex(df_event['date']).normalize(),'event'])

df_event.index = df_event['date']
date_aggr = pd.groupby(df_event,by=[df_event.index.day,'event'])







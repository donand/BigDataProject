# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:18:51 2017

@author: Riccardo
"""

import pandas as pd
import json
from pandas.io.json import json_normalize
import gmplot
import gmaps
import numpy as np

event = pd.read_csv("Data/fuorisalone_2016_anonymous_appdata/anon_db/events_definitivo.csv",encoding="latin1")

categories = [str(x[1]).split(",") for x in event['categories'].iteritems()]


flat_cat = [x for category in categories for x in category]

flat_cat_Set = set(flat_cat)
flat_cat_Set.discard(' giocattoli')
flat_cat_Set.discard(' workshop')

categories = [list(set.intersection(set(x), flat_cat_Set)) for x in categories]

for cat in flat_cat_Set:
    event[cat] = pd.Series(np.zeros(len(categories)))

#event.drop([' giocattoli',' workshop'],axis=1,inplace=True)
        
for index, ev in event.iterrows():
    for cat in categories[index]:
        #print index, cat
        event.set_value(index,cat,1)
        
event.drop(['categories','latitude','longitude','cell','id_event'],axis=1,inplace=True)

event.to_csv("Data/fuorisalone_2016_anonymous_appdata/anon_db/events_ready_to_pre.csv",index=False)
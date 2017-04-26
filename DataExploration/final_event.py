# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:08:10 2017

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

event = pd.read_csv("Data/fuorisalone_2016_anonymous_appdata/anon_db/events_with_counts.csv",encoding="latin1")

cluster = pd.read_csv("Data/fuorisalone_2016_anonymous_appdata/anon_db/event_clustered.csv",encoding="latin1").drop(['latitude','longitude'],axis=1)

res = pd.merge(event,cluster,left_on='id_event',right_on='id_event')

res.to_csv("Data/fuorisalone_2016_anonymous_appdata/anon_db/events_definitivo.csv",index=False)
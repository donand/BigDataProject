# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 11:37:10 2017

@author: Riccardo
"""

import pandas as pd
import csv
import numpy as np

dataset = pd.read_csv('Data/fuorisalone_foursquare-history-2016-04.csv', converters={'history.date': lambda x: x.replace('T',''), 'history.date': lambda x: x.replace('Z','')})
dataset['history.date']=pd.to_datetime(dataset['history.date'],format='%Y-%m-%dT%H:%M')

dataset.describe()

aggr = dataset.groupby(['location.city','history.date'])

dataset.index = dataset['history.date']
date_aggr = pd.groupby(dataset,by=[dataset.index.day,'location.city'])
#to visualize tab with day/city/checkins
date_aggr.sum()


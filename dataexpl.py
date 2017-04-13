# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 18:15:03 2017

@author: ghion
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("./Data/fuorisalone_2016_phone-data/phone.csv")
cellnames= df.squareid.unique() #quante celle sono
singlecell= df[df['squareid']==cellnames[0]]
days = singlecell.day.unique()
totalactivities= sum(df['activity'])
sorteddf= df.sort_values('squareid')
sorteddf.to_csv("./Data/fuorisalone_2016_phone-data/phonesorted.csv",index=False)
#counts=(len(df[df['squareid']==x]) for x in cellnames)

occurrency_per_cell= df.squareid.value_counts()

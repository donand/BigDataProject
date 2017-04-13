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

tot_activity_per_cell= []
for i in range(0,len(cellnames)):
    tot_activity_per_cell.append([cellnames[i], sum(df[df['squareid']==cellnames[i]].activity) ])

df2 = pd.DataFrame(tot_activity_per_cell)
df2.columns=['id','activity']
df2= df2.sort_values('activity', ascending=False)
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 10:06:48 2017

@author: ghion
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gmplot
from sklearn.cluster import DBSCAN
from sklearn import metrics
import matplotlib.pyplot as plt

#pulisco df
df=pd.read_csv("Data/fuorisalone_2016_anonymous_appdata/anon_db/events_full_coloumn.csv", encoding= 'latin1')
tmp=[x for x in range(9, 30)]
df.drop(df.columns[tmp], axis=1, inplace=True)
df.drop(['latitude','longitude','cell'],axis=1, inplace=True)

#trovo i 4 cluster più grandi
perf=[[df[(df['cluster']==i) & (df['timeslot'] == j)].activity.sum(),df[(df['cluster']==i) & (df['timeslot'] == j)].position_count.sum(),i, j] for i in range(df['cluster'].min(),df['cluster'].max() + 1) for j in range(0,4)]
perf.sort(key=lambda x: x[0], reverse= True)
perf=np.array(perf)

#+++++++qui normalizzo ma non mi viene dioboia+++++
'''
perf_norm=perf.copy()
minact=perf[:,0].min()
maxact=perf[:,0].max()
for i in range(0,len(perf)):
    perf_norm[i,0]=(perf[i,0] - minact)/(maxact-minact)
    
'''    
best_clust= perf[:4,:]

#plotto
#REFERENCE: https://chrisalbon.com/python/matplotlib_grouped_bar_plot.html
pos = list(range(len(best_clust)))
width = 0.25
fig, ax = plt.subplots(figsize=(10,len(best_clust)))

#crea bar per le activity e per le positionn
plt.bar(pos,best_clust[:,0],width,alpha=0.5, color='#abcdf1', label='activity' )
plt.bar([p + width for p in pos],best_clust[:,1],width,alpha=0.5, color='#fff532', label='positioncount' )

ax.set_ylabel('count in millions')
ax.set_xlabel('clusters')
ax.set_xticks([p + 0.5 * width for p in pos]) #da mettere a posto
ax.set_xticklabels(best_clust[:,2])
# Adding the legend and showing the plot
plt.legend(['activity', 'position_count'], loc='upper left')
plt.grid()
plt.show()




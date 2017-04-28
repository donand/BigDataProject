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
df=pd.read_csv("../Data/fuorisalone_2016_anonymous_appdata/anon_db/events_full_coloumn.csv", encoding= 'latin1')
tmp=[x for x in range(9, 30)]
df.drop(df.columns[tmp], axis=1, inplace=True)
df.drop(['latitude','longitude','cell'],axis=1, inplace=True)

#trovo i 4 cluster più grandi
perf=[[df[(df['cluster']==i) & (df['timeslot'] == j)].activity.sum(),df[(df['cluster']==i) & (df['timeslot'] == j)].position_count.sum(),i, j] for i in range(df['cluster'].min(),df['cluster'].max() + 1) for j in range(0,4)]

perf.sort(key=lambda x: x[0], reverse= True)
perf= pd.DataFrame(np.array(perf), columns = ['activities', 'positions', 'cluster', 'timeslot'])

#+++++++qui normalizzo ma non mi viene dioboia+++++
'''
perf_norm=perf.copy()
minact=perf[:,0].min()
maxact=perf[:,0].max()
for i in range(0,len(perf)):
    perf_norm[i,0]=(perf[i,0] - minact)/(maxact-minact)
    
'''    
#best_clust= perf[:4,:]
perf = perf[(perf.cluster == 0) | (perf.cluster == 3) | (perf.cluster == 7) | (perf.cluster == -7)]



# PLOT CON CLUSTER SULLE ASCISSE
best_clust = perf.groupby('cluster').sum().drop('timeslot', axis = 1)
best_clust['cluster'] = best_clust.index
# normalizzo
max_act = max(best_clust.activities)
max_pos = max(best_clust.positions)
best_clust.activities = best_clust.activities.map(lambda x: x / max_act)
best_clust.positions = best_clust.positions.map(lambda x: x / max_pos)
best_clust = best_clust.as_matrix()

font_size = 26

#plotto
#REFERENCE: https://chrisalbon.com/python/matplotlib_grouped_bar_plot.html
pos = list(range(len(best_clust)))
width = 0.25
fig, ax = plt.subplots(figsize=(10,len(best_clust)))
plt.rcParams.update({'font.size': font_size})
#crea bar per le activity e per le positionn
plt.bar(pos,best_clust[:,0],width,alpha=0.5, color='#abcdf1', label='activity' )
plt.bar([p + width for p in pos],best_clust[:,1],width,alpha=0.5, color='#fff532', label='positioncount' )
ax.set_ylabel('count in millions')
ax.set_xlabel('clusters')
ax.set_xticks([p + 1 * width for p in pos]) #da mettere a posto
#ax.set_xticklabels(best_clust[:,2])
ax.set_xticklabels(['Center Outliers', 'Tortona', 'Brera', 'Lambrate'])
# Adding the legend and showing the plot
plt.legend(['activity', 'position_count'], loc='upper left')
plt.grid()

corr = np.corrcoef(best_clust[:,0], best_clust[:,1])[0,1]

fig, ax = plt.subplots(figsize=(10,len(best_clust)))
plt.plot(pos, best_clust[:,0], 'bo-' ,label = 'activity', color = 'blue', linewidth = 2)
plt.plot(pos, best_clust[:,1], 'ro-',label = 'positions', color = 'red', linewidth = 2)
ax.set_ylabel('count in millions')
ax.set_xlabel('clusters')
ax.set_xticks([-0.5] + pos + [len(pos) - 0.5]) #da mettere a posto
ax.set_yticks([i/10 for i in range(0, 13, 2)])
ax.set_xticklabels(['', 'Center Outliers', 'Tortona', 'Brera', 'Lambrate'])
# Adding the legend and showing the plot
plt.legend(['activity', 'position_count'], loc='upper left')
plt.grid()
plt.show()


# UN PLOT PER CLUSTER CON TIMESLOT SULLE ASCISSE
clust_names = {-7: 'CENTER OUTLIERS', 0:'TORTONA', 3:'BRERA', 7:'LAMBRATE'}
clusters = np.sort(perf.cluster.unique()).tolist()
for c in clusters:
    clust = perf[perf.cluster == c].sort_values(by = 'timeslot', axis = 0)
    # normalizzo
    max_act = max(clust.activities)
    max_pos = max(clust.positions)
    clust.activities = clust.activities.map(lambda x: x / max_act)
    clust.positions = clust.positions.map(lambda x: x / max_pos)
    clust = clust.as_matrix()
    
    pos = list(range(4))
    fig, ax = plt.subplots(figsize=(10,len(clust)))
    plt.rcParams.update({'font.size': font_size})
    plt.title(clust_names[c] + ', correlation: ' + str(np.corrcoef(clust[:,0], clust[:,1])[0,1]))
    plt.plot(pos, clust[:,0], 'bo-' ,label = 'activity', color = 'blue', linewidth = 2)
    plt.plot(pos, clust[:,1], 'ro-',label = 'positions', color = 'red', linewidth = 2)
    ax.set_ylabel('count in millions')
    ax.set_xlabel('Timeslots')
    ax.set_xticks([-0.5] + pos + [len(pos) - 0.5]) #da mettere a posto
    ax.set_yticks([i/10 for i in range(0, 13, 2)])
    ax.set_xticklabels(['', '0 AM - 6 AM', '6 AM - 12 AM', '12 AM - 18 PM', '18 PM - 24 PM'])
    # Adding the legend and showing the plot
    plt.legend(['activity', 'positions'], loc='upper left')
    plt.grid()

plt.show()

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 17:48:52 2017

@author: ghion
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gmplot
from sklearn.cluster import DBSCAN
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.linear_model import LassoLarsCV
from sklearn.linear_model import LassoCV

df = pd.read_csv("Prediction/events_cluster_encoded.csv", encoding ="latin1")

X = df.drop(['activity','position_count'],axis=1)
Y = df['activity']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 1024)

LLC = LassoLarsCV(normalize=False, cv= 10, n_jobs=-1)
'''
LLC.fit(X_train,y_train)
y_pred = LLC.predict(X_test)
score = LLC.score(X_test, y_test)
'''

LC = LassoCV()
'''
lm.fit(X_train,y_train)
y_pred = lm.predict(X_test)
score = lm.score(X_test, y_test)
'''
from sklearn.model_selection import cross_val_score
scores1=cross_val_score(LLC, X_train, y_train, cv=10, n_jobs=-1)
scores2=cross_val_score(LC, X_train, y_train, cv=10, n_jobs=-1)
 #print (scores)
#print ('\nmean ' + str(scores.mean())+ '+/- ' + str(scores.std()*2))

from scipy.stats import ttest_ind
#+++ se il p value è giga allora sono uguali +++
ttest_ind(scores1,scores2)

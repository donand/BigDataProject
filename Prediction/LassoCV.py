# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 18:27:30 2017

@author: Riccardo
"""

import pandas as pd
import json
from pandas.io.json import json_normalize
import gmplot
import gmaps
import numpy as np
import math

import matplotlib.pyplot as plt
from sklearn.linear_model import LassoCV



data = pd.read_csv("Prediction/events_cluster_encoded.csv",encoding="latin1")
data_PCA=pd.read_csv("Prediction/events_pca_90.csv",encoding="latin1")


lm = LassoCV()

X = data.drop(['activity','position_count'],axis=1)
Y = data['activity']

#Hold-Out Splitting
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 1024)

lm.fit(X_train,y_train)
y_pred = lm.predict(X_test)
#R2 score
score = lm.score(X_test, y_test)
print 'LassoCV HoldOut: R2 = ' + str(score)

#Cross Validation
from sklearn.model_selection import cross_val_score
lm2 = LassoCV()
scores = cross_val_score(lm2,X_train,y_train,scoring='r2',cv=10)
print 'LassoCV XVal R2 = ' + str(scores.mean()) + ' +/- ' + str(scores.std() * 2)



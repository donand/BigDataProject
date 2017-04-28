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
from OLS_and_Ridge import ridge

import matplotlib.pyplot as plt
from sklearn.linear_model import LassoCV

def get_split(dataset):
    return dataset.drop(['activity','position_count'],axis=1), dataset['activity'], dataset['position_count']


full_data = pd.read_csv("events_encoded.csv",encoding="latin1")
pca_data = pd.read_csv("events_pca_90.csv",encoding="latin1")



lm = LassoCV()
used_dataset = full_data
X, y_act, y_pos = get_split(used_dataset)


#Hold-Out Splitting
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y_act, test_size = 0.2, random_state = 1024)

lm.fit(X_train,y_train)
y_pred = lm.predict(X_test)
#R2 score
score = lm.score(X_test, y_test)
w_vec = pd.Series(lm.coef_)
lasso_sel_feat = pd.Series(X_train.columns.values)[w_vec != 0]

print 'Feature eliminated = ' + str(len(w_vec) - np.count_nonzero(w_vec))
print 'LassoCV HoldOut: R2 = ' + str(score)

#Cross Validation
from sklearn.model_selection import cross_val_score
lm2 = LassoCV()
scores = cross_val_score(lm2,X_train,y_train,scoring='r2',cv=10)

print 'LassoCV XVal R2 = ' + str(scores.mean()) + ' +/- ' + str(scores.std() * 2)

#RFE
from sklearn.feature_selection import RFECV
lm3 = LassoCV()
selector = RFECV(lm3, cv=3)
X_opt = selector.fit_transform(X_train, y_train)
rfe_score = selector.score(X_test,y_test)
#Selected Features
sel_feat = pd.Series(X_train.columns.values[selector.support_])

from scipy.stats import ttest_ind
#+++ se il p value è giga allora sono uguali +++
ttest_ind(cross_bay,cross_ridge)

cross_ridge, cross_PCA_ridge, cross_svr, cross_PCA_svr, cross_bay, cross_PCA_bay = ridge('POSITION',y_pos,y_pos_PCA)


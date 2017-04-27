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

df = pd.read_csv("Prediction/events_cluster_encoded.csv",encoding="latin1")
df_PCA=pd.read_csv("Prediction/events_pca_90.csv",encoding="latin1")

X = df.drop(['activity','position_count'],axis=1)
Y = df['position_count']

X_PCA = df_PCA.drop(['activity','position_count'],axis=1)
Y_PCA = df_PCA['position_count']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 1024)

X_train_PCA, X_test_PCA, y_train_PCA, y_test_PCA = train_test_split(X_PCA, Y_PCA, test_size = 0.2, random_state = 1024)

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

 #LassoCV e LarsLassoCV senza PCA
from sklearn.model_selection import cross_val_score
scores1=cross_val_score(LLC, X_train, y_train, cv=10, n_jobs=-1)
scores2=cross_val_score(LC, X_train, y_train, cv=10, n_jobs=-1)
print ('\nmean ' + str(scores1.mean())+ '+/- ' + str(scores1.std()*2))
print ('\nmean ' + str(scores2.mean())+ '+/- ' + str(scores2.std()*2))

LLC.fit(X_train,y_train)
wLLC=LLC.coef_
LC.fit(X_train,y_train)
wLC=LC.coef_


 #LassoCV e LarsLassoCV con PCA
scores1_PCA=cross_val_score(LLC, X_train_PCA, y_train_PCA, cv=10, n_jobs=-1)
scores2_PCA=cross_val_score(LC, X_train_PCA, y_train_PCA, cv=10, n_jobs=-1)
print ('\nmean ' + str(scores1_PCA.mean())+ '+/- ' + str(scores1_PCA.std()*2))
print ('\nmean ' + str(scores2_PCA.mean())+ '+/- ' + str(scores2_PCA.std()*2))

LLC.fit(X_train_PCA,y_train_PCA)
wLLCpca=LLC.coef_
LC.fit(X_train_PCA,y_train_PCA)
wLCpca=LLC.coef_


#Ora FaI ELASTIC NET

from scipy.stats import ttest_ind
#+++ se il p value è giga allora sono uguali +++
ttest_ind(scores1,scores2)


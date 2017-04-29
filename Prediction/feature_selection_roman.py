# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVR
from sklearn.linear_model import BayesianRidge
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import RFECV
from scipy.stats import ttest_ind

def get_split(df):
    return df.drop(['activity', 'position_count'], axis = 1), df['activity'], df['position_count']


df = pd.read_csv('events_encoded.csv', encoding = 'latin1')
df_pca = pd.read_csv('events_pca_90.csv', encoding = 'latin1')

x, y_act, y_pos = get_split(df)
x_PCA, y_act_PCA, y_pos_PCA = get_split(df_pca)


def feature_selection(pred_string, y, y_PCA):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 1024)
    x_train_PCA, x_test_PCA, y_train_PCA, y_test_PCA = train_test_split(x_PCA, y_PCA, test_size = 0.2, random_state = 1024)
    
    print('\n##### ' + pred_string + ' #####\n')
    
    
    # Ridge
    ridge = RidgeCV()
    selector = RFECV(ridge, cv=3)
    x_opt = selector.fit_transform(x_train, y_train)
    cross_full = cross_val_score(ridge, x_train, y_train, cv = 10)
    cross_new = cross_val_score(ridge, x_opt, y_train, cv = 10)
    res = pd.Series(x_train.columns.values[selector.support_])
    
    x_PCA_opt = selector.fit_transform(x_train_PCA, y_train)
    cross_PCA_full = cross_val_score(ridge, x_train_PCA, y_train_PCA, cv = 10)
    cross_PCA_new = cross_val_score(ridge, x_PCA_opt, y_train_PCA, cv = 10)
    print('\nRIDGE\n------')
    print('error not PCA, full dataset: ' + str(cross_full.mean()) + ' +/- ' + str(cross_full.std()*2))
    print('error not PCA, new features: ' + str(cross_new.mean()) + ' +/- ' + str(cross_new.std()*2))
    print('t-test: ' + str(ttest_ind(cross_full, cross_new)))
    #print(res)
    print('\n')
    print('error PCA, full dataset: ' + str(cross_PCA_full.mean()) + ' +/- ' + str(cross_PCA_full.std()*2))
    print('error PCA: new features' + str(cross_PCA_new.mean()) + ' +/- ' + str(cross_PCA_new.std()*2))
    print('t-test: ' + str(ttest_ind(cross_PCA_full, cross_PCA_new)))

    
    # Bayesian Ridge
    bay_ridge = BayesianRidge()
    selector = RFECV(ridge, cv=3)
    x_opt = selector.fit_transform(x_train, y_train)
    cross_full = cross_val_score(bay_ridge, x_train, y_train, cv = 10)
    cross_new = cross_val_score(bay_ridge, x_opt, y_train, cv = 10)
    res = pd.Series(x_train.columns.values[selector.support_])
    
    x_PCA_opt = selector.fit_transform(x_train_PCA, y_train)
    cross_PCA_full = cross_val_score(bay_ridge, x_train_PCA, y_train_PCA, cv = 10)
    cross_PCA_new = cross_val_score(bay_ridge, x_PCA_opt, y_train_PCA, cv = 10)
    print('\nBAYESIAN RIDGE\n------')
    print('error not PCA, full dataset: ' + str(cross_full.mean()) + ' +/- ' + str(cross_full.std()*2))
    print('error not PCA, new features: ' + str(cross_new.mean()) + ' +/- ' + str(cross_new.std()*2))
    print('t-test: ' + str(ttest_ind(cross_full, cross_new)))
    #print(res)
    print('\n')
    print('error PCA, full dataset: ' + str(cross_PCA_full.mean()) + ' +/- ' + str(cross_PCA_full.std()*2))
    print('error PCA: new features' + str(cross_PCA_new.mean()) + ' +/- ' + str(cross_PCA_new.std()*2))
    print('t-test: ' + str(ttest_ind(cross_PCA_full, cross_PCA_new)))
    
    
    # Random Forest
    rf = RandomForestRegressor()
    selector = RFECV(ridge, cv=3)
    x_opt = selector.fit_transform(x_train, y_train)
    x_test_opt = selector.transform(x_test)
    cross_full = cross_val_score(rf, x_train, y_train, cv = 10)
    cross_new = cross_val_score(rf, x_opt, y_train, cv = 10)
    res = pd.Series(x_train.columns.values[selector.support_])
    
    x_PCA_opt = selector.fit_transform(x_train_PCA, y_train)
    cross_PCA_full = cross_val_score(rf, x_train_PCA, y_train_PCA, cv = 10)
    cross_PCA_new = cross_val_score(rf, x_PCA_opt, y_train_PCA, cv = 10)
    print('\nRANDOM FOREST\n------')
    print('error not PCA, full dataset: ' + str(cross_full.mean()) + ' +/- ' + str(cross_full.std()*2))
    print('error not PCA, new features: ' + str(cross_new.mean()) + ' +/- ' + str(cross_new.std()*2))
    rf.fit(x_opt, y_train)
    print('test error new features: ' + str(rf.score(x_test_opt, y_test)))
    print('t-test: ' + str(ttest_ind(cross_full, cross_new)))
    #print(res)
    print('\n')
    print('error PCA, full dataset: ' + str(cross_PCA_full.mean()) + ' +/- ' + str(cross_PCA_full.std()*2))
    print('error PCA: new features: ' + str(cross_PCA_new.mean()) + ' +/- ' + str(cross_PCA_new.std()*2))
    print('t-test: ' + str(ttest_ind(cross_PCA_full, cross_PCA_new)))
    
    return res

sel_features_act = feature_selection('ACTIVITIES', y_act, y_act_PCA)
sel_features_pos = feature_selection('POSITIONS', y_pos, y_pos_PCA)
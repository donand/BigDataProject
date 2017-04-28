import pandas as pd
import numpy as np
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVR
from sklearn.linear_model import BayesianRidge
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor

def get_split(df):
    return df.drop(['activity', 'position_count'], axis = 1), df['activity'], df['position_count']


df = pd.read_csv('events_encoded.csv', encoding = 'latin1')
df_pca = pd.read_csv('events_pca_90.csv', encoding = 'latin1')

x, y_act, y_pos = get_split(df)
x_PCA, y_act_PCA, y_pos_PCA = get_split(df_pca)

def ridge(pred_string, y, y_PCA):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 1024)
    x_train_PCA, x_test_PCA, y_train_PCA, y_test_PCA = train_test_split(x_PCA, y_PCA, test_size = 0.2, random_state = 1024)
    
    print('\n##### ' + pred_string + ' #####\n')
    
    # Ridge
    ridge = RidgeCV()
    cross_ridge = cross_val_score(ridge, x_train, y_train, cv = 10)
    cross_PCA_ridge = cross_val_score(ridge, x_train_PCA, y_train_PCA, cv = 10)
    print('RIDGE\n------')
    print('error not PCA: ' + str(cross_ridge.mean()) + ' +/- ' + str(cross_ridge.std()*2))
    print('error PCA: ' + str(cross_PCA_ridge.mean()) + ' +/- ' + str(cross_PCA_ridge.std()*2))
    
    '''
    # SVR
    svr = SVR()
    cross_svr = cross_val_score(svr, x_train, y_train, cv = 10)
    cross_PCA_svr = cross_val_score(svr, x_train_PCA, y_train_PCA, cv = 10)
    print('\nSVR\n------')
    print('error not PCA: ' + str(cross_svr.mean()) + ' +/- ' + str(cross_svr.std()*2))
    print('error PCA: ' + str(cross_PCA_svr.mean()) + ' +/- ' + str(cross_PCA_svr.std()*2))
    '''
    
    # Bayesian Ridge
    bay_ridge = BayesianRidge()
    cross_bay = cross_val_score(bay_ridge, x_train, y_train, cv = 10)
    cross_PCA_bay = cross_val_score(bay_ridge, x_train_PCA, y_train_PCA, cv = 10)
    print('\nBAYESIAN RIDGE\n------')
    print('error not PCA: ' + str(cross_bay.mean()) + ' +/- ' + str(cross_bay.std()*2))
    print('error PCA: ' + str(cross_PCA_bay.mean()) + ' +/- ' + str(cross_PCA_bay.std()*2))
    
    
    # Random Forest
    rf = RandomForestRegressor()
    cross_rf = cross_val_score(rf, x_train, y_train, cv = 10)
    cross_PCA_rf = cross_val_score(rf, x_train_PCA, y_train_PCA, cv = 10)
    print('\nRANDOM FOREST\n------')
    print('error not PCA: ' + str(cross_rf.mean()) + ' +/- ' + str(cross_rf.std()*2))
    print('error PCA: ' + str(cross_PCA_rf.mean()) + ' +/- ' + str(cross_PCA_rf.std()*2))
    '''
    # MLP
    mlp = MLPRegressor(max_iter = 1000)
    cross = cross_val_score(mlp, x_train, y_train, cv = 10)
    cross_PCA = cross_val_score(mlp, x_train_PCA, y_train_PCA, cv = 10)
    print('\nMLP\n------')
    print('error not PCA: ' + str(cross.mean()) + ' +/- ' + str(cross.std()*2))
    print('error PCA: ' + str(cross_PCA.mean()) + ' +/- ' + str(cross_PCA.std()*2))
    '''
    return cross_ridge, cross_PCA_ridge, cross_svr, cross_PCA_svr, cross_bay, cross_PCA_bay
    
#ridge('ACTIVITIES', y_act, y_act_PCA)
#ridge('POSITIONS', y_pos, y_pos_PCA)

from sklearn.feature_selection import mutual_info_regression
feat = mutual_info_regression(x, y_pos, random_state = 1024)
feat = pd.Series(feat)
slected_cols = pd.Series(x.columns.values)[feat > 0.07]
#p = pd.Series(feat[1])
#print(p[p < 0.05].count())

feat_PCA = mutual_info_regression(x_PCA, y_act_PCA, random_state = 1024)
f = np.sort(feat_PCA)
#p_PCA = pd.Series(feat_PCA[1])
#print(p_PCA[p_PCA < 0.05].count())
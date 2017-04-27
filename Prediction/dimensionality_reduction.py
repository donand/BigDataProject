import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv('Prediction/events_ready_to_pre.csv', encoding = 'latin1')

df.cluster = df.cluster.map(lambda x: x - min(df.cluster))

# OneHotEncoder of the clusters
one_hot_enc = OneHotEncoder()
a = one_hot_enc.fit_transform(df.cluster.reshape(-1, 1)).toarray()
a = pd.DataFrame(a)
df = pd.concat([df, a], axis = 1)
df.drop('cluster', axis = 1, inplace = True)
# drop cluster 0, the outliers of the outliers
df.drop(0, axis = 1, inplace = True)

# OneHotEncoder of the timeslots, and drop timeslot_0
a = one_hot_enc.fit_transform(df.timeslot.reshape(-1, 1)).toarray()
a = pd.DataFrame(a, columns = ['timeslot_0', 'timeslot_1', 'timeslot_2', 'timeslot_3'])
df = pd.concat([df, a], axis = 1)
df.drop('timeslot', axis = 1, inplace = True)
df.drop('timeslot_0', axis = 1, inplace = True)

# dump to csv ready dataset
df.to_csv('Prediction/events_encoded.csv', index = False)


y_phone = df['activity']
y_position = df['position_count']
x = df.drop(['activity', 'position_count'], axis = 1)

# PCA dimensionality reduction
pca = PCA(n_components = 0.9, svd_solver = 'full')
pca.fit(x)

variance_ratios = pca.explained_variance_ratio_
components = pca.components_

x_reduced = pd.DataFrame(np.dot(x, np.transpose(components)))
df_reduced = pd.concat([x_reduced, y_position, y_phone], axis = 1)

df_reduced.to_csv('Prediction/events_pca_90.csv', index = False)
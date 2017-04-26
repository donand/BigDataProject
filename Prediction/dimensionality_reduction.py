import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv('Prediction/events_ready_to_pre.csv', encoding = 'latin1')

df.cluster = df.cluster.map(lambda x: x - min(df.cluster))

one_hot_enc = OneHotEncoder()
a = one_hot_enc.fit_transform(df.cluster.reshape(-1, 1)).toarray()

a = pd.DataFrame(a)
df = pd.concat([df, a], axis = 1)

# drop cluster 0, the outliers of the outliers
df.drop(0, axis = 1, inplace = True)
df.drop('cluster', axis = 1, inplace = True)

df.to_csv('Prediction/events_cluster_encoded.csv', index = False)
from sklearn.neighbors import NearestNeighbors as nn
import numpy as np
from sklearn.externals.joblib import dump
data = np.load('findata.npy')
nbrs = nn(n_neighbors=2).fit(data)
dump(nbrs, 'nbrs.joblib')
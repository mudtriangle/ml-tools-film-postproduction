from scipy.cluster.vq import kmeans
import pickle
import pandas as pd

with open('../test_data/shots.pkl', 'rb') as f:
    shots = pickle.load(f)

shots = pd.DataFrame(shots)
shots = shots.to_numpy()[:, :-2]

centroids = kmeans(shots, 5)[0]

with open('../test_data/centroids.pkl', 'wb') as f:
    pickle.dump(centroids, f)

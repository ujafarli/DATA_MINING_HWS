import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from copy import deepcopy

# Reading csv dataset as it does not have header, and separated by names
wine = pd.read_csv("wine.data", names = ["Class", 
                                         "Alcohol",
                                         "Malic acid",
                                         "Ash",
                                         "Alcalinity of ash",
                                         "Magnesium",
                                         "Total phenols",
                                         "Flavanoids",
                                         "Nonflavanoid phenols",
                                         "Proanthocyanins",
                                         "Color intensity",
                                         "Hue",
                                         "OD280/OD315 of diluted wines",
                                         "Proline"])


wine.Class = wine.Class - 1

# K-means from scratch 
X = wine.iloc[:, [12, 1]].values 

data = pd.DataFrame(X)

val1 = data[0].values
val2 = data[1].values

#Euclidean Distance Function
def dist(x, y, ax=1):
    return np.linalg.norm(x - y, axis=ax)

# Number of clusters
k = 3

# Creating random centroids
# random x coordinates of centroids
x_coor = np.random.randint(0, np.max(X)-7, size=k)
# random y coordinates of random centroids
y_coor = np.random.randint(0, np.max(X)-7, size=k)
# Centroids
_centroid = np.array(list(zip(x_coor, y_coor)), dtype=np.float32)
print("Initial Centroids")
print(_centroid)

# Plotting actual values and the random centroids
plt.scatter(val1, val2, c='#050505', s=7)
plt.scatter(x_coor, y_coor, marker='x', s=200, c='g')

# To store the old value of centroids when it updates
my_centroid = np.zeros(_centroid.shape)
clusters = np.zeros(len(X))

# Error function  - Distance between updated and old centroids
error = dist(_centroid, my_centroid, None)

# Loop will run till the error becomes zero
while error != 0:
    # Assigning each value to its closest cluster
    for i in range(len(X)):
        distances = dist(X[i], _centroid)
        cluster = np.argmin(distances)
        clusters[i] = cluster
    # Storing the old centroid values
    C_old = deepcopy(_centroid)
    # Finding the new centroids by taking the average value
    for i in range(k):
        points = [X[j] for j in range(len(X)) if clusters[j] == i]
        _centroid[i] = np.mean(points, axis=0)
    error = dist(_centroid, my_centroid, None)

colors = ['red','blue','green']
fig, ax = plt.subplots()
for i in range(k):
        points = np.array([X[j] for j in range(len(X)) if clusters[j] == i])
        ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
ax.scatter(_centroid[:, 0], _centroid[:, 1], marker='*', s=200, c='#050505')

           
# K means with scikit-learn libraries
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);














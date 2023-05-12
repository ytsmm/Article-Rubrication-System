import numpy as np
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans, AgglomerativeClustering


def clusterization(X, clusterType):
    k = [], clResult = [], scores = [], quantity = []

    for i in range(2, 10):
        if clusterType == 'Hierarchial':
            clResult.append(AgglomerativeClustering(n_clusters=i))
        elif clusterType == 'K-Means':
            clResult.append(KMeans(n_clusters=i))
        k.append(i)

    for i in range(8):
        scores.append(silhouette_score(X, clResult[i].fit_predict(X)))

    optimalScore = k[np.argmax(scores)]
    if clusterType == 'Hierarchial':
        model = AgglomerativeClustering(metric='euclidean', n_clusters=optimalScore, linkage='ward').fit(X)
    elif clusterType == 'K-Means':
        model = KMeans(n_clusters=optimalScore).fit(X)

    labels = model.labels_
    
    for i in range(optimalScore):
        count = 0
        for j in labels:
            if j == i:
                count += 1
        quantity.append(count)
    return labels, optimalScore, quantity

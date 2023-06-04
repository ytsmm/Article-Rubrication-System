import numpy as np
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans, AgglomerativeClustering
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc


# Функция выполняет кластеризацию числовых данных
# vectors - массив pd.DataFrame() векторных представлений статей
# clusterType – строковый параметр, содержащий тип кластеризации
# labels – целочисленный массив с номерами кластеров
# n – целочисленный параметр, соответствующий числу кластеров
# size – целочисленный массив с количеством статей в каждом кластере
def clusterization(vectors, clusterType):
    if clusterType == 'Hierarchical clustering':
        labels, n, size = hierarchial(vectors)
        return labels, n, size
    elif clusterType == 'K-Means clustering':
        labels, n, size = kmeans(vectors)
        return labels, n, size


def kmeans(X):
    k = []
    clResult = []

    for i in range(2, 10):
        clResult.append(KMeans(n_clusters=i))
        k.append(i)

    scores = [silhouette_score(X, clResult[i].fit_predict(X)) for i in range(8)]
    optimalScore = k[np.argmax(scores)]
    model = KMeans(n_clusters=optimalScore).fit(X)
    labels = model.labels_
    number = [sum([1 for j in labels if j == i]) for i in range(optimalScore)]

    plt.plot(k, scores, marker='o')
    plt.xlabel('Number of clusters', fontsize=16)
    plt.ylabel('Silhouette coefficient', fontsize=16)
    plt.show()

    plt.figure(figsize=(6, 6))
    plt.scatter(X['X'], X['Y'], c=clResult[optimalScore - 2].fit_predict(X), cmap='rainbow')
    plt.show()

    return labels, optimalScore, number


def hierarchial(X):
    k = []
    clResult = []

    for i in range(2, 10):
        clResult.append(AgglomerativeClustering(n_clusters=i))
        k.append(i)

    scores = [silhouette_score(X, clResult[i].fit_predict(X)) for i in range(8)]
    optimalScore = k[np.argmax(scores)]
    model = AgglomerativeClustering(metric='euclidean', n_clusters=optimalScore, linkage='ward').fit(X)
    labels = model.labels_
    number = [sum([1 for j in labels if j == i]) for i in range(optimalScore)]

    plt.plot(k, scores, marker='o')
    plt.xlabel('Number of clusters', fontsize=16)
    plt.ylabel('Silhouette coefficient', fontsize=16)
    plt.show()
    Dendrogram = shc.dendrogram((shc.linkage(X, method='ward')), leaf_font_size=6)
    plt.show()
    plt.figure(figsize=(6, 6))
    plt.scatter(X['X'], X['Y'], c=clResult[optimalScore - 2].fit_predict(X), cmap='rainbow')
    plt.show()

    return labels, optimalScore, number

import numpy as np
import pandas as pd
import gensim.downloader as api
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, normalize

corpus = api.load("glove-wiki-gigaword-50")


# Функция выполняет векторизацию текстовых данных
# data - строковый массив предобработанных данных
# vectorData – массив pd.DataFrame() векторных представлений статей
def vectorizing(data):
    features = []
    for tokens in data:
        zero_vector = np.zeros(corpus.vector_size)
        vectors = []

        for token in tokens:
            if token in corpus:
                try:
                    vectors.append(corpus[token])
                except KeyError:
                    continue

        if vectors:
            vectors = np.asarray(vectors)
            avg_vec = vectors.mean(axis=0)
            features.append(avg_vec)

        else:
            features.append(zero_vector)

    vectorData = pcaModule(features)

    return vectorData


def pcaModule(X):
    X_scaled = StandardScaler().fit_transform(X)
    X_normalized = normalize(X_scaled)
    X_normalized = pd.DataFrame(X_normalized)
    X_principal = PCA(n_components=2).fit_transform(X_normalized)
    X_principal = pd.DataFrame(X_principal)
    X_principal.columns = ['X', 'Y']
    return X_principal

from gensim.models import Word2Vec
import nltk
import numpy as np
from sklearn.cluster import KMeans
from sklearn import cluster 
from sklearn import metrics
from sklearn.decomposition import _pca
from scipy.cluster import hierarchy
from sklearn.cluster import AgglomerativeClustering

def create_model(arr_sent):
    return Word2Vec(arr_sent, size=50, min_count=1, sg=1)

def vectorizer(sent, m):
    vec = []
    numw = 0

    for w in sent:
        try:
            if numw == 0:
                vec = m[w]
            else:
                vec = np.add(vsc, m[w])
            numw += 1
        except:
            pass

        return np.asarray(vec) / numw

def another(sent):
    l = []
    for i in sent:
        l.append(vectorizer(i,m))
    X=np.array(l)
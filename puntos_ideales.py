# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from socal_jaccard import socal_jaccard
from coorp3c import coorp3c

def puntos_ideales(X, x):
    n, p = X.shape

    a = np.dot(X, x)
    d = np.dot((np.ones((n, p)) - X), (np.ones((1, p)) - x).T)
    s = (a + d) / p
    d = 2 * (np.ones((n, 1)) - s[0])
    st = s.T
    dt = d.T

    # Después de usar la función coorp
    # Y es la matriz de coordenadas
    _, _, D2_S, _ = socal_jaccard(X)
    Y, vaps, percent, acum = coorp3c(D2_S)
    B = np.dot(Y, Y.T)
    b = np.diag(B)
    n, p = Y.shape
    Lambda = np.diag(vaps[:p])

    ddd = np.dot(np.linalg.inv(Lambda), (Y.T))

    y =  np.dot(np.dot(np.linalg.inv(Lambda), (Y.T)), (b - d[0]) );
    yt = y.T

    return yt

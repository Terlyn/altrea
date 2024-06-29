import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scripts import non2euclid
from scipy.linalg import svd


def coorp3c(D):
    n, _ = D.shape
    H = np.eye(n) - np.ones((n, n)) / n
    B = -np.dot(np.dot(H, D), H) / 2
    L, V = np.linalg.eig(B)
    m = np.min(L)

    epsilon = 1e-6
    if np.abs(m) < epsilon:
        D1 = non2euclid(D)
        B = -np.dot(np.dot(H, D1), H) / 2

    T, lambda_vals, V = svd(B)
    vaps = lambda_vals
    lambda_vals = np.diag(lambda_vals)
    j = 0

    while vaps[j] > epsilon:
        T1 = T[:, :j+1]
        X = np.dot(T1, np.sqrt(lambda_vals[:j+1, :j+1]))
        j = min(j + 1, n)

    percent = vaps / np.sum(vaps) * 100
    acum = np.zeros(n)
    for i in range(n):
        acum[i] = np.sum(percent[:i+1])

    return X, vaps, percent, acum



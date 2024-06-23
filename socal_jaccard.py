import numpy as np

def socal_jaccard(X):
    X = X.astype(float)  # Convertir los datos a tipo de dato float
    n, p = X.shape

    J = np.ones((n, p))
    a = np.dot(X, X.T)
    d = np.dot((J - X), (J - X).T)

    S_Sokal = (a + d) / p
    S_Jaccard = a / (p * np.ones((n, n)) - d)

    J = np.ones((n, n))

    D2_S = 2 * (J - S_Sokal)
    D2_J = 1 * (J - S_Jaccard)

    return S_Sokal, S_Jaccard, D2_S, D2_J

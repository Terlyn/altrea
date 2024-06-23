# -- coding: utf-8 --
import numpy as np
import pandas as pd
import openpyxl
from socal_jaccard import socal_jaccard
from coorp3c import coorp3c
from puntos_ideales import puntos_ideales

data_ideal = [
    [  0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,
      1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
      0, 1, 1, 0, 1, 0, 0, 0
    ],
    [  0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1,
      0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0,
      0, 0, 0, 0, 0, 0, 1, 0
    ],
    [  0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0,
      0, 0, 0, 0, 0, 1, 0, 1
    ],
    [ 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
      0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1,
      1, 0, 0, 1, 0, 0, 0, 0
    ]
]

def es_bidimensional(arreglo):
    # Verificar si todos los elementos son listas
    return all(isinstance(sub_arreglo, list) for sub_arreglo in arreglo)

def estilosfil_form( data_1 ):
  data__1 = np.array( data_ideal )
  
  if ( es_bidimensional(data_1) ):
    data__2 = np.array( data_1 )
  else:
    data__2 = np.array( [data_1] )

  # Calcular las distancias
  S_Sokal, S_Jaccard, D2_S, D2_J = socal_jaccard( data__1 )

  # Calcular las coordenadas principales
  R, vaps, percent, acum = coorp3c(D2_S)

  # Calcular los puntos ideales
  X = data__1
  x = data__2
  m, n = x.shape
  r = np.zeros((m, 3))
  yt = np.zeros((8, 3))

  for i in range(m):
    yt[i] = puntos_ideales(X, x[i, :])
    r[i, 0:3] = yt[i:i+1][0]

  p, q = r.shape
  n, m = R.shape

  normat = np.zeros((p, n))
  for j in range(p):
    for i in range(n):
      normat[j, i] = np.linalg.norm(R[i, :] - r[j, :])

  return normat, R, yt


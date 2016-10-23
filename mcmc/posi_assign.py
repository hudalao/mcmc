#the class of the vertex

#N: the number of the vertexs
#M: the number of edges
#Dx: the dimension of the 2D grid along x direction
#Dy: the dimension of the 2D grid along y direction
#Lx: the length of 2D grid along x direction
#Ly: the length of 2D grid along y direction
#Req1: N is equal or smaller than D^2
import sys
sys.path.append('../mcmc')

import numpy as np

def posi_assign(N, Dx, Dy, Lx, Ly):
    nx, ny = (Dx, Dy)
    x = np.linspace(0, Lx, Dx)
    y = np.linspace(0, Ly, Dy)
    #picking the position (x, y) randomly for N vertexs
    repeat = True
    while repeat == True:
        x_ind = np.random.randint(0, Dx, size = N)
        y_ind = np.random.randint(0, Dy, size = N)
        x_pick = np.zeros(N)
        y_pick = np.zeros(N)
        for ii in range(N):
            x_pick[ii] = x[x_ind[ii]]
            y_pick[ii] = y[y_ind[ii]]
        posi = np.stack((x_pick, y_pick), axis=-1)
        posi_ref = np.stack((x_ind, y_ind), axis=-1)
        posi_uni = np.vstack({tuple(row) for row in posi_ref})
        if np.shape(posi_ref) == np.shape(posi_uni):
            repeat = False
    return posi

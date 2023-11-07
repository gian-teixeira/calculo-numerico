import matplotlib.pyplot as plt
import numpy as np

P = list()
fig = plt.figure(figsize=(5,5))
plt.xlim(0,10)
plt.ylim(0,10)

def bezier():
    if len(P) < 4: return
    
    n = len(P)
    D = np.empty((n))

    for i in range(0,n):
        if i == 0: D[i] = 0
        else: D[i] = D[i-1] + np.linalg.norm(P[i] - P[i-1])

    S = np.array([d/D[-1] for d in D])
    T = np.array([S**i for i in range(0,n)]).T
    M = np.array([[1,0,0,0],
                  [-3,3,0,0],
                  [3,-6,3,0],
                  [-1,3,-3,1]])
    
    inv = lambda X : np.linalg.inv(X)
    mult = lambda X,Y : np.matmul(X,Y)
    C = mult(mult(inv(M),inv(mult(T.T,T))),mult(T.T,P))

    for t in np.arange(0,1,0.005):
        tm = np.array([1,t,t**2,t**3])
        p = mult(mult(tm,M),C)
        plt.plot(p[0],p[1],'.',markersize=2,color='black')
    fig.canvas.draw()

def onclick(event):
    plt.plot(event.xdata,event.ydata,'bo')
    P.append(np.array([event.xdata,event.ydata]))
    fig.canvas.draw()
    bezier()

fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
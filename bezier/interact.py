import matplotlib.pyplot as plt
import numpy as np
from interpolation import *

POINTS = list()
POINT_SIZE = 6
POINT_DISTANCE = 0.1
SELECTED = -1
CURRENT_EVENT = 'standard'

def set_plot():
    plt.xlim((0,10))
    plt.ylim((0,10))

def draw(extra = None):
    plt.clf()
    set_plot()
    for x,y in POINTS:
        plt.plot(x,y,'bo',markersize = POINT_SIZE)
    if len(POINTS) > 2:
        path, A, B = bezier(POINTS,50)
        px, py = path[:,0], path[:,1]
        plt.plot(px, py, 'b-')
        #A,B = bezier_interpolate(POINTS)
        for i in range(len(A)):
            plt.plot([A[i][0],POINTS[i][0]], [A[i][1],POINTS[i][1]], 'b-')
            plt.plot([B[i][0],POINTS[i+1][0]], [B[i][1],POINTS[i+1][1]], 'b-')
            plt.plot(A[i][0], A[i][1], '.', color = 'black')
            plt.plot(B[i][0], B[i][1], '.', color = 'black')
    if extra: extra()
    fig.canvas.draw()

def target_point(pos):
    target = None
    min_distance = None
    for i in range(len(POINTS)):
        distance = np.linalg.norm(pos - POINTS[i])
        if distance < 2e-1: 
            if not target: 
                target = i
                min_distance = distance
            elif distance < min_distance:
                target = i
    return target

def onhover(event):
    pos = np.array([event.xdata,event.ydata])
    if not pos[0] or not pos[1]: return
    global TARGET
    global SELECTED 
    if CURRENT_EVENT == 'move':
        if TARGET != None:
            POINTS[TARGET] = pos
            draw()
    if CURRENT_EVENT == 'standard':
        TARGET = target_point(pos)
        if TARGET == None: 
            SELECTED = None
            draw()
        elif TARGET != SELECTED:
            SELECTED = TARGET
            draw(lambda : plt.plot(POINTS[TARGET][0],POINTS[TARGET][1],'ro', 
                                   markersize = 1.5*POINT_SIZE))

def onrelease(event):
    global TARGET
    global CURRENT_EVENT
    TARGET = None
    CURRENT_EVENT = 'standard'


def onclick(event):
    pos = np.array([event.xdata,event.ydata])
    target = target_point(pos)
    if target == None: 
        POINTS.append(pos)
        draw()
    else: 
        global TARGET
        global CURRENT_EVENT
        CURRENT_EVENT = 'move'
        TARGET = target
        draw()

fig = plt.figure(figsize=(5,5))
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('button_release_event', onrelease)
fig.canvas.mpl_connect('motion_notify_event', onhover)

set_plot()
plt.show()
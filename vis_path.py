'''
Created on 2012-04-26

@author: Sebastien Ouellet sebouel@gmail.com
'''
import landmark_map
import pickle
from matplotlib import pyplot

def visualize_map(map=None):
    if map==None:
        map = landmark_map.Map()
    figure = pyplot.figure()
    ax = figure.add_subplot(111)
    ax.axis((0, map.width, 0, map.height))
    for landmark in map.landmarks:
        #ax.plot((landmark.location1[0], landmark.location2[0]),(landmark.location1[1], landmark.location2[1]), landmark.color[0]+landmark.marker)
        for x in landmark.points[0]:
            for y in landmark.points[1]:
                ax.plot(x,y, landmark.color[0]+landmark.marker)
    return figure

def plot_scores():
    from matplotlib import pylab
    import numpy
    savedsco = open("savedsco","r")
    scores = pickle.load(savedsco)
    scores[0] = 0
    savedsco.close()
    pylab.clf()
    figure = pylab.figure()
    pylab.plot(scores)
    x = numpy.arange(len(scores))
    scores = numpy.array(scores)
    m,b = pylab.polyfit(x,scores,1)
    print m
    #pylab.plot(x, m*x+b)
    pylab.savefig("averagescores.png")

def plot_pheromones():
    from matplotlib import cm
    from matplotlib import colors
    import numpy
    sp = open("savedphe","r")
    pheromones = pickle.load(sp)
    sp.close()
    display = [[-1 for y in xrange(0,100)] for x in xrange(0,100)]
    for x in xrange(len(pheromones)):
        for y in xrange(len(pheromones[0])):
            display[x*5][y*5] = pheromones[x][y]
    pyplot.imsave("pheromones.png", numpy.array(display), cmap=cm.hot)

def plot_route():
    savedmap = open("savedmap","r")
    #savedant = open("antpath","r")
    savedpath = open("savedpath","r")
    map = pickle.load(savedmap)
    history = pickle.load(savedpath)
    #ant = pickle.load(savedant)
    savedmap.close()
    #savedant.close()
    savedpath.close()
    figure = visualize_map(map)
    x = []
    y = []
    #x1 = []
    #y1 = []
    for step in history:
        if step == None:
            break
        x.append(step[0])
        y.append(step[1])
    #for step in ant:
    #    x1.append(step[0]*5)
    #    y1.append(step[1]*5)
    pyplot.plot(x,y)
    #pyplot.plot(x1,y1)
    print len(history)
    pyplot.savefig("geneticpath.png")
    
plot_route()
#plot_pheromones()
#plot_scores()

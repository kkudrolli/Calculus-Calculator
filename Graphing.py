#Kais Kudrolli, kkudroll
#15-112, Section C, Term Project
#This file handles all the graphing of functions

import matplotlib.pyplot as plt

class Graph(object):
    #class variable annotating axes
    ax = None
    
    def __init__(self, xValues, yValues):
        #numpy arrays of the x and y coordinates
        self.xValues = xValues
        self.yValues = yValues
    
    def getXYs(self, text):
        #gets xy coordinates of annotation and its text
        index = 0
        if(text == "f(x)"):
            index = len(self.xValues)/2
        elif(text == "f'(x)"):
            index = len(self.xValues)/4
        else:
            index = 3*len(self.xValues)/4
        #set xy
        x = self.xValues[index]
        y = self.yValues[index]
        #set xyText
        offset = 50
        xText = x + offset
        yText = y
        
        return ((x,y), (xText,yText))
        
    def annotateGraph(self, text):
        #marks the integral, derivative or function with an annotation
        (xy,xyText) = self.getXYs(text)
        Graph.ax.annotate(text, xy=xy,  xycoords='data',
                xytext=xyText, textcoords='offset points',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='right', verticalalignment='bottom',
                )
        
    def drawGraph(self,text,):
        #method draws a graph
        fig = plt.figure(1)
        #adds a new sublot to the annotating axes
        Graph.ax = fig.add_subplot(111)
        if((text != "") and (self.xValues != None) and (self.yValues != None)):
            self.annotateGraph(text)
        
        #checks if there are y values and plots the coordinates
        if(self.yValues != None):
            Graph.ax.plot(self.xValues,self.yValues)
            #limits the graph range from becoming too large
            if(self.yValues.max() > 100):
                Graph.ax.set_ylim(self.yValues.min(),100)
            elif(self.yValues.min() < -100):
                Graph.ax.set_ylim(-100,self.yValues.max())
        #gives the graph gridlines
        plt.grid(True)
        
        #next two segments taken from matplotlib tutorial
        #http://matplotlib.org/examples/pylab_examples/axes_props.html
        xticklines = plt.getp(plt.gca(), 'xticklines')
        yticklines = plt.getp(plt.gca(), 'yticklines')
        xticklabels = plt.getp(plt.gca(), 'xticklabels')
        yticklabels = plt.getp(plt.gca(), 'yticklabels')
        
        #sets the line width of the tick lines
        plt.setp(xticklines, 'linewidth', 3)
        plt.setp(yticklines, 'linewidth', 3)
        #makes the tick labels blue
        plt.setp(yticklabels, 'color', 'b', fontsize='medium')
        plt.setp(xticklabels, 'color', 'b', fontsize='medium')
        
        #shows the graph
        plt.show()
        
        
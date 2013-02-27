'''
Creates maps for the route generation algorithm

Created on 2012-02-21

@author: Sebastien Ouellet sebouel@gmail.com
'''
import random

####### Parameters #######

map_width = 100
map_height = 100

number_landmarks = random.choice(range(25,30))

#sizes = range(1,11)
#heights = range(1,11)
sizes = random.gauss(5,2)
heights = random.gauss(5,2)
colors = ["green","blue","yellow","red"]
shapes = ["tree", "cabin", "pond", "rock"]
estimated_heights = ["short", "average", "tall"]
estimated_sizes = ["small", "medium", "large"]

##########################

class Map:
    def __init__(self, width=map_width, height=map_height, number=number_landmarks ):
        self.width = width
        self.height = height
        self.landmarks = [Landmark() for _ in xrange(number)]
        for landmark in self.landmarks:
            landmark.limit()
            landmark.fill()

class Landmark:
    def __init__(self):
        self.location1 = (random.randint(0,map_width-10), random.randint(0,map_height-10))
        self.color = random.choice(colors)
        self.shape = random.choice(shapes)
        #self.height = random.choice(heights)
        #self.size = random.choice(sizes)
        self.height = random.gauss(5,2)
        self.size = random.gauss(5,2)
        self.points = [[],[]]
        self.marker = None
        self.location2 = None
        self.center = [0,0]
        self.estimated_size = None
        self.estimated_height = None
    
    def limit(self):
        if self.height < 1:
            self.height = 1
        if self.size < 1:
            self.size = 1
        if self.shape == "pond":
            self.height = 1
        #if self.shape == "tree":
        #    self.location2 = (self.location1[0]+1, self.location1[1]+1)
        #else:
        self.location2 = (self.location1[0]+self.size, self.location1[1]+self.size)
        self.center[0] = self.location1[0]+self.size/2.0
        self.center[1] = self.location1[1]+self.size/2.0
    
    def fill(self):
        if self.shape == "pond":
            self.marker = "o"
        if self.shape == "tree":
            self.marker = "^"
        if self.shape == "cabin":
            self.marker = "s"
        if self.shape == "rock":
            self.marker = "D"
        self.points[0] = range(self.location1[0], int(round(self.location2[0])))
        self.points[1] = range(self.location1[1], int(round(self.location2[1]))) 

def translate_to_landmark(color,size,height,shape):
    landmark = Landmark()
    landmark.color = color
    landmark.shape = shape
    landmark.estimated_height = height
    landmark.estimated_size = size
    return landmark

def assess_landmarks(landmarks):
        length = len(landmarks)
        sizes = sorted(landmarks, key=lambda x: x.size)
        heights = sorted(landmarks, key=lambda x: x.height)
        first = round(length/3.0)
        second = first*2
        for i in xrange(length):
            if i < first:
                sizes[i].estimated_size = "small"
                heights[i].estimated_height = "short"
            elif i < second:
                sizes[i].estimated_size = "medium"
                heights[i].estimated_height = "average"
            else:
                sizes[i].estimated_size = "large"
                heights[i].estimated_height = "tall"    
        
        
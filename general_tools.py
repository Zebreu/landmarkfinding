'''
Created on 2012-04-24

@author: Sebastien Ouellet sebouel@gmail.com
'''
import math

def turn_vector(vector, orientation):
    if orientation ==  "left":
        x = 0*vector[0]+(-1)*vector[1]
        y = 1*vector[0]+0*vector[1]
    else:
        x = 0*vector[0]+1*vector[1]
        y = (-1)*vector[0]+0*vector[1]
    return (x,y)

def rotate_vector(vector, angle):
    x = math.cos(angle)*vector[0]+(-math.sin(angle))*vector[1]
    y = math.sin(angle)*vector[0]+math.cos(angle)*vector[1]
    return (x,y)

def unitize_vector(vector):
    length = float(calculate_length(vector))
    return (vector[0]/length, vector[1]/length)

def calculate_length(vector):
    return math.sqrt(vector[0]**2+vector[1]**2)

def calculate_difference(vector1, vector2):
    return (vector2[0]-vector1[0], vector2[1]-vector1[1])

def calculate_distance(vector1, vector2):
    return calculate_length(calculate_difference(vector1, vector2))

def print_landmark(landmark):
    if landmark == None:
        return ""
    else:
        #return "a {0} {1} {2} {3}".format(landmark.estimated_size, landmark.color, landmark.estimated_height, landmark.shape)        
        return "a {0} {1} {2}".format(landmark.estimated_size, landmark.color, landmark.shape)        

def print_step(step):
    print step["action"]+" "+step["orientation"]+" "+print_landmark(step["landmark"])

def print_route(route):
    for step in route:
        if step != None:
            print_step(step)
            
def compare_landmarks(landmark1, landmark2):
    if landmark1.estimated_size == landmark2.estimated_size:
        #if landmark1.estimated_height == landmark2.estimated_height:
        if landmark1.color == landmark2.color:
            if landmark1.shape == landmark2.shape:
                #print "Found one"
                return True  
    return False
    
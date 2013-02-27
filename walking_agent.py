'''
Created on 2012-04-23

@author: Sebastien Ouellet sebouel@gmail.com
'''
import math
import random

import landmark_map
import general_tools

####### Parameters #######

vision = 40
tolerance = 10

##########################    

class Agent():
    def __init__(self, map, route, destination):
        self.position = (0,0)
        self.direction = (1,0)
        self.map = map
        self.route = list(route)
        self.duration = 0
        self.destination = destination
        self.history = []
        self.desired = None
        self.near_landmarks = []
        
    def update(self,verbose=False):
        step = self.route.pop(0)
        self.interpret_step(step, verbose)
        test = self.is_final_destination()
        if test[0]:
            if verbose:
                print "Got there!"
            return ("Got there!",test[1])
        elif len(self.route)==0:
            return ("No more instructions", test[1])
        else:
            return False
    
    def interpret_step(self, step, verbose):
        desired = step["landmark"]
        if desired != None:
            self.identify_landmarks(desired)
        if step["action"] == "go":
            if step["orientation"] == "toward" or step["orientation"] == "forward":
                if self.desired != None:
                    if verbose:
                        general_tools.print_step(step)
                    self.walk()
            else:
                self.direction = general_tools.turn_vector(self.direction, step["orientation"])
                self.walk()
    
    def walk(self):
        landmarks = self.what_landmarks()
        for _ in xrange(self.duration):
            self.history.append(self.position)
            self.position = (self.position[0]+self.direction[0], self.position[1]+self.direction[1])
            if self.landmark_collision(landmarks)[0]:
                if len(self.history) < 2:
                    self.position = (0,0)
                else:
                    self.position = self.history[-2]
                break
    
    def walk_simulation(self):
        landmarks = self.what_landmarks()
        for _ in xrange(self.duration):
            self.position = (self.position[0]+self.direction[0], self.position[1]+self.direction[1])
            collision = self.landmark_collision(landmarks)
            if collision[0]:
                #print "Boom!"
                if collision[1]:
                    return True
                else:
                    return False
        return True
    
    def landmark_collision(self, landmarks):
        for landmark in landmarks:
            counter = 0
            for i in xrange(2):
                if self.position[i] > landmark.location1[i]-1 and self.position[i] < landmark.location2[i]+1:
                    counter += 1
            if counter > 1:
                if landmark == self.desired:
                    return (True,True)
                else:
                    return (True,False)
        return (False,False)
    
    def turn(self, location):
        self.direction = general_tools.calculate_difference(self.position, location)
        self.duration = int(math.floor(general_tools.calculate_length(self.direction)))
        self.direction = general_tools.unitize_vector(self.direction)
    
    def choose(self, candidates):
        if len(candidates) == 0:
            self.desired = None
        else:
            landmark = random.choice(candidates)
            #print "Yes!"
            self.turn(landmark.center)
            self.desired = landmark
    
    def is_visible(self, landmarks, landmark):
        previous_desired = self.desired
        previous_direction = self.direction
        previous_position = self.position
        self.turn(landmark.center)
        self.desired = landmark
        outcome = self.walk_simulation()
        self.direction = previous_direction
        self.position = previous_position
        self.desired = previous_desired
        return outcome
    
    def assess_landmarks(self, landmarks):
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
    
    def what_landmarks(self):
        #return self.map.landmarks
        return [landmark for landmark in self.map.landmarks if general_tools.calculate_distance(landmark.center, self.position) < vision]
        
    def identify_landmarks(self, desired, landmarks=None):
        compatible = []
        if landmarks == None:
            landmarks = self.what_landmarks()        
        #self.assess_landmarks(landmarks)
        for landmark in landmarks:
            if general_tools.compare_landmarks(desired, landmark):
                #print "Possible yes"
                if self.is_visible(landmarks, landmark):
                    compatible.append(landmark)
        self.choose(compatible)
        
    def is_final_destination(self):
        distance = general_tools.calculate_distance(self.position, self.destination)
        if distance < tolerance:
            return (True, distance)
        else:
            return (False, distance)    
    
    

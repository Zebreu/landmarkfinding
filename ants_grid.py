'''
Created on 2012-04-26

@author: Sebastien Ouellet sebouel@gmail.com
'''
import random
import pickle
import copy

import walking_agent
import landmark_map
import general_tools


####### Parameters #######

population_size = 50
iterations = 200

maximum_moves = 45
maximum_route_length = 20

pheromone_importance = 0.75
decay_rate = 0.90
pheromone_tolerance = 0.90


ant_vision = 5

many_tests = False
early_termination = True
early_number = 50

#map = landmark_map.Map()
#destination = random.choice(map.landmarks).center
somemap = open("somemap","r")
map = pickle.load(somemap)
destination = (35,80)

landmark_map.assess_landmarks(map.landmarks)
grid = [[0 for y in xrange(0,map.height,ant_vision)] for x in xrange(0,map.width,ant_vision)]
for x in xrange(len(grid)):
    for y in xrange(len(grid[0])):
        if x == 0 or x == map.width/ant_vision-1 or y == 0 or y == map.height/ant_vision-1:
            grid[x][y] = -1
        else:
            position = (x*ant_vision, y*ant_vision)
            for landmark in map.landmarks:
                counter = 0
                for i in xrange(2):
                    if position[i] > landmark.location1[i]-2 and position[i] < landmark.location2[i]+2:
                        counter += 1
                if counter > 1:
                    grid[x][y] = -1

##########################

class Ant:
    def __init__(self, internal_map, pheromones):
        self.map = internal_map
        self.pheromones = copy.deepcopy(pheromones)
        self.route = [None]*maximum_route_length
        self.route_counter = 0
        self.move_counter = 0
        self.position = (0,0)
        self.history = [None]*maximum_moves
        self.score = None
    
    def walk(self):
        for m in xrange(maximum_moves):
            self.history[m] = self.position
            self.decide_move()
            self.move_counter += 1
            self.translate_path()
            if self.route_counter == maximum_route_length:
                break
                
        self.route = [step for step in self.route if step!=None]
        self.history = [position for position in self.history if position != None]
    
    def decide_move(self):
        if self.move_counter == 0:
            possibles = [(x,y) for x in xrange(self.position[0]-1,self.position[0]+2) for y in xrange(self.position[1]-1,self.position[1]+2) if (x,y) != self.history[self.move_counter]]
        else:
            possibles = [(x,y) for x in xrange(self.position[0]-1,self.position[0]+2) for y in xrange(self.position[1]-1,self.position[1]+2) if (x,y) != self.history[self.move_counter] and (x,y) != self.history[self.move_counter-1]]
        #print possibles
        cells = [(self.pheromones[possible[0]][possible[1]],(possible[0], possible[1])) for possible in possibles if self.pheromones[possible[0]][possible[1]] >= 0]
        #print cells
        if len(cells) != 0:
            if random.random() < pheromone_importance:
                cells.sort()
                if cells[-1][0] == 0:
                    random.shuffle(cells)
                self.position =  cells[-1][1]
            else:
                self.position = random.choice(cells)[1]        
        #print self.position, self.move_counter
    def translate_path(self):
        position = (self.position[0]*ant_vision, self.position[1]*ant_vision)
        near = None
        shortest = walking_agent.vision
        for landmark in self.map.landmarks:
            distance = general_tools.calculate_distance(position, landmark.center)
            if distance < shortest:
                near = landmark
                shortest = distance
        if near != None:
            step = dict()
            step["action"] = "go"
            step["landmark"] = near
            step["orientation"] = "toward"
            if self.route_counter < 1:
                self.route[self.route_counter] = step
                self.route_counter += 1
            elif not step == self.route[self.route_counter-1]:
                self.route[self.route_counter] = step
                self.route_counter += 1
                
    def lay_pheromones(self):
        strength = 1-(self.score*0.00704) # 1/142, or the maximum distance
        #strength = 142-self.score
        if strength < 0:
            strength = 0        
        return strength

def calculate_fitness(route, plot=False, verbose=False):
    if verbose:
        print "Winning route instructions: "
    dude = walking_agent.Agent(map=map, destination=destination, route=route)
    walking = False
    while walking == False:
            walking = dude.update(verbose=verbose)
    if plot:
        savedpath = open("savedpath","w")
        savedmap = open("savedmap","w")
        pickle.dump(dude.history,savedpath)
        pickle.dump(map,savedmap)
        savedpath.close()
        savedmap.close()
    return walking[1]

def pheromone_decay(pheromones):
    pheromones[0][0] = -1
    for x in xrange(len(pheromones)):
        for y in xrange(len(pheromones[0])):
            if pheromones[x][y] > decay_rate: 
                pheromones[x][y] *= decay_rate
            elif pheromones[x][y] < -1:
                pheromones[x][y] = -1

def add_pheromones(all_pheromones, ant):
    strength = ant.lay_pheromones()
    if strength > pheromone_tolerance:
        for position in ant.history:
                all_pheromones[position[0]][position[1]] += strength

def fitness(ant):
    position = (ant.position[0]*ant_vision, ant.position[1]*ant_vision)
    distance = general_tools.calculate_distance(position, (90,10))
    return distance

def main():
    pheromones = copy.deepcopy(grid)
    scores = []
    bests = []
    early = False
    for i in xrange(iterations):
        if not early:
            ants = [Ant(map,pheromones) for _ in xrange(population_size)]
            for ant in ants:
                ant.walk()
                ant.score = calculate_fitness(ant.route)
            for ant in ants:
                add_pheromones(pheromones, ant)
            
            best= min([ant.score for ant in ants])
            print best
            bests.append(best)
            if i%early_number == 0 and i != 0:
                if sum(bests[-early_number:]) < (walking_agent.tolerance)*early_number:
                    early = early_termination
            scores.append(sum([ant.score for ant in ants])/population_size)
            pheromone_decay(pheromones)
            print i
    
    sp = open("savedsco","w")
    pickle.dump(scores,sp)
    sp.close()
    sp = open("savedphe","w")
    pickle.dump(pheromones,sp)
    sp.close()
    s = min([ant.score for ant in ants])
    print s
    show = [ant for ant in ants if ant.score == s][0]
    savedpath = open("antpath","w")
    pickle.dump(show.history,savedpath)
    savedpath.close()
    calculate_fitness(show.route,plot=True,verbose=True)
    
main()



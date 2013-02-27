'''
Created on 2012-04-25

@author: Sebastien Ouellet sebouel@gmail.com
'''
import random
import pickle

import landmark_map
import walking_agent
import general_tools


####### Parameters #######

population_size = 50
crossover_probability = 0.8
mutation_probability = 0.001

tournament_size = 7
tournament_probability = 0.9

number_genes = 20
iterations = 100

many_tests = False

#map = landmark_map.Map()
somemap = open("somemap","r")
map = pickle.load(somemap)
destination = (35,80)
landmark_map.assess_landmarks(map.landmarks)

##########################

def min_or_max(scores):
    return min(scores)

def tournament(population, scores):
    chosen = random.sample(scores, tournament_size)
    if random.random() < tournament_probability:
        index = min_or_max(chosen)
        winner = population[index[1]]
        return winner
    else:
        return population[random.choice(chosen)[1]]

def selection(population, scores):
    selected = [None]*population_size
    for i in xrange(population_size):
        selected[i] = tournament(population, scores)
    return selected

def walking_test(route, plot=False, verbose=False):
    dude = walking_agent.Agent(map=map, destination=destination, route=route)
    walking = False
    while walking == False:
        walking = dude.update(verbose=verbose)
        #print general_tools.print_landmark(dude.desired)
        #print walking
    if plot:
        savedpath = open("savedpath","w")
        savedmap = open("savedmap","w")
        pickle.dump(dude.history,savedpath)
        pickle.dump(map,savedmap)    
    return walking[1]

def fitness_test(population):
    scores = [None]*population_size
    for i in xrange(population_size):
            route = population[i]
            distance = walking_test(route)
            scores[i] = (distance,i)
    return scores

def random_step():
    step = dict()
    step["action"] = "go"
    #step["landmark"] = landmark_map.translate_to_landmark(random.choice(landmark_map.colors),random.choice(landmark_map.estimated_sizes),random.choice(landmark_map.estimated_heights),random.choice(landmark_map.shapes))
    step["landmark"] = random.choice(map.landmarks)
    step["orientation"] = "toward"
    return step

def generate_random():
    route = []
    for _ in xrange(number_genes):
        step = random_step()
        route.append(step)
    return route
    
    individual = [None]*number_genes
    for i in xrange(number_genes):
        individual[i] = random.randint(0,1)
    return individual

def generate_population():
    population = [None]*population_size
    for i in xrange(population_size):
        population[i] = generate_random()
    return population

def one_crossover(parent1, parent2):
    first = random.randint(1,number_genes-1)
        
    child1 = list(parent1)
    child2 = list(parent2)
    
    for index in xrange(first):
        child1[index] = mutate(parent2[index])
        child2[index] = mutate(parent1[index])

    return child1,child2

def mutate(allele):
    step = random_step()
    return step

def all_mutate(individual):
    for i in xrange(number_genes):
        if random.random() < mutation_probability:
            individual[i] = mutate(individual[i])
            
    return individual 

def generate_offsprings(selected, scores, population):
    new_population = [None]*population_size
    #fittest = min_or_max(scores)
    #best = list(population[fittest[1]])
    for i in xrange(population_size):
        if random.random() < crossover_probability and i < population_size-1:
            new_population[i], new_population[i+1] = one_crossover(selected[i],selected[i+1])
        else:
            new_population[i] = all_mutate(selected[i])
    #new_population[0] = best
    return new_population

def main(test):
    population = generate_population()
    scores = fitness_test(population)
    selected = selection(population, scores)
    for iteration in xrange(iterations):
        population = generate_offsprings(selected,scores,population)
        scores = fitness_test(population)
        selected = selection(population, scores)
        fittest = min_or_max(scores)
        print "Best score: "+str(fittest[0])
        print "Generation: "+str(iteration)
        if fittest[0] < walking_agent.tolerance:
            break
    fittest = min_or_max(scores)
    print "Best score: "+str(fittest[0])
    print "Fittest individual: "
    route = population[fittest[1]]
    print walking_test(route,plot=True,verbose=True)
    
    if test:
        return fittest[0]

main(test=many_tests)
    
    
    
    

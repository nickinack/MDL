import numpy as np
import random
import json
import os
import client
import matplotlib.pyplot as plt
import pickle
import datetime

# issues might be that the high powers make weights much more sensitive
# we have to incorporate the overfittedness requirement of the assignment

# PARAMETERS

# pop_cnt = 10, max_gen = 50, sus

mutation_ratio = 0.7
pop_cnt = 12
gene_size = 11
max_gen = 11
n_matings = (pop_cnt - 3) // 2
n_mutation = int(mutation_ratio * pop_cnt)
population = []  # population that stores n 11-d arrays (weights for the model)
errors = []
pop_verbose = []
debug = False

# LOGGERS
iter_no = 0
fitness_track = []
iteration_track = []
best_individuals_track = []
verbose = []

# Heuristics
crossover_strategy = 'simulated_binary'
selection_strategy = 'classic_linear_rank'
mutation_strategy = 'mutation_2'


# overfit vector
overfit = [0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11, -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,  2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]

def open_file2(file_name):
    open_file = open(file_name, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()
    return loaded_list

def get_previous_population_entry(filename):
    population = open_file2(filename)
    return population

def initialize_population():
    """Sets up population array
    with randomized individual states
    returns:
    numpy array that models initial population
    """
    population = np.empty(shape=(pop_cnt, gene_size))

    for i in range(gene_size):
        population[:, i] = np.random.uniform(-10, 10 , size=pop_cnt)
    # for i in range(gene_size):
    #     population[:, i] = np.ones((pop_cnt,))

    return population


def initialize_population_SUBMISSION():
    """Sets up population array
    based off of overfit model
    returns:
    numpy array that models initial population
    """
    if not debug: 
        overfit = [0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11, -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,  2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]
    if debug:
        overfit = open_file("weights.pkl")

    population = np.empty(shape=(pop_cnt, gene_size))

    for i in range(pop_cnt):
        if not debug:
            population[i] = [x*np.random.uniform(0.9, 1.1) for x in overfit]
        if debug:
            population[i] = [x*np.random.uniform(0.8, 1.2) for x in overfit]
    
    return population


def solve():  # TODO: demoss
    """
    Runs the genetic algorithm for some number of iterations and optimizes the weights for the model
    """
    global population
    global best_individuals_track
    
    # Declare necessary data structures
    curr_generation = 0
    average_fitness = []
    max_fitness = []
    # Initialize random population and compute its fitness
    # population = initialize_population_SUBMISSION()
    population = np.array(get_previous_population_entry('continue_best_submission_7.pkl'))[:12]
    fitness = compute_population_fitness(population)

    print('------init---------')
    print(fitness[0])
    
    # Sort population and fitness in descending order of fitness value
    sorted_ind = np.argsort(fitness)[::-1]  # indices of population in descending order of fitness values
    population, fitness = population[sorted_ind, :], fitness[sorted_ind]

    while curr_generation < max_gen:
        curr_generation += 1
        pop_verbose_iter = {"generation": curr_generation , "after_selection": [], "after_crossover": [], "after_mutation": []}
        if curr_generation % 5 == 0:
            print('curr_generation: ', curr_generation)
            print('best weights: ', population[0])
            print('best fitness: ', fitness[0])
            print('-------------')
        fitness_track.append(fitness[0])
        iteration_track.append(curr_generation)
        best_individuals_track = population[0]
    
        # update tracking
        average_fitness.append(np.mean(fitness))
        max_fitness.append(fitness[0])
    
        #  select parents indices
        ma, pa = selection(fitness, selection_strategy , n_matings), selection(fitness, selection_strategy , n_matings)
        pop_verbose_iter["after_selection"] = population
        
        j = 0
        for i in range(n_matings):
            ma_el, pa_el = population[ma[i], :], population[pa[i], :]  # choose the two parents from the ma, pa indices
            c1, c2 = crossover(ma_el, pa_el, crossover_strategy)  # Produce two offsprings from the selected parents
            # Replace the parents in population with the offsprings
            # TODO: possible issues are repeated parent individuals. Maybe enforce uniqueness?
            population[-j-1,:] = c1
            population[-j-2,:] = c2
            j = j + 2
        pop_verbose_iter["after_crossover"] = population
        population = mutate_population(population)
        pop_verbose_iter["after_mutation"] = population
        pop_verbose.append(pop_verbose_iter)
        fitness = compute_population_fitness(population)  # TODO: THIS HAS BEEN COPY PASTED...
        # fitness = np.hstack((fitness[0], curr_fitness))  # IDEK what hstack does  TODO: why stack fitness[0]????
        sorted_ind = np.argsort(fitness)[::-1]  # indices of population in descending order of fitness values
        population, fitness = population[sorted_ind, :], fitness[sorted_ind]
        display_generation_info()
    

def select_parents(population):
    return selection(population, selection_strategy, n_matings), selection(population, selection_strategy, n_matings)


def selection(population , strat , N=1):
    '''
    Returns the fittest from the given population; input: fitness of the population
    '''
    parent_ind = []
    if strat == "rowlette_wheel":
        min_element = min(population)
        tot_fitness = 0
        selection_prob = []
        for i in range(0 , len(population)):
            population[i] = population[i] + abs(min_element)
        for i in range(0 , len(population)):
            tot_fitness = tot_fitness + population[i]
        for i in range(0 , len(population)):
            selection_prob.append(population[i]/tot_fitness)
        for i in range(0 , N):
            parent_ind.append(np.random.choice(len(population) , p=selection_prob))

    elif strat == "sus":
        wheel = makeWheel(population)
        stepSize = 1.0/N
        r = random.random()
        parent_ind = []
        parent_ind.append(binSearch(wheel, r))
        while len(parent_ind) < N:
            r += stepSize
            if r > 1:
                r %= 1
            parent_ind.append(binSearch(wheel, r))

    elif strat == "classic_linear_rank":
        rank = np.zeros(len(population))
        sorted_ind = np.argsort(population)
        for i in range(0 , len(sorted_ind)):
            rank[sorted_ind[i]] = i
        parent_ind = selection(rank , "rowlette_wheel" , N)

    return parent_ind


def mutate_population(population):
    """
    Mutates a random sample of individuals from the population
    :param population: list of indivudals
    """
    indices = random.sample(range(len(population)), n_mutation)
    for ind in indices:
        population[ind] = mutation(population[ind], mutation_strategy)  # param1, param2?
    return population


def mutation(individual , str , param1=0 , param2=0):
    '''
    Mutates a given individual using a probability distribution
    Gauss: Param1 = mu; Param2 = sigma
    Gamma: Param1 = alpha; Param2 = beta
    '''
    global debug
    if str == "uniform_mutation":
        if not debug:
            delta = np.random.uniform(0.8 , 1.2)
        if debug:
            delta = np.random.uniform(0.70 , 1.30)
        allele = min(10, max(-10, random.randint(0, len(individual)-1)))
        individual[allele] = individual[allele]*delta
        val = random.uniform(min(individual), min(individual)*delta)
        u = random.random()*10
        if u <= 4:
            individual[allele] = individual[allele] + val

    if str == "mutation_2":
        for i in range(0 , len(individual)):
            u = np.random.randint(0 , 10)
            if u < 3:
                delta = np.random.uniform(0.94 , 1.06)
                individual[i] = individual[i]*delta
    
    if str == "mutation3":
        for i in range(0 , len(individual)):
            u = np.random.randint(0 , 11)
            if u < 3:
                delta = np.random.uniform(0.95 , 1.05)
                individual[i] = 0.3 * individual[i] + 0.7 * overfit[i]*delta

    elif str == "gauss":
        allele = random.randint(0, len(individual)-1)
        individual[allele] = random.gauss(param1, param2)

    elif str == "gamma":
        allele = random.randint(0, len(individual)-1)
        individual[allele] = random.gammavariate(param1, param2)
    
    elif str == "interchanging":
        pos1 = random.randint(0, len(individual)-1)
        pos2 = random.randint(0, len(individual)-1)
        while pos1 == pos2:
            pos2 = random.randint(0, len(individual)-1)
        temp = individual[pos1]
        individual[pos1] = individual[pos2]
        individual[pos2] = temp

    elif str == "insert":
        pos1 = random.randint(0, len(individual)-1)
        pos2 = random.randint(0, len(individual)-1)
        while pos1 == pos2:
            pos2 = random.randint(0, len(individual)-1)
        if pos1 > pos2:
            temp = pos1
            pos1 = pos2
            pos2 = temp
        pos1_val = individual[pos1]
        for shift in range(pos1 + 1, pos2 + 1):
            individual[shift - 1] = individual[shift]
        individual[pos2] = pos1_val

    return individual

def crossover(parent1 , parent2 , str):
    '''
    Given two parents, performs crossover 
    '''
    len1 = len(parent1)
    len2 = len(parent2)
    offspring1 = []
    offspring2 = []
    assert len1 == len2 , "Length of the individuals should be the same"

    if str == "one_point":
        crossover_point = np.random.randint(0 , len1)
        for i in range(0 , crossover_point):
            offspring1.append(parent1[i])
            offspring2.append(parent2[i])
        for i in range(crossover_point , len1):
            offspring1.append(parent2[i])
            offspring2.append(parent1[i])

    if str == "simulated_binary":
        u = random.random()
        n_c = 3

        if u < 0.5:
            beta = (2 * u)**((n_c + 1)**-1)
        else:
            beta = ((2*(1-u))**-1)**((n_c + 1)**-1)
        offspring1 = 0.5*((1 + beta) * np.array(parent1) + (1 - beta) * np.array(parent2))
        offspring2 = 0.5*((1 - beta) * np.array(parent1) + (1 + beta) * np.array(parent2))

    elif str == "two_point":
        crossover_point1 = np.random.randint(0 , len1)
        crossover_point2 = crossover_point1
        while crossover_point2 == crossover_point2:
            crossover_point2 = np.random.randint(0 , len1)
        for i in range(0 , crossover_point1):
            offspring1.append(parent1[i])
            offspring2.append(parent2[i])
        for i in range(crossover_point1 , crossover_point2):
            offspring1.append(parent2[i])
            offspring2.append(parent1[i])
        for i in range(crossover_point2 , len1):
            offspring1.append(parent1[i])
            offspring2.append(parent2[i])

    elif str == "uniform":
        for i in range(0 , len1):
            choice = np.random.randint(0,2)
            if choice == 0:
                offspring1.append(parent1[i])
                offspring2.append(parent2[i])
            elif choice == 1:
                offspring1.append(parent2[i])
                offspring2.append(parent1[i])

    return [offspring1 , offspring2]


def fitness_func(weight):
    '''
    Given weights, calculates the fitness functions and calls the API
    '''
    global debug
    weight = list(np.array(weight).ravel())
    if not debug:
        train_error , validation_error = client.get_errors('GU0MCOlKFoi0lk7HmBpwjhFGlcTTZvO77FA3FVMq0m4lYCMIho' , weight)
    if debug:
        train_error , validation_error = equation.get_errors(weight)
    #train_error, validation_error = equation.get_errors(weight)
    if not debug:
        train_weight , val_weight = 1,1
    if debug:
        train_weight , val_weight = 0.4 , 0.6
    ratio = train_weight*train_error + val_weight*validation_error + abs(validation_error - train_error)
    return (1/ratio), train_error, validation_error


def compute_population_fitness(population):
    """
    Given the population, return the fitness values of each individual
     :param population: a list of 11-d vector individuals
     :returns: fitness of current population
    """
    global iter_no

    fitness = []
    error_dict = {"generation": iter_no , "fitness": [], "train_error": [], "val_error": [] , "population": [], "pop_verbose": []}
    iter_no += 1
    
    for i in range(len(population)):
        ind_fitness, train_error, val_error = fitness_func(population[i])
        fitness.append(ind_fitness)
        error_dict["fitness"].append(ind_fitness)
        error_dict["train_error"].append(train_error)
        error_dict["val_error"].append(val_error)
        error_dict["population"].append(population[i])
        error_dict["pop_verbose"].append(pop_verbose)
    verbose.append(error_dict)
    return np.array(fitness)

def display_generation_info():
    print(verbose[-1]["train_error"] , verbose[-1]["val_error"])
    mini_val = 1e32
    mini_index = -1
    for i in range(0 , len(verbose[-1]["val_error"])):
        if mini_val > verbose[-1]["val_error"][i]:
            mini_val = verbose[-1]["val_error"][i]
            mini_index = i

    print("Lowest Val error: {:0.10e}".format(mini_val))
    print("Corr Train error: {:0.10e}".format(verbose[-1]["train_error"][mini_index]))
    print("Correspo weights: ", verbose[-1]["population"][mini_index])
    print("\n")

# TODO: demoss

def makeWheel(population):
    """Helper for the RWS in creating a proportional
    distribution among elements in a given array
    Args:
        population(list): List of int/float
    
    Returns:
        list: The generated wheel
    """
    wheel = []
    total = 0
    for i in range(0 , len(population)):
        total = total + population[i]
    top = 0
    for i in range(0 , len(population)):
        p = population[i]
        f = p/total
        wheel.append((top, top+f, i))
        top += f
    return wheel

def binSearch(wheel, num):
    """Standard binary search
    Args:
        wheel(list): An ordered list of floats/ints
        num(int/float): Element to be searched
    
    Returns:
        int: value
    """
    mid = len(wheel)//2
    low, high, answer = wheel[mid]
    if low<=num<=high:
        return answer
    elif high < num:
        return binSearch(wheel[mid+1:], num)
    else:
        return binSearch(wheel[:mid], num)

def open_file(file_name):
    open_file = open(file_name, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()
    return loaded_list

try:
    solve()
except Exception:
    print('solve() terminated')

if not debug:
    fname = "verbose" + str(datetime.datetime.now()) + ".pkl"
if debug:
    fname = "debug_verbose" + str(datetime.datetime.now()) + ".pkl"
open_fname = open(fname , "wb")
pickle.dump(verbose , open_fname)
open_fname.close()

print('best fitness achieved', fitness_track[-1])
plt.plot(iteration_track, fitness_track)
plt.savefig('fitness_iteration.png')

plt.plot(list(map(lambda pop: pop['generation'], verbose)), list(map(lambda x: min(x['train_error']), verbose)), label='train_error')
plt.plot(list(map(lambda pop: pop['generation'], verbose)), list(map(lambda x: min(x['val_error']), verbose)), label='val_error')
plt.legend(loc="upper left")
plt.savefig('err_iteration.png')


# 26/02/2021
# RUN-1 (Best till date):
    # Rowlette Wheel
    # 0.4 , 0.6
    # pop_cnt=25 x x10

# RUN-2 (Best till date):
    # Sus
    # 0.5 , 0.5
    # pop_cnt=25 x x10

# 27/02/2021
# RUN-1
    # Classical Linear Rank
    # 0.5 , 0.5
    # 0.96 , 1.04 => Initial

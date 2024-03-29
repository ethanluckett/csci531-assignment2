#!/usr/bin/env python
from util import generate, evaluate, print_board
import time
import random
try:
    from tqdm import tqdm
except:
    def tqdm(x):
        return x


def crossover(a, b):
    fulcrum = random.randint(0, len(a)-1)
    return a[:fulcrum] + b[fulcrum:]


def mutate(individual, rate):
    index = random.randint(0, len(individual)-1)
    if random.random() < rate:
        individual[index] = random.randint(0, len(individual)-1)


def do_iteration(population, fitness, mutation_rate, max_fitness):
    pop_size = len(population)
    
    new_population = []
    new_fitness = []
    for i in range(pop_size):
        [a, b] = random.choices(population, weights=fitness, k=2)
        child = crossover(a, b)
        mutate(child, mutation_rate)

        new_population.append(child)

        f = evaluate(child)
        if f == max_fitness:
            return [], [], [], max_fitness
        new_fitness.append(f)

    best_f = 0
    for i in range(pop_size):
        f = fitness[i]
        if f > best_f:
            best_f = f
            best_individual = new_population[i]

    return new_population, new_fitness, best_individual, best_f


def nqueens_genetic(size, pop_size, max_generations, mutation_rate):
    population = [generate(size) for _ in range(pop_size)]
    max_fitness = (size * (size - 1)) / 2
   
    i = 0
    fitness = list(map(evaluate, population))
    while i < max_generations:
        population, fitness, best_individual, best_f = do_iteration(population, fitness, mutation_rate, max_fitness)
        i += 1
        if best_f  == max_fitness:
            break

    return best_f, i*pop_size


def main():
    size = 8 # number of queens
    pop_size = 500
    max_generations = 200
    mutation_rate = 0.1

    n = 1000
    num_solutions = 0
    total_individuals = 0
    for i in tqdm(range(n)):
        best_f, num_individuals = nqueens_genetic(size, pop_size, max_generations, mutation_rate)
        if best_f == (size * (size - 1)) / 2:
            num_solutions += 1
            total_individuals += num_individuals

    print('{:.1f}% success, avg individuals: {}'.format(num_solutions * 100/n, total_individuals / num_solutions))




if __name__ == '__main__':
    main()

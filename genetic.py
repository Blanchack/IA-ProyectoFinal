import random

from deap import algorithms, base, creator, tools

from pacman_ga.fitness import fitness_base
from pacman_ga.maze import enforce_borders

POPULATION_SIZE = 100
N_GENERATIONS = 1000
CROSSOVER_PROB = 0.7
MUTATION_PROB = 0.05
CHROMOSOME_LENGTH = 400


def cx_three_point(ind1, ind2):
    n = len(ind1)
    if n < 4:
        return ind1, ind2
    q = n // 4
    child1 = list(ind1)
    child2 = list(ind2)
    for seg in (1, 3):
        s = seg * q
        e = s + q
        for i in range(s, e):
            child1[i] = ind2[i]
            child2[i] = ind1[i]
    for i in range(n):
        ind1[i] = child1[i]
        ind2[i] = child2[i]
    return ind1, ind2


def _reset_creators():
    if hasattr(creator, "FitnessMax"):
        del creator.FitnessMax
    if hasattr(creator, "Individual"):
        del creator.Individual
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)


def _create_toolbox(fitness_fn, cx_function=cx_three_point):
    toolbox = base.Toolbox()
    toolbox.register("attr_int", random.randint, 0, 1)
    toolbox.register(
        "individual",
        tools.initRepeat,
        creator.Individual,
        toolbox.attr_int,
        n=CHROMOSOME_LENGTH,
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", fitness_fn)
    toolbox.register("mate", cx_function)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selRoulette)
    return toolbox


def _fix_individual(individual):
    fixed = enforce_borders(list(individual))
    for i in range(len(individual)):
        individual[i] = fixed[i]


def run_base(n_generations=N_GENERATIONS, pop_size=POPULATION_SIZE, verbose=True, elitism=True):
    _reset_creators()
    toolbox = _create_toolbox(fitness_base, cx_function=cx_three_point)

    pop = toolbox.population(n=pop_size)
    for ind in pop:
        _fix_individual(ind)

    fits = toolbox.map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fits):
        ind.fitness.values = fit

    best_overall = tools.selBest(pop, k=1)[0]

    fitness_log = []
    best_per_gen = []

    for gen in range(n_generations):
        offspring = algorithms.varAnd(
            pop, toolbox, cxpb=CROSSOVER_PROB, mutpb=MUTATION_PROB
        )
        for ind in offspring:
            _fix_individual(ind)

        fits = toolbox.map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fits):
            ind.fitness.values = fit

        pop = toolbox.select(offspring, k=len(pop))

        if elitism:
            worst_idx = min(
                range(len(pop)),
                key=lambda i: pop[i].fitness.values[0],
            )
            pop[worst_idx] = toolbox.clone(best_overall)

        current_best = tools.selBest(pop, k=1)[0]
        if current_best.fitness.values[0] > best_overall.fitness.values[0]:
            best_overall = current_best

        fits_values = [ind.fitness.values[0] for ind in pop]
        avg_fit = sum(fits_values) / len(fits_values)
        fitness_log.append(avg_fit)
        best_per_gen.append(list(best_overall))

        if verbose and gen % 200 == 0:
            print(
                f"  [Base] Gen {gen}/{n_generations} | "
                f"Avg fitness: {avg_fit:.4f} | "
                f"Best: {best_overall.fitness.values[0]:.4f}"
            )

    return fitness_log, best_per_gen

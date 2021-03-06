from solver import KCenterSolver
import random


class EvolutionarySolver(KCenterSolver):
    def __init__(self, graph, pop_size, iters, mutation_rate, tournament_size, selection_type):
        super().__init__(graph)
        self.pop_size = pop_size
        self.population = []
        self.iters = iters
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.selection_type = selection_type

    def __repr__(self):
        return f"Evoultionary; Pop_size {self.pop_size} " + \
                f"Iters: {self.iters}" + f" Selection type: {self.selection_type}"\
                + f" n = {self.graph.cardV}"

    def __initialize(self, k):
        for i in range(self.pop_size):
            idx = random.sample(range(self.graph.cardV), k)
            new_individual = self.graph.cardV * [False]
            for i in idx:
                new_individual[i] = True
            self.population.append(new_individual)

    def __selection(self, population: list):
        if self.selection_type == 1:
            contestants = random.sample(population, self.tournament_size)
            best = min(contestants, key=lambda x: x[1])
            return best[0]
        else:
            total_fitness = sum(map(lambda x: 1/x[1], population))
            treshold = random.uniform(0, total_fitness)
            cum_sum = 0.0
            for (solution, fitness) in population:
                cum_sum += 1/fitness
                if treshold <= cum_sum:
                    return solution

    def __crossover(self, parent1: list, parent2: list, k):
        child1 = parent1[:]
        child2 = parent2[:]
        index1 = set()
        index2 = set()
        for i in range(len(parent1)):
            if parent1[i]:
                index1.add(i)
            if parent2[i]:
                index2.add(i)


        set_dif1 = index1.difference(index2)
        set_dif2 = index2.difference(index1)
        samp1 = set(random.sample(set_dif1, len(set_dif1)))
        samp2 = set(random.sample(set_dif2, len(set_dif2)))


        
        for s1, s2 in zip(samp1, samp2):
            t1 = sum(child1)
            tmp = child1[s1]
            child1[s1] = child2[s1]
            child2[s1] = tmp

            tmp = child2[s2]
            child2[s2] = child1[s2]
            child1[s2] = tmp
        return (child1[:], child2[:])

    def __mutate(self, child: list):
        if random.random() > self.mutation_rate:
            return child
        index1 = random.randint(0, self.graph.cardV-1)
        changed_val = child[index1]
        child[index1] = not child[index1]
        while True:
            index2 = random.randint(0, self.graph.cardV-1)
            if changed_val != child[index2]:
                child[index2] = not child[index2]
                break

        return child

    def solve(self, k):
        self.__initialize(k)

        for iteration in range(self.iters):
            
            fitnesses = list(map(lambda x: self.evaluate(x), self.population))
            pop_with_fit = list(zip(self.population, fitnesses))
            pop_with_fit.sort(key=lambda t: t[1], reverse=False)
            new_population = []
            for i in range(int(10)):
                new_population.append(pop_with_fit[i][0])

            for i in range(int(10), self.pop_size, 2):
                parent1 = self.__selection(pop_with_fit)
                parent2 = self.__selection(pop_with_fit)
                child1, child2 = self.__crossover(parent1, parent2, k)
                self.__mutate(child1)
                self.__mutate(child2)
                new_population.append(child1)
                new_population.append(child2)

            self.population = new_population
            # if iteration % 100 == 0:
            #     print(self.evaluate(self.population[0]))
        print(self, end = " ")
        print(self.evaluate(self.population[0]))

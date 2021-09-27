import random, operator, copy, math
from itertools import groupby

M = 16

def initial_population(mapper1, population, popSize):
    pop = []
    for i in range(len(population)):
        pop.append(population[i])
    for i in range(popSize):
        m1 = mapper1.copy()
        random.shuffle(m1)
        pop.append(m1)
    return list(tuple(pop))

def mappoints(map, mapper):
    mapped = {}
    for i in range(len(mapper)):
        for j in map.keys():
            if j == mapper[i]:
                #print(mapper[i], map.get(i))
                mapped[j] = map.get(i)
    return mapped


def fitness(list1, list2, list3, map):
    list4 = []
    list1, list2, list3 = mappoints(map, list1), mappoints(map, list2), mappoints(map, list3)
    for i in range(len(list2)):
        for j in range(len(list3)):
            if i != j:
                fit = abs(list1[i]-list1[j]) * abs(list2[i]-list2[j]) * abs(list3[i]-list3[j])
                list4.append(fit)
    return round(min(list4),4)

def rank_fitness(gray, mapper2, population, map):
    rFit = {}
    for i in range(len(population)):
        rFit[i] = fitness(gray, mapper2, population[i], map)
    return sorted(rFit.items(), key=operator.itemgetter(1), reverse=True)

def Keeping_best_chromosomes(mapper1, mapper2, population, map):
    rank = rank_fitness(mapper1, mapper2, population, map)
    best = rank[0][1]
    keep = []
    for i in range(len(population)):
        if fitness(mapper1, mapper2, population[i], map) == best:
            keep.append(list(population[i]).copy())
            #if len(keep) == len(list(population))/2: break
    return keep

def remove_duplicates(ls):
    # groupby needs ls to be sorted first
    new = sorted(ls)
    return list(key for key,val in groupby(new))

def ls1_setminus_ls2(ls1, ls2):
    ls2_set = set(ls2)
    return [item for item in ls1 if item not in ls2]

def davis_xover(x, y, i, j):
    # Init
    z = []
    length = len(x)
    xover_sect = x[i:j+1] # [i, j + 1) = [i, j]
    # Main
    fillers = ls1_setminus_ls2(y, xover_sect)
    for at in range(length):
        # copy xover section
        if i <= at <= j:
            z.insert(at, x[at])
        # use fillers
        else:
            filler = fillers.pop(0) # pop returns 1st elem and deletes it.
            z.insert(at, filler)
    return z

def all_davis_xover(x, y):
    oll = []
    length = len(x)

    for i in range(0, length):
        for j in range(i, length):
            z1 = davis_xover(x, y, i, j)
            z2 = davis_xover(y, x, i, j)
            oll.append(z1)
            oll.append(z2)

    return remove_duplicates(oll)

def crossoverPopulation(population):
    crossed = []
    for i in range(len(population)):
        for j in range(len(population)):
            crossed.append(all_davis_xover(population[i], population[j]))
    return crossed


def mutation(child, rate):
    if random.random() < rate:
        i = random.randint(0, len(child)-1)
        j = random.randint(0, len(child)-1)

        child[i], child[j] = child[j], child[i]
    return child

def mutatePopulation(children, rate):
    mutated = []
    for i in range(len(children)):
        for j in range(len(children[i])):
            mutated.append(mutation(children[i][j], rate))
    return mutated

def AddToPopulation(parents, children, best, AddedPop):
    for i in range(len(parents)):
        AddedPop.append(parents[i])
    for i in range(len(children)):
        AddedPop.append(children[i])
    for i in range(len(best)):
        AddedPop.append(best[i])
    return AddedPop

def nextGeneration(gray, mapper2, population, popSize, map):
    newPop = []
    rank = rank_fitness(gray, mapper2, population, map)
    for i in range(popSize):
        newPop.append(population[rank[i][0]])
    return newPop

map = {
0 :complex( 0.5501 , 0.0 ),
1 :complex( 0.17000963814973397 , 0.5231698891719558 ),
2 :complex( -0.4450162804442702 , 0.32337365405911883 ),
3 :complex( -0.44507619626306205 , -0.3232911837956679 ),
4 :complex( 0.16991268809472232 , -0.5232013841958234 ),
5 :complex( 1.1476 , 0.0 ),
6 :complex( 0.965421725548501 , 0.6204406916369642 ),
7 :complex( 0.4767274802388382 , 1.043894951412798 ),
8 :complex( -0.16332506017978676 , 1.135918432246466 ),
9 :complex( -0.7515228121037436 , 0.8672941962723383 ),
10 :complex( -1.1011162957809277 , 0.32330892837298547 ),
11 :complex( -1.1011115453420512 , -0.32332510684207577 ),
12 :complex( -0.7515100690247531 , -0.8673052381684377 ),
13 :complex( -0.16330837031662837 , -1.1359208318296337 ),
14 :complex( 0.47674281794843226 , -1.0438879468288673 ),
15 :complex( 0.9654308414679534 , -0.6204265068019573 )
}
mapper1 = [15, 11, 9, 3, 8, 2, 6, 13, 1, 4, 5, 7, 14, 10, 0, 12]
mapper2 = [12,10,13,9,15,11,8,14,6,5,7,3,1,4,0,2]
mapper3 = [10, 6, 8, 13, 15,7,14,5,1,11,12,9,3,4,0,2]
mapper4 = [9, 0, 7, 4, 11, 3, 14, 8, 10, 12, 15, 2, 5, 1, 13, 6]



maps = [mapper1,mapper2,mapper3,mapper4]

print(fitness(mapper1, mapper2, mapper3, map))
#print(fitness(mapper1, mapper2, map))

print("Enter population size")
popsize = int(input())
print("Enter mutation rate")
mutRate = float(input())

Maps = initial_population(mapper1,maps,popsize)
A = []

while True:
    best = Keeping_best_chromosomes(mapper1, mapper2, Maps, map)
    C = crossoverPopulation(Maps)
    M = mutatePopulation(C, mutRate)
    A = AddToPopulation(Maps, M, best, A)
    Maps = nextGeneration(mapper1, mapper2, A, popsize, map)
    print(Maps)
    print(rank_fitness(mapper1, mapper2, Maps, map))
    A = []

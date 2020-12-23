from random import randint

EQUATION_RESULT = 300
PARAMS_COUNT = 6

"""
    Solved equation: 
    6 * x1 + 7 * x2 + 2 * x3 + 2 * x4 + 5 * x5 + 1 * x6 = 300 (EQUATION_RESULT)
"""


def get_mutation(populations, populations_count):
    new_populations = []
    for i in range(len(populations)):
        random = randint(0, 100)
        # 0.5 - шанс новой генерации
        if random < 100 * 0.5:
            index = int(random // 100 * populations_count)
            populations[i][index] = randint(-100, 100)
        new_populations.append(populations[i])
    return new_populations


def get_reverse(results):
    results = [1 / abs(EQUATION_RESULT - result) for result in results]
    return [result / sum(results) for result in results]


def calculate_populations(populations):
    results = []
    for x1, x2, x3, x4, x5, x6 in populations:
        results.append(
            6 * x1 + 7 * x2 + 2 * x3 + 2 * x4 + 5 * x5 + 1 * x6
        )
    return results


def get_result(populations):
    for x1, x2, x3, x4, x5, x6 in populations:
        calculated = (
            6 * x1 + 7 * x2 + 2 * x3 + 2 * x4 + 5 * x5 + 1 * x6
        )
        if calculated == EQUATION_RESULT:
            return (x1, x2, x3, x4, x5, x6)
    return False


def next_population(populations, populations_count):
    results = calculate_populations(populations)
    coefficient = get_reverse(results)
    fitnes = sum(coefficient)
    results = dict(zip(range(0, len(populations)), coefficient))
    results = [k for k, i in sorted(results.items(), key=lambda item: item[1], reverse=True)]
    new_populations = []
    for i in range(len(populations) // 2):
        population_1 = populations[results[2 * i]]
        population_2 = populations[results[2 * i + 1]]
        random_slice = randint(1, len(population_1) - 2)
        new_population = (
            population_1[:random_slice] + population_2[random_slice:],
            population_2[:random_slice] + population_1[random_slice:]
        )

        new_populations.extend(new_population)
    if get_result(new_populations):
        return new_populations
    new_fitnes = sum(get_reverse(calculate_populations(new_populations)))
    if fitnes > new_fitnes:
        populations = get_mutation(populations, populations_count)
    else:
        populations = new_populations
    return populations


populations = []
populations_count = 10
for i in range(populations_count):
    pop = []
    for j in range(PARAMS_COUNT):
        pop.append(randint(-100, 100))
    populations.append(pop)

i = 1
while not get_result(populations):
    print(f'|Population {i}|')
    populations = next_population(populations, populations_count)
    calculated_populations = calculate_populations(populations)
    best_result = None
    for result in calculated_populations:
        if (best_result is None or abs(best_result - EQUATION_RESULT) > abs(result - EQUATION_RESULT)):
            best_result = result
    print(f'Best population result: {best_result}')
    i += 1

print(f'Equation roots: {get_result(populations)}')


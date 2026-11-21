import random

from dataclasses import dataclass

from deap import base, creator, tools

from truck_route_optimizer.route_metrics import calculate_route_metrics
from truck_route_optimizer.route_operators import (
    generate_random_route,
    crossover_routes,
    mutate_route,
)
from truck_route_optimizer.vehicle import Vehicle


@dataclass
class GeneticAlgorithmResult:
    best_route: list[str]
    best_time_hours: float
    best_fuel_liters: float
    best_distance_km: float
    history: list[dict] 


def _create_deap_types():
    """
    Tworzy typy osobnika i funkcji przystosowania DEAP.

    Oba kryteria są minimalizowane. DEAP porównuje wartości
    fitness leksykograficznie, dlatego czas ma pierwszeństwo
    przed zużyciem paliwa.
    """
    if not hasattr(creator, "TruckRouteFitnessMin"):
        creator.create(
            "TruckRouteFitnessMin",
            base.Fitness,
            weights=(-1.0, -1.0),
        )

    if not hasattr(creator, "TruckRouteIndividual"):
        creator.create(
            "TruckRouteIndividual",
            list,
            fitness=creator.TruckRouteFitnessMin,
        )


def optimize_route(
    graph,
    vehicle: Vehicle,
    start_city: str,
    end_city: str,
    population_size: int = 50,
    generations: int = 100,
    crossover_probability: float = 0.8,
    mutation_probability: float = 0.2,
    elite_size: int = 2,
    tournament_size: int = 3,
    random_seed: int | None = None,
) -> GeneticAlgorithmResult:
    """
    Uruchamia algorytm genetyczny poszukujący optymalnej trasy.

    Kryteria optymalizacji:
    1. Minimalny czas przejazdu.
    2. Minimalne zużycie paliwa przy takim samym czasie.

    Zwraca najlepszą znalezioną trasę, jej parametry
    oraz historię najlepszego osobnika w kolejnych pokoleniach.
    """
    if population_size < 2:
        raise ValueError("Populacja musi liczyć co najmniej 2 osobniki.")

    if generations < 1:
        raise ValueError("Liczba pokoleń musi być większa od zera.")

    if not 0 <= crossover_probability <= 1:
        raise ValueError("Prawdopodobieństwo krzyżowania musi być w zakresie 0-1.")

    if not 0 <= mutation_probability <= 1:
        raise ValueError("Prawdopodobieństwo mutacji musi być w zakresie 0-1.")

    if not 1 <= elite_size < population_size:
        raise ValueError("Liczba elit musi być mniejsza od populacji i co najmniej równa 1.")

    if tournament_size < 2:
        raise ValueError("Rozmiar turnieju musi wynosić co najmniej 2.")

    if random_seed is not None:
        random.seed(random_seed)

    _create_deap_types()

    toolbox = base.Toolbox()

    def create_individual():
        return creator.TruckRouteIndividual(
            generate_random_route(
                graph,
                vehicle,
                start_city,
                end_city,
            )
        )

    def evaluate(individual):
        metrics = calculate_route_metrics(
            graph,
            list(individual),
            vehicle,
        )

        return metrics.time_hours, metrics.fuel_liters

    def mate(individual1, individual2):
        child1, child2 = crossover_routes(
            graph,
            vehicle,
            list(individual1),
            list(individual2),
        )

        individual1[:] = child1
        individual2[:] = child2

        return individual1, individual2

    def mutate(individual):
        mutated = mutate_route(
            graph,
            vehicle,
            list(individual),
        )

        individual[:] = mutated

        return (individual,)

    toolbox.register("individual", create_individual)
    toolbox.register(
        "population",
        tools.initRepeat,
        list,
        toolbox.individual,
    )
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", mate)
    toolbox.register("mutate", mutate)
    toolbox.register(
        "select",
        tools.selTournament,
        tournsize=tournament_size,
    )

    population = toolbox.population(n=population_size)

    # Ocena początkowej populacji.
    for individual in population:
        individual.fitness.values = toolbox.evaluate(individual)

    hall_of_fame = tools.HallOfFame(1)
    hall_of_fame.update(population)

    history = []

    def record_best(generation):
        best = hall_of_fame[0]

        history.append({
            "generation": generation,
            "time_hours": best.fitness.values[0],
            "fuel_liters": best.fitness.values[1],
        })

    record_best(0)

    # Główna pętla algorytmu genetycznego.
    for generation in range(1, generations + 1):

        # Wybór rodziców metodą turniejową.
        parents = toolbox.select(population, len(population))

        # Tworzenie kopii rodziców.
        offspring = list(map(toolbox.clone, parents))

        # Krzyżowanie.
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < crossover_probability:
                toolbox.mate(child1, child2)

                del child1.fitness.values
                del child2.fitness.values

        # Mutacja.
        for individual in offspring:
            if random.random() < mutation_probability:
                toolbox.mutate(individual)
                del individual.fitness.values

        # Ocena osobników, których fitness został unieważniony.
        for individual in offspring:
            if not individual.fitness.valid:
                individual.fitness.values = toolbox.evaluate(individual)

        # Aktualizacja najlepszego znalezionego rozwiązania.
        hall_of_fame.update(offspring)

        # Elitaryzm: przeniesienie najlepszych osobników
        # z poprzedniej populacji do następnego pokolenia.
        elites = tools.selBest(population, elite_size)

        remaining = tools.selBest(
            offspring,
            population_size - elite_size,
        )

        population = elites + remaining

        hall_of_fame.update(population)

        record_best(generation)

    best_route = list(hall_of_fame[0])

    best_metrics = calculate_route_metrics(
        graph,
        best_route,
        vehicle
    )

    return GeneticAlgorithmResult(
        best_route=best_route,
        best_time_hours=best_metrics.time_hours,
        best_fuel_liters=best_metrics.fuel_liters,
        best_distance_km=best_metrics.distance_km,
        history=history
    )

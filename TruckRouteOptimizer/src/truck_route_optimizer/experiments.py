
from dataclasses import dataclass
from statistics import fmean, pstdev

from truck_route_optimizer.genetic_algorithm import (
    GeneticAlgorithmResult,
    optimize_route,
)
from truck_route_optimizer.vehicle import Vehicle


@dataclass
class ExperimentResult:
    """
    Wyniki całej serii eksperymentów.

    runs:
        Wyniki poszczególnych uruchomień algorytmu.

    best_result:
        Najlepsze rozwiązanie spośród wszystkich uruchomień.

    aggregate_history:
        Zagregowane statystyki kolejnych pokoleń.
    """

    runs: list[GeneticAlgorithmResult]
    best_result: GeneticAlgorithmResult
    aggregate_history: list[dict]


def run_experiments(
    graph,
    vehicle: Vehicle,
    start_city: str,
    end_city: str,
    runs: int = 10,
    base_seed: int = 0,
    population_size: int = 50,
    generations: int = 100,
    crossover_probability: float = 0.8,
    mutation_probability: float = 0.2,
    elite_size: int = 2,
    tournament_size: int = 3,
) -> ExperimentResult:
    """
    Przeprowadza serię niezależnych eksperymentów
    z wykorzystaniem algorytmu genetycznego.

    Każde uruchomienie otrzymuje inne ziarno generatora
    liczb pseudolosowych.

    Zwraca wyniki poszczególnych uruchomień, najlepsze
    znalezione rozwiązanie oraz statystyki zagregowane.
    """

    if runs < 10:
        raise ValueError(
            "Liczba eksperymentów musi wynosić co najmniej 10."
        )

    if base_seed < 0:
        raise ValueError("Ziarno generatora nie może być ujemne.")

    results = []

    # Niezależne uruchomienia algorytmu.
    for run_number in range(runs):
        seed = base_seed + run_number

        result = optimize_route(
            graph=graph,
            vehicle=vehicle,
            start_city=start_city,
            end_city=end_city,
            population_size=population_size,
            generations=generations,
            crossover_probability=crossover_probability,
            mutation_probability=mutation_probability,
            elite_size=elite_size,
            tournament_size=tournament_size,
            random_seed=seed,
        )

        results.append(result)

    # Najlepsze rozwiązanie ze wszystkich uruchomień.
    # Porównanie jest leksykograficzne:
    # najpierw czas, następnie zużycie paliwa.
    best_result = min(
        results,
        key=lambda result: (
            result.best_time_hours,
            result.best_fuel_liters,
        ),
    )

    # Agregacja statystyk dla każdego pokolenia.
    aggregate_history = []

    for generation in range(generations + 1):
        generation_data = {
            "generation": generation,
        }

        metric_names = (
            "best_time_hours",
            "worst_time_hours",
            "mean_time_hours",
            "best_fuel_liters",
            "worst_fuel_liters",
            "mean_fuel_liters",
        )

        for metric in metric_names:
            values = [
                result.history[generation][metric]
                for result in results
            ]

            generation_data[f"{metric}_mean"] = fmean(values)
            generation_data[f"{metric}_std"] = pstdev(values)

        aggregate_history.append(generation_data)

    return ExperimentResult(
        runs=results,
        best_result=best_result,
        aggregate_history=aggregate_history,
    )


from pathlib import Path
import sys
import time

# Udostępnienie pakietu z katalogu src.
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR / "src"))

from truck_route_optimizer.road_network import create_road_network
from truck_route_optimizer.vehicle import create_vehicle
from truck_route_optimizer.experiments import run_experiments
from truck_route_optimizer.experiment_visualization import (
    save_experiment_results,
)


def main():
    # Konfiguracja eksperymentu.
    parameters = {
        "runs": 10,
        "base_seed": 42,
        "population_size": 50,
        "generations": 100,
        "crossover_probability": 0.8,
        "mutation_probability": 0.2,
        "elite_size": 2,
        "tournament_size": 3,
    }

    start_city = "Warszawa"
    end_city = "Szczecin"

    vehicle = create_vehicle("MAN TGX")
    graph = create_road_network()

    print("=" * 60)
    print("TRUCK ROUTE OPTIMIZER - EKSPERYMENTY")
    print("=" * 60)
    print(f"Trasa: {start_city} -> {end_city}")
    print(f"Pojazd: {vehicle.name}")
    print(f"Liczba uruchomień: {parameters['runs']}")
    print(f"Populacja: {parameters['population_size']}")
    print(f"Liczba pokoleń: {parameters['generations']}")
    print(
        f"Ziarna losowości: {parameters['base_seed']}–"
        f"{parameters['base_seed'] + parameters['runs'] - 1}"
    )
    print("=" * 60)

    start_time = time.perf_counter()

    result = run_experiments(
        graph=graph,
        vehicle=vehicle,
        start_city=start_city,
        end_city=end_city,
        **parameters,
    )

    elapsed_time = time.perf_counter() - start_time

    output_dir = PROJECT_DIR / "experiment_results_szczecin"

    save_experiment_results(
        result=result,
        output_dir=output_dir,
        base_seed=parameters["base_seed"],
        parameters=parameters,
    )

    print("\nEKSPERYMENTY ZAKOŃCZONE")
    print("-" * 60)
    print(f"Najlepsza trasa: {' -> '.join(result.best_result.best_route)}")
    print(f"Czas przejazdu: {result.best_result.best_time_hours:.4f} h")
    print(f"Zużycie paliwa: {result.best_result.best_fuel_liters:.4f} l")
    print(f"Dystans: {result.best_result.best_distance_km:.2f} km")
    print(f"Czas wykonania: {elapsed_time:.2f} s")
    print(f"\nWyniki zapisano w: {output_dir}")


if __name__ == "__main__":
    main()


import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt

from truck_route_optimizer.experiments import ExperimentResult


def _save_metric_plot(
    history: list[dict],
    output_path: Path,
    metric_prefix: str,
    title: str,
    y_label: str,
) -> None:
    """Tworzy wykres statystyk populacji dla wybranej metryki."""

    generations = [item["generation"] for item in history]

    series = (
        ("best", "Najlepszy"),
        ("mean", "Średni"),
        ("worst", "Najgorszy"),
    )

    plt.figure(figsize=(11, 6))

    for statistic, label in series:
        key = f"{statistic}_{metric_prefix}"

        means = [
            item[f"{key}_mean"]
            for item in history
        ]

        deviations = [
            item[f"{key}_std"]
            for item in history
        ]

        lower = [
            mean - deviation
            for mean, deviation in zip(means, deviations)
        ]

        upper = [
            mean + deviation
            for mean, deviation in zip(means, deviations)
        ]

        line, = plt.plot(
            generations,
            means,
            label=label,
            linewidth=2,
        )

        plt.fill_between(
            generations,
            lower,
            upper,
            color=line.get_color(),
            alpha=0.15,
        )

    plt.title(title)
    plt.xlabel("Pokolenie")
    plt.ylabel(y_label)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=150)
    plt.close()


def _save_individual_runs(
    result: ExperimentResult,
    output_dir: Path,
    base_seed: int,
) -> None:
    """Zapisuje szczegółowe wyniki każdego przebiegu."""

    runs_dir = output_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    for index, run in enumerate(result.runs):
        run_data = {
            "run": index + 1,
            "seed": base_seed + index,
            "best_route": run.best_route,
            "best_time_hours": run.best_time_hours,
            "best_fuel_liters": run.best_fuel_liters,
            "best_distance_km": run.best_distance_km,
            "history": run.history,
        }

        run_path = runs_dir / f"run_{index + 1:02d}.json"

        with run_path.open("w", encoding="utf-8") as file:
            json.dump(
                run_data,
                file,
                indent=4,
                ensure_ascii=False,
            )


def save_experiment_results(
    result: ExperimentResult,
    output_dir: str | Path,
    base_seed: int = 0,
    parameters: dict | None = None,
) -> None:
    """
    Zapisuje komplet wyników eksperymentu.

    Generuje:
    - aggregate_history.csv
    - run_summary.csv
    - experiment_config.json
    - best_solution.txt
    - time_results.png
    - fuel_results.png
    - runs/run_XX.json dla każdego przebiegu
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not result.runs:
        raise ValueError("Brak wyników eksperymentów do zapisania.")

    if not result.aggregate_history:
        raise ValueError("Brak zagregowanej historii eksperymentów.")

    # 1. Statystyki kolejnych pokoleń.
    aggregate_path = output_dir / "aggregate_history.csv"

    with aggregate_path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(result.aggregate_history[0].keys()),
        )
        writer.writeheader()
        writer.writerows(result.aggregate_history)

    # 2. Podsumowanie poszczególnych uruchomień.
    summary_path = output_dir / "run_summary.csv"

    with summary_path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        fieldnames = [
            "run",
            "seed",
            "best_time_hours",
            "best_fuel_liters",
            "best_distance_km",
            "best_route",
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for index, run in enumerate(result.runs):
            writer.writerow({
                "run": index + 1,
                "seed": base_seed + index,
                "best_time_hours": run.best_time_hours,
                "best_fuel_liters": run.best_fuel_liters,
                "best_distance_km": run.best_distance_km,
                "best_route": " -> ".join(run.best_route),
            })

    # 3. Pełna konfiguracja eksperymentu.
    config = {
        "runs": len(result.runs),
        "base_seed": base_seed,
        "seeds": [
            base_seed + index
            for index in range(len(result.runs))
        ],
        "parameters": parameters or {},
    }

    config_path = output_dir / "experiment_config.json"

    with config_path.open("w", encoding="utf-8") as file:
        json.dump(
            config,
            file,
            indent=4,
            ensure_ascii=False,
        )

    # 4. Najlepsze rozwiązanie ze wszystkich uruchomień.
    best = result.best_result

    best_run_number = next(
        (
            index + 1
            for index, run in enumerate(result.runs)
            if run is best
        ),
        None,
    )

    best_path = output_dir / "best_solution.txt"

    with best_path.open("w", encoding="utf-8") as file:
        file.write("NAJLEPSZE ROZWIĄZANIE\n")
        file.write("====================\n\n")

        file.write(f"Najlepszy przebieg: {best_run_number}\n")
        file.write(f"Trasa: {' -> '.join(best.best_route)}\n")
        file.write(f"Czas przejazdu: {best.best_time_hours:.4f} h\n")
        file.write(f"Zużycie paliwa: {best.best_fuel_liters:.4f} l\n")
        file.write(f"Dystans: {best.best_distance_km:.2f} km\n")

    # 5. Szczegółowe wyniki każdego przebiegu.
    _save_individual_runs(
        result=result,
        output_dir=output_dir,
        base_seed=base_seed,
    )

    # 6. Wykres czasu przejazdu.
    _save_metric_plot(
        history=result.aggregate_history,
        output_path=output_dir / "time_results.png",
        metric_prefix="time_hours",
        title="Optymalizacja czasu przejazdu",
        y_label="Czas przejazdu [h]",
    )

    # 7. Wykres zużycia paliwa.
    _save_metric_plot(
        history=result.aggregate_history,
        output_path=output_dir / "fuel_results.png",
        metric_prefix="fuel_liters",
        title="Optymalizacja zużycia paliwa",
        y_label="Zużycie paliwa [l]",
    )

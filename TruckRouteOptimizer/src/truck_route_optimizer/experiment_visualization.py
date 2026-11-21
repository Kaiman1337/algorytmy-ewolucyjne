
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


def save_experiment_results(
    result: ExperimentResult,
    output_dir: str | Path,
    base_seed: int = 0,
    parameters: dict | None = None,
) -> None:
    """
    Zapisuje wyniki eksperymentów do plików CSV, JSON i PNG.

    Generuje:
    - aggregate_history.csv
    - run_summary.csv
    - experiment_config.json
    - best_solution.txt
    - time_results.png
    - fuel_results.png
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Statystyki kolejnych pokoleń.
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

    # Podsumowanie poszczególnych uruchomień.
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

    # Parametry eksperymentu.
    config = {
        "runs": len(result.runs),
        "base_seed": base_seed,
        "parameters": parameters or {},
    }

    config_path = output_dir / "experiment_config.json"

    with config_path.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=4, ensure_ascii=False)

    # Najlepsze rozwiązanie ze wszystkich uruchomień.
    best = result.best_result

    best_path = output_dir / "best_solution.txt"

    with best_path.open("w", encoding="utf-8") as file:
        file.write("NAJLEPSZE ROZWIĄZANIE\n")
        file.write("====================\n\n")
        file.write(f"Trasa: {' -> '.join(best.best_route)}\n")
        file.write(f"Czas przejazdu: {best.best_time_hours:.4f} h\n")
        file.write(f"Zużycie paliwa: {best.best_fuel_liters:.4f} l\n")
        file.write(f"Dystans: {best.best_distance_km:.2f} km\n")

    # Wykres czasu przejazdu.
    _save_metric_plot(
        history=result.aggregate_history,
        output_path=output_dir / "time_results.png",
        metric_prefix="time_hours",
        title="Optymalizacja czasu przejazdu",
        y_label="Czas przejazdu [h]",
    )

    # Wykres zużycia paliwa.
    _save_metric_plot(
        history=result.aggregate_history,
        output_path=output_dir / "fuel_results.png",
        metric_prefix="fuel_liters",
        title="Optymalizacja zużycia paliwa",
        y_label="Zużycie paliwa [l]",
    )

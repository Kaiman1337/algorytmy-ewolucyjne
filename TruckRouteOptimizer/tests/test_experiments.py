import sys
from pathlib import Path
import unittest
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from truck_route_optimizer.experiments import run_experiments

class TestExperiments(unittest.TestCase):

    def setUp(self):
        self.graph = object()
        self.vehicle = object()

    def create_mock_result(self, seed, generations):
        """
        Tworzy przykładowy wynik pojedynczego uruchomienia.
        Wartości zależą od ziarna, aby można było sprawdzić
        poprawność agregacji statystyk.
        """
        history = []

        for generation in range(generations + 1):
            history.append({
                "generation": generation,
                "time_hours": 20.0 - seed,
                "fuel_liters": 100.0 + seed,

                "best_time_hours": 20.0 - seed,
                "worst_time_hours": 30.0 - seed,
                "mean_time_hours": 25.0 - seed,

                "best_fuel_liters": 100.0 + seed,
                "worst_fuel_liters": 120.0 + seed,
                "mean_fuel_liters": 110.0 + seed,

                "std_time_hours": 1.0,
                "std_fuel_liters": 2.0,
            })

        return SimpleNamespace(
            best_route=["Warszawa", "Kraków"],
            best_time_hours=20.0 - seed,
            best_fuel_liters=100.0 + seed,
            best_distance_km=300.0,
            history=history,
        )

    @patch("truck_route_optimizer.experiments.optimize_route")
    def test_runs_at_least_ten_experiments(self, mock_optimize):
        mock_optimize.side_effect = lambda **kwargs: (
            self.create_mock_result(
                kwargs["random_seed"],
                kwargs["generations"],
            )
        )

        result = run_experiments(
            graph=self.graph,
            vehicle=self.vehicle,
            start_city="Warszawa",
            end_city="Kraków",
            runs=10,
            generations=5,
        )

        self.assertEqual(len(result.runs), 10)
        self.assertEqual(mock_optimize.call_count, 10)

    @patch("truck_route_optimizer.experiments.optimize_route")
    def test_each_run_uses_different_seed(self, mock_optimize):
        mock_optimize.side_effect = lambda **kwargs: (
            self.create_mock_result(
                kwargs["random_seed"],
                kwargs["generations"],
            )
        )

        run_experiments(
            graph=self.graph,
            vehicle=self.vehicle,
            start_city="Warszawa",
            end_city="Kraków",
            runs=10,
            base_seed=100,
            generations=5,
        )

        seeds = [
            call.kwargs["random_seed"]
            for call in mock_optimize.call_args_list
        ]

        self.assertEqual(seeds, list(range(100, 110)))
        self.assertEqual(len(set(seeds)), 10)

    @patch("truck_route_optimizer.experiments.optimize_route")
    def test_selects_best_result(self, mock_optimize):
        mock_optimize.side_effect = lambda **kwargs: (
            self.create_mock_result(
                kwargs["random_seed"],
                kwargs["generations"],
            )
        )

        result = run_experiments(
            graph=self.graph,
            vehicle=self.vehicle,
            start_city="Warszawa",
            end_city="Kraków",
            runs=10,
            generations=5,
        )

        self.assertEqual(result.best_result.best_time_hours, 11.0)
        self.assertEqual(result.best_result.best_fuel_liters, 109.0)

    @patch("truck_route_optimizer.experiments.optimize_route")
    def test_aggregates_generation_statistics(self, mock_optimize):
        mock_optimize.side_effect = lambda **kwargs: (
            self.create_mock_result(
                kwargs["random_seed"],
                kwargs["generations"],
            )
        )

        result = run_experiments(
            graph=self.graph,
            vehicle=self.vehicle,
            start_city="Warszawa",
            end_city="Kraków",
            runs=10,
            generations=5,
        )

        self.assertEqual(len(result.aggregate_history), 6)

        generation = result.aggregate_history[0]

        self.assertEqual(generation["generation"], 0)

        self.assertAlmostEqual(
            generation["best_time_hours_mean"],
            15.5,
        )

        self.assertAlmostEqual(
            generation["best_time_hours_std"],
            2.872281323,
            places=6,
        )

        self.assertAlmostEqual(
            generation["mean_fuel_liters_mean"],
            114.5,
        )

        self.assertAlmostEqual(
            generation["best_fuel_liters_mean"],
            104.5,
        )

    def test_rejects_fewer_than_ten_runs(self):
        with self.assertRaises(ValueError):
            run_experiments(
                graph=self.graph,
                vehicle=self.vehicle,
                start_city="Warszawa",
                end_city="Kraków",
                runs=9,
            )

    def test_rejects_negative_base_seed(self):
        with self.assertRaises(ValueError):
            run_experiments(
                graph=self.graph,
                vehicle=self.vehicle,
                start_city="Warszawa",
                end_city="Kraków",
                runs=10,
                base_seed=-1,
            )


if __name__ == "__main__":
    unittest.main()

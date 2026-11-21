import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from truck_route_optimizer.road_network import create_road_network
from truck_route_optimizer.vehicle import create_vehicle
from truck_route_optimizer.route_validator import validate_route
from truck_route_optimizer.genetic_algorithm import optimize_route


class TestGeneticAlgorithm(unittest.TestCase):

    def setUp(self):
        self.graph = create_road_network()
        self.vehicle = create_vehicle("MAN TGX")

    def test_optimize_route_returns_valid_result(self):
        result = optimize_route(
            graph=self.graph,
            vehicle=self.vehicle,
            start_city="Warszawa",
            end_city="Kraków",
            population_size=10,
            generations=10,
            random_seed=42,
        )

        self.assertEqual(result.best_route[0], "Warszawa")
        self.assertEqual(result.best_route[-1], "Kraków")

        valid, message = validate_route(
            self.graph,
            result.best_route,
            self.vehicle,
        )

        self.assertTrue(valid, message)
        self.assertGreater(result.best_time_hours, 0)
        self.assertGreater(result.best_fuel_liters, 0)

    def test_history_contains_all_generations(self):
        generations = 10

        result = optimize_route(
            graph=self.graph,
            vehicle=self.vehicle,
            start_city="Warszawa",
            end_city="Kraków",
            population_size=10,
            generations=generations,
            random_seed=42,
        )

        self.assertEqual(len(result.history), generations + 1)
        self.assertEqual(result.history[0]["generation"], 0)
        self.assertEqual(
            result.history[-1]["generation"],
            generations,
        )

    def test_best_result_does_not_get_worse(self):
        result = optimize_route(
            graph=self.graph,
            vehicle=self.vehicle,
            start_city="Warszawa",
            end_city="Kraków",
            population_size=10,
            generations=20,
            random_seed=42,
        )

        for previous, current in zip(
            result.history,
            result.history[1:],
        ):
            previous_fitness = (
                previous["time_hours"],
                previous["fuel_liters"],
            )

            current_fitness = (
                current["time_hours"],
                current["fuel_liters"],
            )

            self.assertLessEqual(
                current_fitness,
                previous_fitness,
            )

    def test_invalid_population_size_raises_error(self):
        with self.assertRaises(ValueError):
            optimize_route(
                graph=self.graph,
                vehicle=self.vehicle,
                start_city="Warszawa",
                end_city="Kraków",
                population_size=1,
            )

    def test_invalid_generation_count_raises_error(self):
        with self.assertRaises(ValueError):
            optimize_route(
                graph=self.graph,
                vehicle=self.vehicle,
                start_city="Warszawa",
                end_city="Kraków",
                generations=0,
            )

    def test_invalid_elite_size_raises_error(self):
        with self.assertRaises(ValueError):
            optimize_route(
                graph=self.graph,
                vehicle=self.vehicle,
                start_city="Warszawa",
                end_city="Kraków",
                population_size=10,
                elite_size=10,
            )


if __name__ == "__main__":
    unittest.main()

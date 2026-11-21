import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from truck_route_optimizer.road_network import create_road_network
from truck_route_optimizer.vehicle import create_vehicle
from truck_route_optimizer.route_validator import validate_route
from truck_route_optimizer.route_operators import (
    generate_random_route,
    crossover_routes,
    mutate_route,
)


class TestRouteOperators(unittest.TestCase):

    def setUp(self):
        self.graph = create_road_network()
        self.vehicle = create_vehicle("MAN TGX")
        self.start = "Warszawa"
        self.end = "Kraków"

    def test_generate_random_route(self):
        route = generate_random_route(
            self.graph,
            self.vehicle,
            self.start,
            self.end,
        )

        self.assertEqual(route[0], self.start)
        self.assertEqual(route[-1], self.end)
        self.assertEqual(len(route), len(set(route)))

        valid, message = validate_route(
            self.graph,
            route,
            self.vehicle,
        )

        self.assertTrue(valid, message)

    def test_generate_route_with_unknown_city(self):
        with self.assertRaises(ValueError):
            generate_random_route(
                self.graph,
                self.vehicle,
                "Nieznane miasto",
                self.end,
            )

    def test_crossover_routes(self):
        parent1 = [
            "Warszawa",
            "Łódź",
            "Katowice",
            "Kraków",
        ]

        parent2 = [
            "Warszawa",
            "Katowice",
            "Kraków",
        ]

        child1, child2 = crossover_routes(
            self.graph,
            self.vehicle,
            parent1,
            parent2,
        )

        for child in (child1, child2):
            self.assertEqual(child[0], self.start)
            self.assertEqual(child[-1], self.end)
            self.assertEqual(len(child), len(set(child)))

            valid, message = validate_route(
                self.graph,
                child,
                self.vehicle,
            )

            self.assertTrue(valid, message)

    def test_crossover_without_common_intermediate_city(self):
        parent1 = [
            "Warszawa",
            "Łódź",
            "Katowice",
            "Kraków",
        ]

        parent2 = [
            "Warszawa",
            "Poznań",
            "Wrocław",
            "Kraków",
        ]

        child1, child2 = crossover_routes(
            self.graph,
            self.vehicle,
            parent1,
            parent2,
        )

        self.assertEqual(child1, parent1)
        self.assertEqual(child2, parent2)

    def test_crossover_with_different_endpoints_raises_error(self):
        parent1 = ["Warszawa", "Łódź", "Kraków"]
        parent2 = ["Gdańsk", "Poznań", "Szczecin"]

        with self.assertRaises(ValueError):
            crossover_routes(
                self.graph,
                self.vehicle,
                parent1,
                parent2,
            )

    def test_mutate_route(self):
        route = [
            "Warszawa",
            "Łódź",
            "Katowice",
            "Kraków",
        ]

        mutated_route = mutate_route(
            self.graph,
            self.vehicle,
            route,
        )

        self.assertEqual(mutated_route[0], self.start)
        self.assertEqual(mutated_route[-1], self.end)
        self.assertEqual(
            len(mutated_route),
            len(set(mutated_route)),
        )

        valid, message = validate_route(
            self.graph,
            mutated_route,
            self.vehicle,
        )

        self.assertTrue(valid, message)

    def test_mutation_does_not_change_short_route(self):
        route = ["Warszawa", "Kraków"]

        mutated_route = mutate_route(
            self.graph,
            self.vehicle,
            route,
        )

        self.assertEqual(mutated_route, route)


if __name__ == "__main__":
    unittest.main()

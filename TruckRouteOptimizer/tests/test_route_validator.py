import sys
from pathlib import Path
import unittest

import networkx as nx

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from truck_route_optimizer.route_validator import validate_route
from truck_route_optimizer.vehicle import create_vehicle


class TestRouteValidator(unittest.TestCase):

    def setUp(self):
        self.graph = nx.DiGraph()

        road = {
            "distance_km": 100,
            "speed_limit_kmh": 100,
            "max_weight_t": 40,
            "max_height_m": 4.2,
            "max_width_m": 2.6,
            "max_length_m": 18.75,
            "closed": False,
        }

        self.graph.add_edge("Warszawa", "Łódź", **road)
        self.graph.add_edge("Łódź", "Wrocław", **road)

        self.vehicle = create_vehicle("MAN TGX")

    def test_valid_route(self):
        valid, message = validate_route(
            self.graph,
            ["Warszawa", "Łódź", "Wrocław"],
            self.vehicle,
        )

        self.assertTrue(valid)
        self.assertEqual(message, "Cała trasa jest przejezdna.")

    def test_route_with_unknown_city(self):
        valid, message = validate_route(
            self.graph,
            ["Warszawa", "Gdańsk"],
            self.vehicle,
        )

        self.assertFalse(valid)
        self.assertIn("nie istnieje w grafie", message)

    def test_route_without_connection(self):
        valid, message = validate_route(
            self.graph,
            ["Warszawa", "Wrocław"],
            self.vehicle,
        )

        self.assertFalse(valid)
        self.assertIn("Brak połączenia drogowego", message)

    def test_route_with_restricted_road(self):
        self.graph["Warszawa"]["Łódź"]["max_weight_t"] = 30

        valid, message = validate_route(
            self.graph,
            ["Warszawa", "Łódź"],
            self.vehicle,
        )

        self.assertFalse(valid)
        self.assertIn("nie może przejechać", message)

    def test_route_with_closed_road(self):
        self.graph["Łódź"]["Wrocław"]["closed"] = True

        valid, message = validate_route(
            self.graph,
            ["Warszawa", "Łódź", "Wrocław"],
            self.vehicle,
        )

        self.assertFalse(valid)
        self.assertIn("Łódź -> Wrocław", message)

    def test_route_with_less_than_two_cities(self):
        valid, message = validate_route(
            self.graph,
            ["Warszawa"],
            self.vehicle,
        )

        self.assertFalse(valid)
        self.assertIn("co najmniej dwa miasta", message)


if __name__ == "__main__":
    unittest.main()

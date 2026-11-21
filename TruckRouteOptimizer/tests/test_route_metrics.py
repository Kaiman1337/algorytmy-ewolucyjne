
import sys
import unittest
from pathlib import Path

import networkx as nx

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from truck_route_optimizer.route_metrics import calculate_route_metrics
from truck_route_optimizer.vehicle import create_vehicle


class TestRouteMetrics(unittest.TestCase):

    def setUp(self):
        self.graph = nx.DiGraph()

        road = {
            "distance_km": 100,
            "speed_limit_kmh": 100,
            "max_weight_t": 40,
            "max_height_m": 4.2,
            "max_width_m": 2.6,
            "max_length_m": 18.75,
            "traffic_factor": 1.0,
            "roadworks_factor": 1.0,
            "closed": False,
        }

        self.graph.add_edge("Warszawa", "Łódź", **road)
        self.graph.add_edge("Łódź", "Wrocław", **road)

        self.vehicle = create_vehicle("MAN TGX")

    def test_calculate_basic_metrics(self):
        metrics = calculate_route_metrics(
            self.graph,
            ["Warszawa", "Łódź", "Wrocław"],
            self.vehicle,
        )

        self.assertAlmostEqual(metrics.distance_km, 200)
        self.assertAlmostEqual(metrics.time_hours, 2)
        self.assertAlmostEqual(metrics.fuel_liters, 56)

    def test_calculate_metrics_with_traffic(self):
        self.graph["Warszawa"]["Łódź"]["traffic_factor"] = 2.0

        metrics = calculate_route_metrics(
            self.graph,
            ["Warszawa", "Łódź"],
            self.vehicle,
        )

        self.assertAlmostEqual(metrics.time_hours, 2)
        self.assertAlmostEqual(metrics.distance_km, 100)

    def test_calculate_metrics_with_roadworks(self):
        self.graph["Warszawa"]["Łódź"]["roadworks_factor"] = 2.0

        metrics = calculate_route_metrics(
            self.graph,
            ["Warszawa", "Łódź"],
            self.vehicle,
        )

        self.assertAlmostEqual(metrics.time_hours, 2)

    def test_invalid_route_raises_error(self):
        with self.assertRaises(ValueError):
            calculate_route_metrics(
                self.graph,
                ["Warszawa", "Gdańsk"],
                self.vehicle,
            )

    def test_invalid_speed_limit_raises_error(self):
        self.graph["Warszawa"]["Łódź"]["speed_limit_kmh"] = 0

        with self.assertRaises(ValueError):
            calculate_route_metrics(
                self.graph,
                ["Warszawa", "Łódź"],
                self.vehicle,
            )


if __name__ == "__main__":
    unittest.main()

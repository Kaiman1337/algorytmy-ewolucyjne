import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from truck_route_optimizer.vehicle import (
    Vehicle,
    create_vehicle,
    create_custom_vehicle,
    get_available_profiles,
)


class TestVehicle(unittest.TestCase):

    def test_available_profiles(self):
        profiles = get_available_profiles()

        self.assertIn("MAN TGX", profiles)
        self.assertIn("Lekka ciężarówka", profiles)
        self.assertIn("Zestaw ciężarowy", profiles)

    def test_create_vehicle(self):
        vehicle = create_vehicle("MAN TGX")

        self.assertEqual(vehicle.name, "MAN TGX")
        self.assertEqual(vehicle.gross_weight_kg, 35000)
        self.assertEqual(vehicle.available_payload_kg, 5000)

    def test_change_payload(self):
        vehicle = create_vehicle("MAN TGX", payload_kg=24000)

        self.assertEqual(vehicle.payload_kg, 24000)
        self.assertEqual(vehicle.gross_weight_kg, 39000)

    def test_exceed_gross_weight(self):
        with self.assertRaises(ValueError):
            create_vehicle("MAN TGX", payload_kg=26000)

    def test_unknown_profile(self):
        with self.assertRaises(ValueError):
            create_vehicle("Nieistniejący pojazd")

    def test_custom_vehicle(self):
        vehicle = create_custom_vehicle(
            name="Moja ciężarówka",
            curb_weight_kg=12000,
            max_gross_weight_kg=40000,
            payload_kg=20000,
            height_m=3.9,
            width_m=2.5,
            length_m=16.5,
            fuel_consumption_l_100km=27.0,
        )

        self.assertEqual(vehicle.gross_weight_kg, 32000)

    def test_negative_payload(self):
        with self.assertRaises(ValueError):
            create_vehicle("MAN TGX", payload_kg=-1000)

    def test_invalid_dimensions(self):
        vehicle = Vehicle(
            name="Niepoprawna ciężarówka",
            curb_weight_kg=12000,
            max_gross_weight_kg=40000,
            payload_kg=10000,
            height_m=-1,
            width_m=2.5,
            length_m=16.5,
            fuel_consumption_l_100km=27,
        )

        with self.assertRaises(ValueError):
            vehicle.validate()

    def test_vehicle_can_traverse_valid_road(self):
        vehicle = create_vehicle("MAN TGX")

        road = {
            "closed": False,
            "max_weight_t": 40,
            "max_height_m": 4.2,
            "max_width_m": 2.6,
            "max_length_m": 18.75,
        }

        self.assertTrue(vehicle.can_traverse(road))

    def test_vehicle_cannot_traverse_road_with_weight_limit(self):
        vehicle = create_vehicle("MAN TGX")

        road = {
            "max_weight_t": 34.9,
            "max_height_m": 4.2,
            "max_width_m": 2.6,
            "max_length_m": 18.75,
        }

        self.assertFalse(vehicle.can_traverse(road))

    def test_vehicle_cannot_traverse_road_with_height_limit(self):
        vehicle = create_vehicle("MAN TGX")

        road = {
            "max_weight_t": 40,
            "max_height_m": 3.9,
            "max_width_m": 2.6,
            "max_length_m": 18.75,
        }

        self.assertFalse(vehicle.can_traverse(road))

    def test_vehicle_cannot_traverse_road_with_width_limit(self):
        vehicle = create_vehicle("MAN TGX")

        road = {
            "max_weight_t": 40,
            "max_height_m": 4.2,
            "max_width_m": 2.5,
            "max_length_m": 18.75,
        }

        self.assertFalse(vehicle.can_traverse(road))

    def test_vehicle_cannot_traverse_road_with_length_limit(self):
        vehicle = create_vehicle("MAN TGX")

        road = {
            "max_weight_t": 40,
            "max_height_m": 4.2,
            "max_width_m": 2.6,
            "max_length_m": 16.0,
        }

        self.assertFalse(vehicle.can_traverse(road))

    def test_vehicle_cannot_traverse_closed_road(self):
        vehicle = create_vehicle("MAN TGX")

        road = {
            "closed": True,
            "max_weight_t": 40,
            "max_height_m": 4.2,
            "max_width_m": 2.6,
            "max_length_m": 18.75,
        }

        self.assertFalse(vehicle.can_traverse(road))


if __name__ == "__main__":
    unittest.main()

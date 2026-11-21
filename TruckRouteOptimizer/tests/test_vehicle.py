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


if __name__ == "__main__":
    unittest.main()

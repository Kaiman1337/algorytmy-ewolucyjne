from dataclasses import dataclass

@dataclass
class Vehicle:
    """Model ciężarówki wykorzystywany w symulacji."""

    name: str
    curb_weight_kg: float
    max_gross_weight_kg: float
    payload_kg: float
    height_m: float
    width_m: float
    length_m: float
    fuel_consumption_l_100km: float

    @property
    def gross_weight_kg(self) -> float:
        """Rzeczywista masa całkowita pojazdu."""
        return self.curb_weight_kg + self.payload_kg

    @property
    def available_payload_kg(self) -> float:
        """Pozostała dopuszczalna ładowność."""
        return self.max_gross_weight_kg - self.gross_weight_kg

    def validate(self) -> None:
        """Sprawdza poprawność parametrów pojazdu."""

        if not self.name.strip():
            raise ValueError("Nazwa pojazdu nie może być pusta.")

        positive_values = {
            "Masa własna": self.curb_weight_kg,
            "DMC": self.max_gross_weight_kg,
            "Wysokość": self.height_m,
            "Szerokość": self.width_m,
            "Długość": self.length_m,
            "Spalanie": self.fuel_consumption_l_100km,
        }

        for parameter, value in positive_values.items():
            if value <= 0:
                raise ValueError(f"{parameter} musi być większa od zera.")

        if self.payload_kg < 0:
            raise ValueError("Masa ładunku nie może być ujemna.")

        if self.curb_weight_kg >= self.max_gross_weight_kg:
            raise ValueError("Masa własna musi być mniejsza od DMC.")

        if self.gross_weight_kg > self.max_gross_weight_kg:
            raise ValueError("Przekroczono dopuszczalną masę całkowitą.")

    def get_information(self) -> str:
        """Zwraca czytelne informacje o pojeździe."""

        return (
            f"Pojazd: {self.name}\n"
            f"Masa własna: {self.curb_weight_kg:.0f} kg\n"
            f"Ładunek: {self.payload_kg:.0f} kg\n"
            f"Masa całkowita: {self.gross_weight_kg:.0f} kg\n"
            f"DMC: {self.max_gross_weight_kg:.0f} kg\n"
            f"Wysokość: {self.height_m:.2f} m\n"
            f"Szerokość: {self.width_m:.2f} m\n"
            f"Długość: {self.length_m:.2f} m\n"
            f"Spalanie: {self.fuel_consumption_l_100km:.1f} l/100 km"
        )


# Przykładowe profile pojazdów do symulacji.
VEHICLE_PROFILES = {
    "MAN TGX": {
        "curb_weight_kg": 15000,
        "max_gross_weight_kg": 40000,
        "payload_kg": 20000,
        "height_m": 4.0,
        "width_m": 2.55,
        "length_m": 16.5,
        "fuel_consumption_l_100km": 28.0,
    },
    "Lekka ciężarówka": {
        "curb_weight_kg": 7500,
        "max_gross_weight_kg": 18000,
        "payload_kg": 9000,
        "height_m": 3.5,
        "width_m": 2.45,
        "length_m": 10.0,
        "fuel_consumption_l_100km": 19.0,
    },
    "Zestaw ciężarowy": {
        "curb_weight_kg": 15000,
        "max_gross_weight_kg": 40000,
        "payload_kg": 25000,
        "height_m": 4.0,
        "width_m": 2.55,
        "length_m": 18.75,
        "fuel_consumption_l_100km": 31.0,
    },
}


def get_available_profiles() -> list[str]:
    """Zwraca nazwy dostępnych profili."""
    return list(VEHICLE_PROFILES.keys())


def create_vehicle(
    profile_name: str,
    payload_kg: float | None = None,
) -> Vehicle:
    """Tworzy pojazd na podstawie gotowego profilu."""

    if profile_name not in VEHICLE_PROFILES:
        raise ValueError(f"Nieznany profil pojazdu: {profile_name}")

    parameters = VEHICLE_PROFILES[profile_name].copy()

    if payload_kg is not None:
        parameters["payload_kg"] = payload_kg

    vehicle = Vehicle(name=profile_name, **parameters)
    vehicle.validate()

    return vehicle


def create_custom_vehicle(
    name: str,
    curb_weight_kg: float,
    max_gross_weight_kg: float,
    payload_kg: float,
    height_m: float,
    width_m: float,
    length_m: float,
    fuel_consumption_l_100km: float,
) -> Vehicle:
    """Tworzy pojazd o parametrach podanych przez użytkownika."""

    vehicle = Vehicle(
        name=name,
        curb_weight_kg=curb_weight_kg,
        max_gross_weight_kg=max_gross_weight_kg,
        payload_kg=payload_kg,
        height_m=height_m,
        width_m=width_m,
        length_m=length_m,
        fuel_consumption_l_100km=fuel_consumption_l_100km,
    )

    vehicle.validate()
    return vehicle


from dataclasses import dataclass
from networkx import DiGraph

from truck_route_optimizer.route_validator import validate_route
from truck_route_optimizer.vehicle import Vehicle


# Poziom robót drogowych i odpowiadający mu mnożnik czasu przejazdu.
ROADWORKS_FACTORS = {
    0: 1.0,
    1: 1.1,
    2: 1.2,
    3: 1.4,
    4: 1.7,
    5: 2.0,
}


@dataclass
class RouteMetrics:
    """Parametry obliczonej trasy."""

    distance_km: float
    time_hours: float
    fuel_liters: float


def calculate_route_metrics(
    graph: DiGraph,
    route: list[str],
    vehicle: Vehicle,
) -> RouteMetrics:
    """Oblicza dystans, czas przejazdu i zużycie paliwa."""

    valid, message = validate_route(graph, route, vehicle)

    if not valid:
        raise ValueError(message)

    total_distance = 0.0
    total_time = 0.0

    for start, end in zip(route, route[1:]):
        road = graph.get_edge_data(start, end)

        distance = road["distance_km"]
        speed_limit = road["speed_limit_kmh"]

        traffic_factor = road.get("traffic_factor", 1.0)

        if "roadworks_level" in road:
            roadworks_level = road["roadworks_level"]

            if (
                not isinstance(roadworks_level, int)
                or isinstance(roadworks_level, bool)
                or roadworks_level not in ROADWORKS_FACTORS
            ):
                raise ValueError(
                    f"Nieprawidłowy poziom robót drogowych: "
                    f"{start} -> {end}."
                )

            roadworks_factor = ROADWORKS_FACTORS[roadworks_level]
        else:
            # Kompatybilność ze starszymi danymi dróg.
            roadworks_factor = road.get("roadworks_factor", 1.0)

        if speed_limit <= 0:
            raise ValueError(
                f"Nieprawidłowe ograniczenie prędkości: {start} -> {end}."
            )

        if traffic_factor <= 0 or roadworks_factor <= 0:
            raise ValueError(
                f"Nieprawidłowy współczynnik utrudnień: {start} -> {end}."
            )

        effective_speed = speed_limit / (
            traffic_factor * roadworks_factor
        )

        total_distance += distance
        total_time += distance / effective_speed

    fuel_consumption = (
        total_distance * vehicle.fuel_consumption_l_100km / 100
    )

    return RouteMetrics(
        distance_km=total_distance,
        time_hours=total_time,
        fuel_liters=fuel_consumption,
    )

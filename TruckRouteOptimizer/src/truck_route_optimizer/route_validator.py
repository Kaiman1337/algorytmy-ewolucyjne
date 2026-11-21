
from networkx import DiGraph

from truck_route_optimizer.vehicle import Vehicle


def validate_route(
    graph: DiGraph,
    route: list[str],
    vehicle: Vehicle,
) -> tuple[bool, str]:
    """Sprawdza, czy pojazd może przejechać całą trasę."""

    if len(route) < 2:
        return False, "Trasa musi zawierać co najmniej dwa miasta."

    # Sprawdzenie, czy wszystkie miasta istnieją w grafie.
    for city in route:
        if city not in graph:
            return False, f"Miasto '{city}' nie istnieje w grafie."

    # Sprawdzenie każdego odcinka trasy.
    for start, end in zip(route, route[1:]):
        if not graph.has_edge(start, end):
            return False, f"Brak połączenia drogowego: {start} -> {end}."

        road = graph.get_edge_data(start, end)

        if not vehicle.can_traverse(road):
            return False, (
                f"Pojazd '{vehicle.name}' nie może przejechać "
                f"odcinka {start} -> {end}."
            )

    return True, "Cała trasa jest przejezdna."

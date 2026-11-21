import random
import networkx as nx

from truck_route_optimizer.route_validator import validate_route
from truck_route_optimizer.vehicle import Vehicle


def _find_random_path(
    graph: nx.DiGraph,
    vehicle: Vehicle,
    start_city: str,
    end_city: str,
    forbidden_nodes: set[str] | None = None,
) -> list[str] | None:
    """
    Szuka losowej, poprawnej trasy między dwoma miastami.

    Wyszukiwanie wykorzystuje losową kolejność sąsiadów oraz
    nie pozwala odwiedzać tego samego miasta więcej niż raz.
    """
    if start_city not in graph or end_city not in graph:
        return None

    if start_city == end_city:
        return None

    forbidden = set(forbidden_nodes or set())
    forbidden.discard(start_city)
    forbidden.discard(end_city)

    def search(current_city: str, path: list[str]) -> list[str] | None:
        if current_city == end_city:
            return path.copy()

        neighbors = list(graph.successors(current_city))
        random.shuffle(neighbors)

        for next_city in neighbors:
            if next_city in path or next_city in forbidden:
                continue

            road = graph.get_edge_data(current_city, next_city)

            if not vehicle.can_traverse(road):
                continue

            result = search(next_city, path + [next_city])

            if result is not None:
                return result

        return None

    return search(start_city, [start_city])


def generate_random_route(
    graph: nx.DiGraph,
    vehicle: Vehicle,
    start_city: str,
    end_city: str,
) -> list[str]:
    """
    Generuje losową trasę spełniającą ograniczenia grafu i pojazdu.

    Zwraca listę miast od punktu początkowego do docelowego.
    Jeśli nie istnieje poprawna trasa, zgłasza ValueError.
    """
    route = _find_random_path(
        graph=graph,
        vehicle=vehicle,
        start_city=start_city,
        end_city=end_city,
    )

    if route is None:
        raise ValueError(
            f"Nie znaleziono poprawnej trasy: {start_city} -> {end_city}."
        )

    return route


def crossover_routes(
    graph: nx.DiGraph,
    vehicle: Vehicle,
    parent1: list[str],
    parent2: list[str],
) -> tuple[list[str], list[str]]:
    """
    Krzyżuje dwie trasy w losowo wybranym wspólnym mieście.

    Początek i koniec tras pozostają niezmienione.
    Jeśli utworzone dziecko jest niepoprawne, zachowywany jest rodzic.
    """
    if (
        len(parent1) < 2
        or len(parent2) < 2
        or parent1[0] != parent2[0]
        or parent1[-1] != parent2[-1]
    ):
        raise ValueError(
            "Rodzice muszą mieć ten sam punkt początkowy i docelowy."
        )

    common_cities = list(
        set(parent1[1:-1]) & set(parent2[1:-1])
    )

    if not common_cities:
        return parent1.copy(), parent2.copy()

    crossover_city = random.choice(common_cities)

    index1 = parent1.index(crossover_city)
    index2 = parent2.index(crossover_city)

    child1 = parent1[:index1 + 1] + parent2[index2 + 1:]
    child2 = parent2[:index2 + 1] + parent1[index1 + 1:]

    def is_valid_child(route: list[str]) -> bool:
        if len(route) != len(set(route)):
            return False

        valid, _ = validate_route(graph, route, vehicle)
        return valid

    if not is_valid_child(child1):
        child1 = parent1.copy()

    if not is_valid_child(child2):
        child2 = parent2.copy()

    return child1, child2


def mutate_route(
    graph: nx.DiGraph,
    vehicle: Vehicle,
    route: list[str],
) -> list[str]:
    """
    Mutuje trasę poprzez zastąpienie jej fragmentu inną poprawną drogą.

    Miasta początkowe i docelowe pozostają bez zmian.
    Nowy fragment nie może powodować powtarzania miast.
    Jeśli nie uda się znaleźć alternatywy, zwracana jest oryginalna trasa.
    """
    if len(route) < 3:
        return route.copy()

    possible_segments = [
        (start_index, end_index)
        for start_index in range(len(route) - 1)
        for end_index in range(start_index + 1, len(route))
    ]

    random.shuffle(possible_segments)

    for start_index, end_index in possible_segments:
        start_city = route[start_index]
        end_city = route[end_index]

        forbidden_nodes = set(route) - {start_city, end_city}

        alternative_path = _find_random_path(
            graph=graph,
            vehicle=vehicle,
            start_city=start_city,
            end_city=end_city,
            forbidden_nodes=forbidden_nodes,
        )

        if alternative_path is None:
            continue

        original_segment = route[start_index:end_index + 1]

        if alternative_path == original_segment:
            continue

        mutated_route = (
            route[:start_index]
            + alternative_path
            + route[end_index + 1:]
        )

        if len(mutated_route) != len(set(mutated_route)):
            continue

        valid, _ = validate_route(graph, mutated_route, vehicle)

        if valid:
            return mutated_route

    return route.copy()

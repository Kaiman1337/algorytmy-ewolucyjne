import networkx as nx


def create_road_network():
    """
    Tworzy symulowaną sieć dróg pomiędzy polskimi miastami.

    Każda krawędź reprezentuje odcinek drogi.
    Graf jest skierowany, aby umożliwić uwzględnienie
    dróg jednokierunkowych i różnych parametrów przejazdu.
    """

    graph = nx.DiGraph()

    # Współrzędne służą wyłącznie do wizualizacji.
    cities = {
        "Warszawa": (0, 5),
        "Gdańsk": (1, 8),
        "Szczecin": (-5, 6),
        "Poznań": (-3, 4),
        "Łódź": (0, 3),
        "Wrocław": (-4, 1),
        "Katowice": (0, 0),
        "Kraków": (2, -1),
    }

    for city, position in cities.items():
        graph.add_node(city, pos=position)

    # start, koniec, dystans, prędkość, DMC, wysokość, szerokość, długość, typ drogi
    roads = [
        ("Warszawa", "Gdańsk", 340, 120, 40, 4.2, 2.6, 18.75, "highway"),
        ("Warszawa", "Łódź", 130, 120, 40, 4.2, 2.6, 18.75, "highway"),
        ("Warszawa", "Poznań", 310, 120, 40, 4.2, 2.6, 18.75, "highway"),
        ("Warszawa", "Katowice", 290, 110, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Gdańsk", "Poznań", 300, 100, 40, 4.0, 2.6, 18.75, "national"),
        ("Poznań", "Szczecin", 270, 100, 40, 4.2, 2.6, 18.75, "expressway"),
        ("Poznań", "Wrocław", 180, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Poznań", "Łódź", 200, 100, 40, 4.0, 2.6, 18.75, "national"),
        ("Łódź", "Wrocław", 220, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Łódź", "Katowice", 180, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Wrocław", "Katowice", 170, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Katowice", "Kraków", 80, 100, 40, 4.0, 2.6, 18.75, "highway"),
        ("Warszawa", "Kraków", 300, 120, 40, 4.2, 2.6, 18.75, "expressway"),
    ]

    for road in roads:
        (
            start,
            end,
            distance,
            speed,
            max_weight,
            max_height,
            max_width,
            max_length,
            road_type,
        ) = road

        road_data = {
            "distance_km": distance,
            "speed_limit_kmh": speed,
            "max_weight_t": max_weight,
            "max_height_m": max_height,
            "max_width_m": max_width,
            "max_length_m": max_length,
            "road_type": road_type,
            "closed": False,
            "traffic_factor": 1.0,
            "roadworks_factor": 1.0,
        }

        # Domyślnie drogi są dwukierunkowe.
        graph.add_edge(start, end, **road_data)
        graph.add_edge(end, start, **road_data.copy())

    return graph

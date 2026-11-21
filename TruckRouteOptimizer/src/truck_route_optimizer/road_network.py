
import networkx as nx


def create_road_network():
    """
    Tworzy symulowaną sieć drogową obejmującą 33 polskie miasta.

    Każdy fizyczny odcinek jest reprezentowany przez dwie krawędzie
    skierowane, dzięki czemu domyślnie drogi są dwukierunkowe.

    Współrzędne miast są schematyczne i służą wyłącznie wizualizacji.
    Nie są rzeczywistymi współrzędnymi geograficznymi.
    """

    graph = nx.DiGraph()

    # Schematyczne rozmieszczenie miast na mapie Polski.
    # Oś X: zachód -> wschód.
    # Oś Y: południe -> północ.
    cities = {
        # Północny zachód
        "Szczecin": (-6.0, 6.0),
        "Koszalin": (-4.2, 6.8),
        "Słupsk": (-2.7, 7.0),
        "Gdynia": (-1.2, 7.2),
        "Gdańsk": (-0.3, 6.7),

        # Północny wschód
        "Elbląg": (1.2, 6.3),
        "Olsztyn": (2.4, 5.5),
        "Białystok": (5.2, 5.2),

        # Zachód
        "Gorzów Wielkopolski": (-5.5, 4.3),
        "Zielona Góra": (-5.0, 2.5),
        "Poznań": (-3.5, 4.5),

        # Północne centrum
        "Bydgoszcz": (-2.0, 5.1),
        "Toruń": (-0.9, 4.9),
        "Grudziądz": (-0.7, 5.9),

        # Centrum
        "Płock": (-0.2, 3.9),
        "Warszawa": (1.5, 3.9),
        "Łódź": (0.0, 2.7),
        "Radom": (2.0, 2.2),
        "Lublin": (4.0, 2.7),

        # Południowy zachód
        "Legnica": (-4.6, 2.0),
        "Jelenia Góra": (-5.0, 0.5),
        "Wrocław": (-3.4, 1.4),
        "Opole": (-1.9, 0.3),

        # Południe
        "Gliwice": (-0.8, -0.2),
        "Katowice": (0.2, -0.1),
        "Częstochowa": (0.5, 1.2),
        "Kielce": (2.5, 1.0),
        "Bielsko-Biała": (-0.2, -1.2),
        "Kraków": (1.7, -0.8),
        "Tarnów": (3.1, -0.2),
        "Nowy Sącz": (3.8, -1.3),
        "Rzeszów": (5.0, 0.3),
    }

    for city, position in cities.items():
        graph.add_node(city, pos=position)

    # start, koniec, dystans, prędkość, DMC, wysokość,
    # szerokość, długość, typ drogi
    roads = [
        # Północny korytarz
        ("Szczecin", "Koszalin", 170, 100, 40, 4.2, 2.6, 18.75, "expressway"),
        ("Koszalin", "Słupsk", 65, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Słupsk", "Gdynia", 105, 100, 40, 4.2, 2.6, 18.75, "expressway"),
        ("Gdynia", "Gdańsk", 25, 100, 40, 4.2, 2.6, 18.75, "highway"),
        ("Gdańsk", "Elbląg", 60, 120, 40, 4.2, 2.6, 18.75, "highway"),
        ("Elbląg", "Olsztyn", 100, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Olsztyn", "Białystok", 220, 90, 40, 4.0, 2.6, 18.75, "national"),

        # Zachód i północny zachód
        ("Szczecin", "Gorzów Wielkopolski", 110, 100, 40, 4.2, 2.6, 18.75, "expressway"),
        ("Gorzów Wielkopolski", "Poznań", 160, 100, 40, 4.2, 2.6, 18.75, "expressway"),
        ("Gorzów Wielkopolski", "Zielona Góra", 110, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Zielona Góra", "Poznań", 160, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Poznań", "Szczecin", 270, 100, 40, 4.2, 2.6, 18.75, "expressway"),
        ("Poznań", "Bydgoszcz", 140, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Zielona Góra", "Legnica", 120, 90, 40, 4.0, 2.6, 18.75, "national"),

        # Północne centrum
        ("Bydgoszcz", "Toruń", 50, 100, 40, 4.2, 2.6, 18.75, "highway"),
        ("Toruń", "Grudziądz", 55, 120, 40, 4.2, 2.6, 18.75, "highway"),
        ("Grudziądz", "Gdańsk", 110, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Toruń", "Płock", 100, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Poznań", "Toruń", 150, 100, 40, 4.0, 2.6, 18.75, "expressway"),

        # Centrum i wschód
        ("Płock", "Warszawa", 110, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Warszawa", "Białystok", 200, 120, 40, 4.2, 2.6, 18.75, "highway"),
        ("Białystok", "Lublin", 250, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Warszawa", "Lublin", 170, 120, 40, 4.2, 2.6, 18.75, "expressway"),
        ("Lublin", "Rzeszów", 170, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Warszawa", "Olsztyn", 220, 100, 40, 4.0, 2.6, 18.75, "expressway"),

        # Warszawa i okolice
        ("Warszawa", "Łódź", 130, 120, 40, 4.2, 2.6, 18.75, "highway"),
        ("Warszawa", "Radom", 105, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Łódź", "Radom", 140, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Łódź", "Płock", 115, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Łódź", "Katowice", 180, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Poznań", "Łódź", 200, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Poznań", "Warszawa", 310, 120, 40, 4.2, 2.6, 18.75, "highway"),

        # Południowy zachód
        ("Legnica", "Jelenia Góra", 75, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Legnica", "Wrocław", 75, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Jelenia Góra", "Wrocław", 115, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Wrocław", "Opole", 95, 120, 40, 4.2, 2.6, 18.75, "highway"),
        ("Wrocław", "Łódź", 220, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Wrocław", "Poznań", 180, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Wrocław", "Gliwice", 165, 100, 40, 4.0, 2.6, 18.75, "expressway"),

        # Południowe centrum
        ("Opole", "Gliwice", 85, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Opole", "Częstochowa", 110, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Gliwice", "Katowice", 30, 100, 40, 4.2, 2.6, 18.75, "highway"),
        ("Katowice", "Częstochowa", 75, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Katowice", "Bielsko-Biała", 60, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Katowice", "Kraków", 80, 100, 40, 4.2, 2.6, 18.75, "highway"),
        ("Częstochowa", "Kraków", 120, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Częstochowa", "Kielce", 100, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Kielce", "Kraków", 120, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Radom", "Kielce", 80, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Radom", "Lublin", 110, 90, 40, 4.0, 2.6, 18.75, "national"),

        # Południowy wschód
        ("Kraków", "Tarnów", 85, 120, 40, 4.2, 2.6, 18.75, "highway"),
        ("Tarnów", "Nowy Sącz", 75, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Tarnów", "Rzeszów", 105, 120, 40, 4.2, 2.6, 18.75, "highway"),
        ("Nowy Sącz", "Kraków", 110, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Rzeszów", "Kraków", 170, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Rzeszów", "Lublin", 170, 100, 40, 4.0, 2.6, 18.75, "expressway"),

        # Dodatkowe połączenia alternatywne
        ("Warszawa", "Katowice", 290, 110, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Warszawa", "Kraków", 300, 120, 40, 4.2, 2.6, 18.75, "highway"),
        ("Gdańsk", "Warszawa", 340, 120, 40, 4.2, 2.6, 18.75, "highway"),
        ("Bydgoszcz", "Poznań", 140, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Bielsko-Biała", "Kraków", 95, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Kielce", "Tarnów", 115, 90, 40, 4.0, 2.6, 18.75, "national"),
        ("Olsztyn", "Gdańsk", 170, 100, 40, 4.0, 2.6, 18.75, "expressway"),
        ("Gdynia", "Bydgoszcz", 170, 90, 40, 4.0, 2.6, 18.75, "national"),
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

        graph.add_edge(start, end, **road_data)
        graph.add_edge(end, start, **road_data.copy())

    return graph

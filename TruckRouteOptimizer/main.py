import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from truck_route_optimizer.road_network import create_road_network
from truck_route_optimizer.visualization import draw_road_network


def main():
    graph = create_road_network()

    print("Symulowana sieć drogowa")
    print(f"Liczba miast: {graph.number_of_nodes()}")
    print(f"Liczba odcinków: {graph.number_of_edges()}")

    print("\nDostępne miasta:")

    for city in graph.nodes:
        print(f"- {city}")

    draw_road_network(graph)


if __name__ == "__main__":
    main()

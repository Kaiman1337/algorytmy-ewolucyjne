
import matplotlib.pyplot as plt
import networkx as nx


def draw_road_network(graph, route=None):
    """Czytelna wizualizacja symulowanej sieci drogowej."""

    positions = nx.get_node_attributes(graph, "pos")

    # Do rysowania zwykłych dróg używamy grafu nieskierowanego.
    # Oryginalny graf nadal zachowuje kierunki przejazdu.
    visual_graph = nx.Graph()

    visual_graph.add_nodes_from(graph.nodes(data=True))

    for u, v, data in graph.edges(data=True):
        if visual_graph.has_edge(u, v):
            continue
        visual_graph.add_edge(u, v, **data)

    route_edges = set()

    if route:
        route_edges = {
            frozenset((u, v))
            for u, v in zip(route, route[1:])
        }

    normal_edges = []
    closed_edges = []
    selected_edges = []

    for u, v, data in visual_graph.edges(data=True):
        edge = (u, v)

        if frozenset(edge) in route_edges:
            selected_edges.append(edge)
        elif data["closed"]:
            closed_edges.append(edge)
        else:
            normal_edges.append(edge)

    fig, ax = plt.subplots(figsize=(13, 8))

    # Zwykłe drogi.
    nx.draw_networkx_edges(
        visual_graph,
        positions,
        edgelist=normal_edges,
        edge_color="#87929E",
        width=2,
        alpha=0.8,
        ax=ax,
    )

    # Zamknięte drogi.
    nx.draw_networkx_edges(
        visual_graph,
        positions,
        edgelist=closed_edges,
        edge_color="#E05252",
        width=3,
        style="dashed",
        ax=ax,
    )

    # Wyznaczona trasa.
    nx.draw_networkx_edges(
        visual_graph,
        positions,
        edgelist=selected_edges,
        edge_color="#16A36A",
        width=4,
        ax=ax,
    )

    # Węzły.
    nx.draw_networkx_nodes(
        visual_graph,
        positions,
        node_size=1900,
        node_color="#DCEBFA",
        edgecolors="#376A9C",
        linewidths=1.8,
        ax=ax,
    )

    # Nazwy miast.
    nx.draw_networkx_labels(
        visual_graph,
        positions,
        font_size=10,
        font_weight="bold",
        font_color="#172B40",
        ax=ax,
    )

    # Odległości - każda droga tylko raz.
    edge_labels = {
        (u, v): f'{data["distance_km"]} km'
        for u, v, data in visual_graph.edges(data=True)
    }

    nx.draw_networkx_edge_labels(
        visual_graph,
        positions,
        edge_labels=edge_labels,
        font_size=8,
        font_color="#34495E",
        rotate=True,
        bbox={
            "alpha": 0.85,
            "color": "white",
            "pad": 1.5,
        },
        ax=ax,
    )

    ax.set_title(
        "TRUCK ROUTE OPTIMIZER – ROAD NETWORK",
        fontsize=15,
        fontweight="bold",
        pad=20,
    )

    ax.legend(
        handles=[
            plt.Line2D([0], [0], color="#87929E", lw=2, label="Drogi"),
            plt.Line2D([0], [0], color="#16A36A", lw=4, label="Wyznaczona trasa"),
            plt.Line2D([0], [0], color="#E05252", lw=3,
                       linestyle="--", label="Droga zamknięta"),
        ],
        loc="upper left",
        frameon=True,
    )

    ax.axis("off")
    ax.margins(0.15)

    fig.tight_layout()
    plt.show()

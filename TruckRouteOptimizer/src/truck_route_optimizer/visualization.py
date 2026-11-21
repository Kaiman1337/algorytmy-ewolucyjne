import matplotlib.pyplot as plt
import networkx as nx


# GitHub Dark
BACKGROUND = "#0d1117"
PANEL = "#161b22"
ROAD_COLOR = "#6e7681"
CLOSED_COLOR = "#f85149"
ROUTE_COLOR = "#3fb950"
NODE_COLOR = "#21262d"
NODE_BORDER = "#58a6ff"
TEXT_COLOR = "#e6edf3"
MUTED_COLOR = "#c9d1d9"


def draw_road_network(graph, route=None, ax=None):
    """Rysuje symulowaną sieć drogową i opcjonalnie wyznaczoną trasę."""

    if ax is None:
        fig, ax = plt.subplots(figsize=(13, 8))
    else:
        fig = ax.figure

    ax.clear()

    fig.set_facecolor(BACKGROUND)
    ax.set_facecolor(PANEL)

    positions = nx.get_node_attributes(graph, "pos")

    # Graf nieskierowany służy wyłącznie do czytelnego rysowania dróg.
    visual_graph = nx.Graph()
    visual_graph.add_nodes_from(graph.nodes(data=True))

    for u, v, data in graph.edges(data=True):
        if not visual_graph.has_edge(u, v):
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

    # Zwykłe drogi – Warszawa–Katowice rysowana osobnym łukiem
    for u, v in normal_edges:
        if {u, v} == {"Warszawa", "Katowice"}:
            x1, y1 = positions[u]
            x2, y2 = positions[v]

            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops={
                    "arrowstyle": "-",
                    "connectionstyle": "arc3,rad=-0.35",
                    "color": ROAD_COLOR,
                    "linewidth": 2.2,
                    "alpha": 0.85,
                },
                zorder=1,
            )
        else:
            nx.draw_networkx_edges(
                visual_graph,
                positions,
                edgelist=[(u, v)],
                edge_color=ROAD_COLOR,
                width=2.2,
                alpha=0.85,
                ax=ax,
            )

    nx.draw_networkx_edges(
        visual_graph,
        positions,
        edgelist=closed_edges,
        edge_color=CLOSED_COLOR,
        width=3,
        style="dashed",
        ax=ax,
    )

    nx.draw_networkx_edges(
        visual_graph,
        positions,
        edgelist=selected_edges,
        edge_color=ROUTE_COLOR,
        width=4.5,
        alpha=1.0,
        ax=ax,
    )

    # Węzły miast
    nx.draw_networkx_nodes(
        visual_graph,
        positions,
        node_size=3200,
        node_color=NODE_COLOR,
        edgecolors=NODE_BORDER,
        linewidths=2,
        ax=ax,
    )

    # Nazwy miast
    nx.draw_networkx_labels(
        visual_graph,
        positions,
        font_size=9,
        font_weight="bold",
        font_color=TEXT_COLOR,
        ax=ax,
    )

    # Etykiety długości dróg
    for u, v, data in visual_graph.edges(data=True):
        x1, y1 = positions[u]
        x2, y2 = positions[v]

        if {u, v} == {"Warszawa", "Katowice"}:
            # Etykieta bezpośrednio na zakrzywionej drodze
            ax.text(
                (x1 + x2) / 2 + 0.4,
                (y1 + y2) / 2,
                f'{data["distance_km"]} km',
                ha="center",
                va="center",
                fontsize=8,
                color=MUTED_COLOR,
                bbox={
                    "boxstyle": "round,pad=0.2",
                    "facecolor": PANEL,
                    "edgecolor": "none",
                    "alpha": 0.95,
                },
                zorder=5,
            )
        else:
            middle_x = (x1 + x2) / 2
            middle_y = (y1 + y2) / 2

            ax.annotate(
                f'{data["distance_km"]} km',
                xy=(middle_x, middle_y),
                xytext=(0, 9),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                color=MUTED_COLOR,
                bbox={
                    "boxstyle": "round,pad=0.2",
                    "facecolor": PANEL,
                    "edgecolor": "none",
                    "alpha": 0.95,
                },
                zorder=5,
            )

    ax.set_title(
        "ROAD NETWORK",
        fontsize=15,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=20,
    )

    legend = ax.legend(
        handles=[
            plt.Line2D(
                [0], [0],
                color=ROAD_COLOR,
                lw=2.2,
                label="Drogi"
            ),
            plt.Line2D(
                [0], [0],
                color=ROUTE_COLOR,
                lw=4.5,
                label="Wyznaczona trasa"
            ),
            plt.Line2D(
                [0], [0],
                color=CLOSED_COLOR,
                lw=3,
                linestyle="--",
                label="Droga zamknięta"
            ),
        ],
        loc="upper left",
        frameon=True,
        fontsize=9,
    )

    legend.get_frame().set_facecolor(PANEL)
    legend.get_frame().set_edgecolor("#30363d")

    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)

    ax.axis("off")
    ax.margins(0.15)

    fig.tight_layout()

    return fig, ax

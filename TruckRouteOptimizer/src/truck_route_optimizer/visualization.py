
import matplotlib.pyplot as plt
import networkx as nx

from matplotlib.patches import FancyArrowPatch


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


def _draw_curved_edge(
    ax,
    positions,
    start,
    end,
    color,
    width,
    alpha=0.85,
    style="solid",
    rad=0.12,
    zorder=1,
):
    """Rysuje pojedynczą zakrzywioną drogę."""

    x1, y1 = positions[start]
    x2, y2 = positions[end]

    edge = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="-",
        connectionstyle=f"arc3,rad={rad}",
        color=color,
        linewidth=width,
        linestyle=style,
        alpha=alpha,
        shrinkA=13,
        shrinkB=13,
        zorder=zorder,
    )

    ax.add_patch(edge)


def _get_edge_label_position(positions, start, end, rad):
    """Wyznacza przybliżony środek zakrzywionej drogi."""

    x1, y1 = positions[start]
    x2, y2 = positions[end]

    dx = x2 - x1
    dy = y2 - y1

    midpoint_x = (x1 + x2) / 2
    midpoint_y = (y1 + y2) / 2

    # Przesunięcie etykiety zgodne z krzywizną drogi.
    label_x = midpoint_x + 0.5 * rad * dy
    label_y = midpoint_y - 0.5 * rad * dx

    return label_x, label_y


def _get_label_offset(city, position):
    """Dobiera kierunek etykiety na podstawie położenia miasta."""

    x, y = position

    if city in {
        "Szczecin",
        "Koszalin",
        "Słupsk",
        "Gdynia",
        "Gdańsk",
        "Elbląg",
        "Grudziądz",
    }:
        return (0, 13)

    if city in {
        "Jelenia Góra",
        "Bielsko-Biała",
        "Kraków",
        "Nowy Sącz",
    }:
        return (0, -15)

    if x <= -4.5:
        return (-9, 0)

    if x >= 4.0:
        return (9, 0)

    if x < -2.0:
        return (-7, 9)

    if x > 2.0:
        return (7, 9)

    if y < 1.0:
        return (0, -14)

    return (0, 12)


def draw_road_network(graph, route=None, ax=None):
    """Rysuje symulowaną sieć drogową i opcjonalną trasę."""

    if ax is None:
        fig, ax = plt.subplots(figsize=(17, 12))
    else:
        fig = ax.figure

    ax.clear()

    fig.set_facecolor(BACKGROUND)
    ax.set_facecolor(PANEL)

    positions = nx.get_node_attributes(graph, "pos")

    # Graf nieskierowany służy wyłącznie do wizualizacji.
    # Właściwy graf pozostaje skierowany.
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
        elif data.get("closed", False):
            closed_edges.append(edge)
        else:
            normal_edges.append(edge)

    # Zapamiętujemy krzywiznę każdej drogi.
    # Dzięki temu etykiety będą odpowiadały faktycznemu
    # przebiegowi narysowanych łuków.
    edge_curvatures = {}

    all_edges = normal_edges + closed_edges

    for index, (u, v) in enumerate(all_edges):
        direction = 1 if index % 2 == 0 else -1
        curvature = 0.10 + (index % 4) * 0.045
        rad = direction * curvature

        edge_key = frozenset((u, v))
        edge_curvatures[edge_key] = rad

        data = visual_graph.get_edge_data(u, v)
        is_closed = data.get("closed", False)

        _draw_curved_edge(
            ax,
            positions,
            u,
            v,
            color=CLOSED_COLOR if is_closed else ROAD_COLOR,
            width=2.0 if not is_closed else 2.5,
            alpha=0.8,
            style="dashed" if is_closed else "solid",
            rad=rad,
            zorder=1,
        )

    # Wyznaczona trasa jest rysowana na wierzchu.
    route_curvatures = {}

    for index, (u, v) in enumerate(selected_edges):
        direction = 1 if index % 2 == 0 else -1
        rad = direction * (0.10 + (index % 4) * 0.045)

        route_curvatures[frozenset((u, v))] = rad

        _draw_curved_edge(
            ax,
            positions,
            u,
            v,
            color=ROUTE_COLOR,
            width=4.5,
            alpha=1.0,
            rad=rad,
            zorder=3,
        )

    # Etykiety długości wszystkich fizycznych dróg.
    # Każde połączenie jest oznaczone tylko raz.
    for u, v, data in visual_graph.edges(data=True):
        edge_key = frozenset((u, v))

        rad = route_curvatures.get(
            edge_key,
            edge_curvatures.get(edge_key, 0.12),
        )

        distance = data.get("distance_km")

        if distance is None:
            continue

        label_x, label_y = _get_edge_label_position(
            positions,
            u,
            v,
            rad,
        )

        is_route = edge_key in route_edges
        is_closed = data.get("closed", False)

        if is_route:
            label_color = ROUTE_COLOR
            label_weight = "bold"
            label_alpha = 1.0
        elif is_closed:
            label_color = CLOSED_COLOR
            label_weight = "bold"
            label_alpha = 0.95
        else:
            label_color = MUTED_COLOR
            label_weight = "normal"
            label_alpha = 0.9

        ax.text(
            label_x,
            label_y,
            f"{distance:g} km",
            fontsize=6.5,
            fontweight=label_weight,
            color=label_color,
            ha="center",
            va="center",
            bbox={
                "boxstyle": "round,pad=0.16",
                "facecolor": BACKGROUND,
                "edgecolor": "#30363d",
                "linewidth": 0.5,
                "alpha": label_alpha,
            },
            zorder=4,
        )

    # Węzły miast.
    nx.draw_networkx_nodes(
        visual_graph,
        positions,
        node_size=850,
        node_color=NODE_COLOR,
        edgecolors=NODE_BORDER,
        linewidths=1.7,
        ax=ax,
    )

    # Etykiety miast.
    for city, position in positions.items():
        offset = _get_label_offset(city, position)

        ax.annotate(
            city,
            xy=position,
            xytext=offset,
            textcoords="offset points",
            ha="center",
            va="center",
            fontsize=7.5,
            fontweight="bold",
            color=TEXT_COLOR,
            bbox={
                "boxstyle": "round,pad=0.25",
                "facecolor": PANEL,
                "edgecolor": "#30363d",
                "alpha": 0.95,
            },
            zorder=5,
        )

    # Tytuł.
    ax.set_title(
        "ROAD NETWORK",
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=20,
    )

    # Legenda.
    legend = ax.legend(
        handles=[
            plt.Line2D(
                [0], [0],
                color=ROAD_COLOR,
                lw=2.2,
                label="Drogi",
            ),
            plt.Line2D(
                [0], [0],
                color=ROUTE_COLOR,
                lw=4.5,
                label="Wyznaczona trasa",
            ),
            plt.Line2D(
                [0], [0],
                color=CLOSED_COLOR,
                lw=2.5,
                linestyle="--",
                label="Droga zamknięta",
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
    ax.margins(0.16)

    fig.tight_layout()

    return fig, ax

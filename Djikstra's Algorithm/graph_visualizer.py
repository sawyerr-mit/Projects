"""Visualize graphs stored in the pickle files used by search.py."""

import argparse
import os
import pickle

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


def load_graph(filename):
    with open(filename, "rb") as file:
        return pickle.load(file)


def get_graph_data(graph):
    vertices = list(graph.getVertices())
    vertex_ids = [vertex.id for vertex in vertices]
    vertex_set = set(vertex_ids)

    edges = []
    seen = set()
    for vertex_id in vertex_ids:
        for edge in graph.edgesOf(vertex_id):
            target = edge.t
            if target not in vertex_set:
                continue

            key = (min(vertex_id, target), max(vertex_id, target))
            if key in seen:
                continue
            seen.add(key)
            edges.append((vertex_id, target, getattr(edge, "weight", 1)))

    return vertex_ids, edges


def get_geographic_positions(graph, vertex_ids):
    positions = {}
    for vertex_id in vertex_ids:
        try:
            tags = graph.getTags(vertex_id)
            lat = float(tags["lat"])
            lon = float(tags["lon"])
            positions[vertex_id] = (lon, lat)
        except (KeyError, TypeError, ValueError, AttributeError):
            return None
    return positions


def get_spring_positions(vertex_ids, edges, seed=42):
    try:
        import networkx as nx
    except ImportError as error:
        raise ImportError(
            "This graph does not have latitude/longitude coordinates. "
            "Install networkx to use the spring layout: pip install networkx"
        ) from error

    graph = nx.Graph()
    graph.add_nodes_from(vertex_ids)
    graph.add_edges_from((source, target) for source, target, _ in edges)
    return nx.spring_layout(graph, seed=seed)


def plot_graph(graph, filename, start=None, end=None, layout="auto", show_weights=False):
    vertex_ids, edges = get_graph_data(graph)
    vertex_set = set(vertex_ids)

    if start is not None and start not in vertex_set:
        raise ValueError(f"Start vertex {start} is not in the graph.")
    if end is not None and end not in vertex_set:
        raise ValueError(f"End vertex {end} is not in the graph.")

    geographic_positions = get_geographic_positions(graph, vertex_ids)
    if layout == "geographic":
        if geographic_positions is None:
            raise ValueError("Latitude/longitude coordinates are not available for every vertex.")
        positions = geographic_positions
        is_geographic = True
    elif layout == "spring":
        positions = get_spring_positions(vertex_ids, edges)
        is_geographic = False
    elif geographic_positions is not None:
        positions = geographic_positions
        is_geographic = True
    else:
        positions = get_spring_positions(vertex_ids, edges)
        is_geographic = False

    path = []
    if start is not None and end is not None:
        from search import BFS

        path, _, _ = BFS(graph, start, end)

    path_edges = set(zip(path[:-1], path[1:]))
    path_edges |= set(zip(path[1:], path[:-1]))

    normal_segments = []
    highlighted_segments = []
    normal_weights = []

    for source, target, weight in edges:
        segment = [positions[source], positions[target]]
        if (source, target) in path_edges:
            highlighted_segments.append(segment)
        else:
            normal_segments.append(segment)
            normal_weights.append(weight)

    fig, ax = plt.subplots(figsize=(12, 9))

    if normal_segments:
        ax.add_collection(LineCollection(
            normal_segments,
            colors="#a6a6a6",
            linewidths=0.65 if len(normal_segments) < 10000 else 0.25,
            alpha=0.55,
            zorder=1,
        ))

    if highlighted_segments:
        ax.add_collection(LineCollection(
            highlighted_segments,
            colors="#e63946",
            linewidths=2.5,
            alpha=0.95,
            zorder=3,
        ))

    x_values = [positions[v][0] for v in vertex_ids]
    y_values = [positions[v][1] for v in vertex_ids]
    ax.scatter(x_values, y_values, s=9 if len(vertex_ids) < 10000 else 2,
               color="#2463a6", alpha=0.8, zorder=2, label="Vertices")

    if start is not None:
        ax.scatter(*positions[start], s=100, color="#2a9d55", edgecolors="black",
                   linewidths=0.7, zorder=4, label=f"Start: {start}")
    if end is not None:
        ax.scatter(*positions[end], s=100, color="#f4a261", edgecolors="black",
                   linewidths=0.7, zorder=4, label=f"End: {end}")

    if show_weights and len(edges) <= 500:
        for source, target, weight in edges:
            midpoint = (
                (positions[source][0] + positions[target][0]) / 2,
                (positions[source][1] + positions[target][1]) / 2,
            )
            ax.annotate(f"{weight:g}", midpoint, fontsize=6, alpha=0.75)

    ax.autoscale()
    ax.margins(0.05)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_title(f"{os.path.basename(filename)} — {len(vertex_ids):,} vertices, {len(edges):,} edges")
    ax.set_xlabel("Longitude" if is_geographic else "X")
    ax.set_ylabel("Latitude" if is_geographic else "Y")
    ax.grid(True, alpha=0.2)
    ax.legend(loc="best")
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Plot a graph stored as a pickle file.")
    parser.add_argument("file", help="Pickle file containing the graph, e.g. romania.pickle")
    parser.add_argument("--start", type=int, help="Optional starting vertex ID")
    parser.add_argument("--end", type=int, help="Optional destination vertex ID")
    parser.add_argument("--layout", choices=("auto", "geographic", "spring"), default="auto",
                        help="auto uses latitude/longitude when available")
    parser.add_argument("--weights", action="store_true", help="Show edge weights (small graphs only)")
    args = parser.parse_args()

    graph = load_graph(args.file)
    print(f"Loaded {args.file}")
    print(f"Vertices: {graph.sizeV():,}")
    plot_graph(graph, args.file, args.start, args.end, args.layout, args.weights)


if __name__ == "__main__":
    main()

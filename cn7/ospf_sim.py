# ospf_sim.py
"""
OSPF simulation (link-state). Each router floods LSAs (we simulate perfect flooding)
and then runs Dijkstra locally to build its shortest-path tree and routing table.
"""

import networkx as nx
from typing import Dict, Tuple

def simulate_ospf(graph: nx.Graph):
    """
    graph: weighted graph (edge attribute 'weight' is cost)
    Returns dict: router -> (shortest path tree as dict dest -> (cost, next_hop))
    """
    routing_tables = {}
    for node in graph.nodes():
        # Dijkstra from this node
        lengths, paths = nx.single_source_dijkstra(graph, node, weight='weight')
        table = {}
        for dest, cost in lengths.items():
            if dest == node:
                table[dest] = (0, node)
            else:
                # next hop = first node on path after source
                path = paths[dest]
                next_hop = path[1] if len(path) >= 2 else dest
                table[dest] = (cost, next_hop)
        routing_tables[node] = table
    return routing_tables

if __name__ == "__main__":
    G = nx.Graph()
    edges = [
        ("R1","R2",1), ("R2","R3",1), ("R3","R4",5),
        ("R1","R4",10), ("R2","R4",2)
    ]
    G.add_weighted_edges_from(edges)
    rt = simulate_ospf(G)
    for r, table in rt.items():
        print(f"Router {r}:")
        for dest,(cost,nxt) in sorted(table.items()):
            print(f"  {dest} -> cost {cost}, next {nxt}")
        print()

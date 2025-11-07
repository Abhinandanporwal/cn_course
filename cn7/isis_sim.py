# isis_sim.py
"""
IS-IS simulation (link-state) — similar to OSPF in approach:
- Flood link-state (we simulate perfect flooding)
- Each node builds full topology and runs Dijkstra
"""

import networkx as nx
from typing import Dict, Tuple

def simulate_isis(graph: nx.Graph):
    """
    For simplicity, we assume LSDB is perfectly synchronized, so each router has full graph.
    Each router runs Dijkstra to compute shortest paths.
    Returns mapping router -> routing table (dest -> (cost, next_hop))
    """
    # identical to OSPF simulation for our purposes
    routing_tables = {}
    for node in graph.nodes():
        lengths, paths = nx.single_source_dijkstra(graph, node, weight='weight')
        table = {}
        for dest, cost in lengths.items():
            next_hop = dest if dest==node else paths[dest][1]
            table[dest] = (cost, next_hop)
        routing_tables[node] = table
    return routing_tables

if __name__ == "__main__":
    G = nx.Graph()
    G.add_weighted_edges_from([("A","B",1),("B","C",1),("C","D",1),("A","D",4)])
    out = simulate_isis(G)
    for r,t in out.items():
        print(f"Router {r}:")
        for dest,(c,n) in sorted(t.items()):
            print(f"  {dest} -> cost {c}, next {n}")
        print()

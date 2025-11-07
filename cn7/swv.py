# sim_with_visuals.py
"""
Run simulations for RIP, OSPF, BGP, IS-IS, save JSON routing tables and PNG topology diagrams.
Produces:
 - sim_outputs/ (rip_tables.json, ospf_tables.json, bgp_tables.json, isis_tables.json)
 - sim_outputs/*.png  (topology images)
"""

import json
from pathlib import Path
from typing import Dict, List
import networkx as nx
import matplotlib.pyplot as plt
import copy

OUT_DIR = Path("sim_outputs")
OUT_DIR.mkdir(exist_ok=True)

# -------------------------
# 1) RIP (Distance-vector) - simplified
# -------------------------
class RIPRouter:
    def __init__(self, name: str, neighbors: Dict[str,int]):
        self.name = name
        self.table = {name: (0, name)}
        for n, cost in neighbors.items():
            self.table[n] = (cost, n)

    def update_from_neighbor(self, neighbor_name: str, neighbor_table: Dict[str, tuple], link_cost: int):
        changed = False
        for dest, (n_cost, n_next) in neighbor_table.items():
            if dest == self.name:
                continue
            cost_via = link_cost + n_cost
            if dest not in self.table or cost_via < self.table[dest][0]:
                self.table[dest] = (cost_via, neighbor_name)
                changed = True
        return changed

def simulate_rip(graph: nx.Graph, max_iters=50):
    routers = {}
    for node in graph.nodes():
        neighbors = {nbr: graph.edges[node, nbr].get('weight', 1) for nbr in graph.neighbors(node)}
        routers[node] = RIPRouter(node, neighbors)
    for it in range(max_iters):
        changed_any = False
        snapshot = {r: copy.deepcopy(routers[r].table) for r in routers}
        for router_name, router in routers.items():
            for nbr in graph.neighbors(router_name):
                link_cost = graph.edges[router_name, nbr].get('weight', 1)
                changed = router.update_from_neighbor(nbr, snapshot[nbr], link_cost)
                if changed: changed_any = True
        if not changed_any:
            break
    tables = {name: dict(sorted(r.table.items())) for name, r in routers.items()}
    return tables

# -------------------------
# 2) OSPF (Link-state via Dijkstra)
# -------------------------
def simulate_ospf(graph: nx.Graph):
    routing_tables = {}
    for node in graph.nodes():
        lengths, paths = nx.single_source_dijkstra(graph, node, weight='weight')
        table = {}
        for dest, cost in lengths.items():
            if dest == node:
                table[dest] = (0, node)
            else:
                path = paths[dest]
                next_hop = path[1] if len(path) >= 2 else dest
                table[dest] = (cost, next_hop)
        routing_tables[node] = dict(sorted(table.items()))
    return routing_tables

# -------------------------
# 3) BGP (Simplified path-vector)
# -------------------------
class BGPNode:
    def __init__(self, asn: str, neighbors: List[str]):
        self.asn = asn
        self.table = {}
        self.neighbors = neighbors

    def process_updates_from(self, neighbor_as: str, updates: Dict[str, List[str]]):
        changed = False
        for prefix, path in updates.items():
            # drop if contains self ASN
            if self.asn in path:
                continue
            if prefix not in self.table or len(path) < len(self.table[prefix]):
                self.table[prefix] = path
                changed = True
        return changed

def simulate_bgp(as_graph: nx.DiGraph, origin_prefixes: Dict[str, List[str]], max_iters=50):
    nodes = {}
    for asn in as_graph.nodes():
        # neighbors via outgoing edges + incoming edges (treat as bidirectional)
        neighbors = list(as_graph.neighbors(asn))
        for other in as_graph.nodes():
            if as_graph.has_edge(other, asn) and other not in neighbors:
                neighbors.append(other)
        nodes[asn] = BGPNode(asn, neighbors)
    for origin_asn, prefixes in origin_prefixes.items():
        for p in prefixes:
            nodes[origin_asn].table[p] = [origin_asn]
    for it in range(max_iters):
        changed_any = False
        snapshot = {asn: copy.deepcopy(nodes[asn].table) for asn in nodes}
        for asn, node in nodes.items():
            for nbr in node.neighbors:
                if nbr not in snapshot: continue
                updates = {prefix: path + [nbr] for prefix, path in snapshot[nbr].items()}
                changed = node.process_updates_from(nbr, updates)
                if changed: changed_any = True
        if not changed_any:
            break
    return {asn: nodes[asn].table for asn in nodes}

# -------------------------
# 4) IS-IS (Link-state) - same as OSPF here
# -------------------------
def simulate_isis(graph: nx.Graph):
    tables = {}
    for node in graph.nodes():
        lengths, paths = nx.single_source_dijkstra(graph, node, weight='weight')
        table = {}
        for dest, cost in lengths.items():
            next_hop = dest if dest == node else paths[dest][1]
            table[dest] = (cost, next_hop)
        tables[node] = dict(sorted(table.items()))
    return tables

# -------------------------
# Utilities: draw graphs and save JSON
# -------------------------
def draw_and_save_graph(graph: nx.Graph, path: Path, title: str):
    plt.figure(figsize=(6,4))
    pos = nx.spring_layout(graph, seed=42)
    nx.draw_networkx_nodes(graph, pos, node_size=700)
    nx.draw_networkx_labels(graph, pos)
    nx.draw_networkx_edges(graph, pos)
    # edge labels (weights) if present
    edge_labels = {(u,v): graph.edges[u,v].get('weight', 1) for u,v in graph.edges()}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()

def save_json(obj, path: Path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)

# -------------------------
# Demo topologies and runs
# -------------------------
def demo_rip():
    G = nx.Graph()
    G.add_weighted_edges_from([
        ("R1","R2",1), ("R2","R3",1), ("R3","R4",1),
        ("R2","R4",2), ("R1","R5",1)
    ])
    tables = simulate_rip(G)
    save_json(tables, OUT_DIR/"rip_tables.json")
    draw_and_save_graph(G, OUT_DIR/"rip_topology.png", "RIP Topology")
    print("RIP done")

def demo_ospf():
    G = nx.Graph()
    G.add_weighted_edges_from([
        ("R1","R2",1), ("R2","R3",1), ("R3","R4",5),
        ("R1","R4",10), ("R2","R4",2)
    ])
    tables = simulate_ospf(G)
    save_json(tables, OUT_DIR/"ospf_tables.json")
    draw_and_save_graph(G, OUT_DIR/"ospf_topology.png", "OSPF Topology (weights shown)")
    print("OSPF done")

def demo_bgp():
    G = nx.DiGraph()
    G.add_edges_from([("AS1","AS2"), ("AS2","AS3"), ("AS3","AS4"), ("AS2","AS4")])
    origins = {"AS4":["10.0.0.0/24"], "AS3":["192.0.2.0/24"]}
    tables = simulate_bgp(G, origins)
    save_json(tables, OUT_DIR/"bgp_tables.json")
    # draw as undirected for visualization
    draw_and_save_graph(nx.Graph(G), OUT_DIR/"bgp_topology.png", "BGP AS-level Topology")
    print("BGP done")

def demo_isis():
    G = nx.Graph()
    G.add_weighted_edges_from([("A","B",1),("B","C",1),("C","D",1),("A","D",4)])
    tables = simulate_isis(G)
    save_json(tables, OUT_DIR/"isis_tables.json")
    draw_and_save_graph(G, OUT_DIR/"isis_topology.png", "IS-IS Topology")
    print("IS-IS done")

if __name__ == "__main__":
    demo_rip()
    demo_ospf()
    demo_bgp()
    demo_isis()
    print("All simulations complete. Check sim_outputs/ for JSON & PNG files.")

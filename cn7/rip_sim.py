# rip_sim.py
"""
RIP simulation (distance-vector) using Bellman-Ford-like updates.
Each router maintains a distance vector (# of hops). Routers periodically exchange
routing tables until convergence.
"""

from typing import Dict, Tuple
import networkx as nx
import copy

class RIPRouter:
    def __init__(self, name: str, neighbors: Dict[str,int]):
        self.name = name
        # routing table: dest -> (cost, next_hop)
        self.table: Dict[str, Tuple[int,str]] = {name: (0, name)}
        # initialize neighbor entries
        for n, cost in neighbors.items():
            self.table[n] = (cost, n)

    def update_from_neighbor(self, neighbor_name: str, neighbor_table: Dict[str, Tuple[int,str]], link_cost: int):
        """Incorporate neighbor's distance vector. Returns True if table changed."""
        changed = False
        for dest, (n_cost, n_next) in neighbor_table.items():
            if dest == self.name:
                continue
            # cost via neighbor = cost to neighbor + neighbor's cost to dest
            cost_via = link_cost + n_cost
            if dest not in self.table or cost_via < self.table[dest][0]:
                self.table[dest] = (cost_via, neighbor_name)
                changed = True
        return changed

def simulate_rip(graph: nx.Graph, max_iters=50):
    """
    graph: undirected weighted networkx graph where node names are router names
    and edge attribute 'weight' indicates cost (we treat as hop cost; if omitted assume 1)
    """
    # Initialize routers
    routers = {}
    for node in graph.nodes():
        neighbors = {}
        for nbr in graph.neighbors(node):
            cost = graph.edges[node, nbr].get('weight', 1)
            neighbors[nbr] = cost
        routers[node] = RIPRouter(node, neighbors)

    # Periodic exchange until convergence
    for it in range(max_iters):
        changed_any = False
        # snapshot to simulate simultaneous exchanges
        snapshot = {r: copy.deepcopy(routers[r].table) for r in routers}
        for router_name, router in routers.items():
            for nbr in graph.neighbors(router_name):
                link_cost = graph.edges[router_name, nbr].get('weight', 1)
                changed = router.update_from_neighbor(nbr, snapshot[nbr], link_cost)
                if changed:
                    changed_any = True
        if not changed_any:
            # converged
            # print(f"RIP converged in {it} iterations")
            break

    # Format output
    routing_tables = {}
    for name, r in routers.items():
        # produce sorted table (dest -> (cost, next_hop))
        routing_tables[name] = dict(sorted(r.table.items()))
    return routing_tables

# Example: small helper if run directly
if __name__ == "__main__":
    G = nx.Graph()
    edges = [
        ("A","B",1), ("B","C",1), ("C","D",1), ("B","D",2), ("A","E",1)
    ]
    G.add_weighted_edges_from(edges)
    tables = simulate_rip(G)
    for router, table in tables.items():
        print(f"Router {router} routing table:")
        for dest,(cost,next_hop) in table.items():
            print(f"  {dest} -> cost {cost}, next hop {next_hop}")
        print()

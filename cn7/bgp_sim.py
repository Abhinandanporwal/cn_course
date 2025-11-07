# bgp_sim.py
"""
Simplified BGP simulation (path-vector). Each node represents an AS (router).
We exchange path vectors: dest_prefix -> AS_PATH (list). Preference rule: shortest AS_PATH.
Loop prevention: drop routes containing your own AS number.
"""

from typing import Dict, List, Tuple
import networkx as nx
import copy

class BGPNode:
    def __init__(self, asn: str, neighbors: List[str]):
        self.asn = asn
        # routing table: prefix -> AS_PATH (list of ASNs from origin to current node)
        self.table: Dict[str, List[str]] = {}
        self.neighbors = neighbors

    def advertise(self):
        """
        Produce UPDATE messages to neighbors: for each prefix in table, advertise AS_PATH + [self.asn]
        Returns dict neighbor -> updates (prefix -> as_path)
        """
        updates = {}
        for nbr in self.neighbors:
            updates[nbr] = {}
            for prefix, as_path in self.table.items():
                # advertise path extended by our ASN
                updates[nbr][prefix] = as_path + [self.asn]
        return updates

    def process_updates_from(self, neighbor_as: str, updates: Dict[str, List[str]]):
        changed = False
        for prefix, path in updates.items():
            # loop prevention: if our ASN is in path, ignore
            if self.asn in path:
                continue
            # path that will be stored at this node is path (origin->...->neighbor) + neighbor? we treat updates as already extended by neighbor
            # Our local AS path should be path (origin..neighbor..)
            # Choose path if shorter or prefix absent
            if prefix not in self.table or len(path) < len(self.table[prefix]):
                self.table[prefix] = path
                changed = True
        return changed

def simulate_bgp(as_graph: nx.DiGraph, origin_prefixes: Dict[str, List[str]], max_iters=50):
    """
    as_graph: directed graph of AS peering (but we will treat as undirected for simplicity)
    origin_prefixes: dict mapping origin_asn -> list of prefixes that originate there
    """
    nodes = {}
    for asn in as_graph.nodes():
        neighbors = list(as_graph.neighbors(asn))
        # For simplicity, also include reverse neighbors if graph undirected edges not present
        for other in as_graph.nodes():
            if as_graph.has_edge(other, asn) and other not in neighbors:
                neighbors.append(other)
        nodes[asn] = BGPNode(asn, neighbors)

    # Initialize originators' tables
    for origin_asn, prefixes in origin_prefixes.items():
        for p in prefixes:
            # origin's AS_PATH is [origin_asn]
            nodes[origin_asn].table[p] = [origin_asn]

    # iterative UPDATE exchange (simplified synchronous rounds)
    for it in range(max_iters):
        changed_any = False
        snapshot = {asn: copy.deepcopy(nodes[asn].table) for asn in nodes}
        # each node processes updates from each neighbor
        for asn, node in nodes.items():
            for nbr in node.neighbors:
                if nbr not in snapshot:
                    continue
                # neighbor advertises its table extended by neighbor ASN
                updates = {}
                for prefix, path in snapshot[nbr].items():
                    # advertise path extended by neighbor ASN
                    updates[prefix] = path + [nbr]
                changed = node.process_updates_from(nbr, updates)
                if changed:
                    changed_any = True
        if not changed_any:
            break

    # Format final routing tables (prefix -> chosen AS_PATH)
    final_tables = {asn: nodes[asn].table for asn in nodes}
    return final_tables

if __name__ == "__main__":
    G = nx.DiGraph()
    G.add_edges_from([("AS1","AS2"), ("AS2","AS3"), ("AS3","AS4"), ("AS2","AS4")])
    origins = {"AS4":["10.0.0.0/24"], "AS3":["192.0.2.0/24"]}
    out = simulate_bgp(G, origins)
    for asn, table in out.items():
        print(f"AS {asn} routing table:")
        for prefix, path in table.items():
            print(f"  {prefix} -> AS-PATH: {' '.join(path)}")
        print()

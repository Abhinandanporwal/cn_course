# run_all.py
"""
Run sample simulations for RIP, OSPF, BGP, IS-IS and print routing tables.
Saves simple text snapshots you can screenshot for submission.
"""

import networkx as nx
from rip_sim import simulate_rip
from ospf_sim import simulate_ospf
from bgp_sim import simulate_bgp
from isis_sim import simulate_isis
import json
from pathlib import Path

out_dir = Path("sim_outputs")
out_dir.mkdir(exist_ok=True)

def demo_rip():
    G = nx.Graph()
    G.add_weighted_edges_from([
        ("R1","R2",1), ("R2","R3",1), ("R3","R4",1),
        ("R2","R4",2), ("R1","R5",1)
    ])
    tables = simulate_rip(G)
    path = out_dir / "rip_tables.json"
    path.write_text(json.dumps(tables, indent=2))
    print("RIP routing tables written to", path)
    for r,t in tables.items():
        print(f"=== {r} ===")
        for dest,(cost,nxt) in t.items():
            print(f"{dest:>4}  cost={cost:<3}  next={nxt}")
        print()

def demo_ospf():
    G = nx.Graph()
    G.add_weighted_edges_from([
        ("R1","R2",1), ("R2","R3",1), ("R3","R4",5),
        ("R1","R4",10), ("R2","R4",2)
    ])
    tables = simulate_ospf(G)
    (out_dir/"ospf_tables.json").write_text(json.dumps(tables, indent=2))
    print("OSPF routing tables:")
    for r,t in tables.items():
        print(f"--- {r} ---")
        for dest,(cost,next_hop) in t.items():
            print(f"{dest:>4} cost={cost:<3} next={next_hop}")
        print()

def demo_bgp():
    G = nx.DiGraph()
    G.add_edges_from([("AS1","AS2"), ("AS2","AS3"), ("AS3","AS4"), ("AS2","AS4")])
    origins = {"AS4":["10.0.0.0/24"], "AS3":["192.0.2.0/24"]}
    tables = simulate_bgp(G, origins)
    (out_dir/"bgp_tables.json").write_text(json.dumps(tables, indent=2))
    print("BGP routing tables:")
    for asn,table in tables.items():
        print(f"--- {asn} ---")
        for prefix,path in table.items():
            print(f"{prefix:>18}  AS-PATH: {' '.join(path)}")
        print()

def demo_isis():
    G = nx.Graph()
    G.add_weighted_edges_from([("A","B",1),("B","C",1),("C","D",1),("A","D",4)])
    tables = simulate_isis(G)
    (out_dir/"isis_tables.json").write_text(json.dumps(tables, indent=2))
    print("IS-IS routing tables:")
    for r,t in tables.items():
        print(f"--- {r} ---")
        for dest,(cost,next_hop) in t.items():
            print(f"{dest:>4} cost={cost:<3} next={next_hop}")
        print()

if __name__ == "__main__":
    demo_rip()
    demo_ospf()
    demo_bgp()
    demo_isis()
    print("All simulations done. Check sim_outputs directory for JSON snapshots.")

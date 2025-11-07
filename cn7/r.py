# report_generator.py
"""
Generate a 2-3 page PDF report 'Lab7_Report.pdf' using PNGs + JSONs produced by sim_with_visuals.py
Requires: reportlab
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from pathlib import Path
import json, textwrap

OUT_DIR = Path("sim_outputs")
REPORT_PATH = Path("Lab7_Report.pdf")

def load_json(name):
    p = OUT_DIR / name
    if not p.exists():
        return {}
    return json.load(open(p))

def draw_title(c):
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, 800, "Lab Assignment 7: Routing Protocols Simulation in Python")
    c.setFont("Helvetica", 10)
    c.drawString(40, 786, "Author: Abhinandan Porwal")
    c.drawString(40, 772, "Date: October 17, 2025")
    c.line(40, 765, 555, 765)

def add_obj_and_summary(c):
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 745, "Objective")
    text = (
        "Simulate routing protocols (RIP, OSPF, BGP, IS-IS) in Python. "
        "Show topologies, routing tables, and compare convergence and overhead."
    )
    c.setFont("Helvetica", 10)
    wrapped = textwrap.wrap(text, width=90)
    y = 730
    for line in wrapped:
        c.drawString(40, y, line)
        y -= 12

def add_topology_image(c, img_path, x, y, w=240, h=150, caption=""):
    p = OUT_DIR / img_path
    if not p.exists():
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(x, y + h / 2, f"(image not found: {img_path})")
        return
    img = ImageReader(str(p))
    c.drawImage(img, x, y, width=w, height=h, preserveAspectRatio=True, anchor='c')
    if caption:
        c.setFont("Helvetica", 9)
        c.drawString(x, y - 10, caption)

def add_table_snapshot(c, json_name, x, y, max_entries=6):
    """Draw a small sample from the JSON routing table."""
    data = load_json(json_name)
    if not data:
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(x, y, f"(no snapshot available for {json_name})")
        return

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, f"Snapshot: {json_name}")
    y -= 14
    c.setFont("Helvetica", 9)

    first_router = next(iter(data.keys()))
    c.drawString(x, y, f"Router: {first_router}")
    y -= 12

    entries = list(data[first_router].items())[:max_entries]
    for dest, info in entries:
        if isinstance(info, list):
            # FIX: convert all items to string before joining
            val = "AS-PATH: " + " ".join(map(str, info))
        elif isinstance(info, (list, tuple)):
            if len(info) >= 2:
                val = f"cost={info[0]}, next={info[1]}"
            else:
                val = str(info)
        else:
            val = str(info)

        c.drawString(x, y, f"{dest:12} {val}")
        y -= 11

def make_report():
    c = Canvas(str(REPORT_PATH), pagesize=A4)
    draw_title(c)
    add_obj_and_summary(c)

    # Page 1: RIP + OSPF
    add_topology_image(c, "rip_topology.png", 40, 480, caption="RIP Topology")
    add_topology_image(c, "ospf_topology.png", 320, 480, caption="OSPF Topology")
    add_table_snapshot(c, "rip_tables.json", 40, 320, max_entries=6)
    add_table_snapshot(c, "ospf_tables.json", 320, 320, max_entries=6)
    c.showPage()

    # Page 2: BGP + IS-IS
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, 800, "BGP and IS-IS Results")
    add_topology_image(c, "bgp_topology.png", 40, 540, caption="BGP AS-level Topology")
    add_topology_image(c, "isis_topology.png", 320, 540, caption="IS-IS Topology")
    add_table_snapshot(c, "bgp_tables.json", 40, 360, max_entries=6)
    add_table_snapshot(c, "isis_tables.json", 320, 360, max_entries=6)

    # Page 3: Observations
    c.showPage()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 800, "Observations & Comparison")
    c.setFont("Helvetica", 10)
    obs_text = (
        "RIP: Simple distance-vector; iterative updates until convergence. "
        "Slower convergence and higher message overhead for large networks.\n\n"
        "OSPF/IS-IS: Link-state protocols; each router builds full topology via LSAs "
        "and runs Dijkstra. Faster convergence, scalable, more overhead in flooding LSAs.\n\n"
        "BGP: Path-vector at AS-level. Routes selected by AS-PATH length here; loop prevention "
        "done by AS-PATH checks. Convergence depends on policy and AS relationships."
    )
    wrapped = textwrap.wrap(obs_text, width=100)
    y = 770
    for line in wrapped:
        c.drawString(40, y, line)
        y -= 12

    c.save()
    print("✅ Report generated successfully:", REPORT_PATH)

if __name__ == "__main__":
    make_report()


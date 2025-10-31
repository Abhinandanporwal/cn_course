from dataclasses import dataclass
from typing import List

@dataclass
class Packet:
    source_ip: str
    dest_ip: str
    payload: str
    priority: int  # 0=High, 1=Medium, 2=Low

def fifo_scheduler(packet_list: List[Packet]) -> List[Packet]:
    return list(packet_list)

def priority_scheduler(packet_list: List[Packet]) -> List[Packet]:
    return sorted(packet_list, key=lambda p: p.priority)

# Test block for scheduler
if __name__ == "__main__":
    packets = [
        Packet("10.0.0.1", "10.0.0.2", "Data Packet 1", priority=2),
        Packet("10.0.0.3", "10.0.0.4", "Data Packet 2", priority=2),
        Packet("10.0.0.5", "10.0.0.6", "VOIP Packet 1", priority=0),
        Packet("10.0.0.7", "10.0.0.8", "Video Packet 1", priority=1),
        Packet("10.0.0.9", "10.0.0.10", "VOIP Packet 2", priority=0),
    ]

    fifo_out = fifo_scheduler(packets)
    print("FIFO order:", [p.payload for p in fifo_out])

    prio_out = priority_scheduler(packets)
    print("Priority order:", [p.payload for p in prio_out])

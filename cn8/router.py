
from ip_utils import ip_to_binary, get_network_prefix
from typing import List, Tuple

class Router:
    def __init__(self, routes: List[Tuple[str, str]]):
        self._forwarding_table = []  # list of tuples (binary_prefix, prefix_length, output_link)
        self.build_forwarding_table(routes)

    def build_forwarding_table(self, routes: List[Tuple[str, str]]):
        table = []
        for cidr, out_link in routes:
            # get the binary prefix and length
            try:
                prefix_bits = get_network_prefix(cidr)
            except Exception as e:
                raise ValueError(f"Error parsing route {cidr}: {e}")
            table.append((prefix_bits, len(prefix_bits), out_link))
        # sort by prefix length descending (longest first)
        table.sort(key=lambda x: x[1], reverse=True)
        self._forwarding_table = table

    def route_packet(self, dest_ip: str) -> str:
        dest_bin = ip_to_binary(dest_ip)
        for prefix_bits, prefix_len, out_link in self._forwarding_table:
            if dest_bin.startswith(prefix_bits):
                return out_link
        return "Default Gateway"


# Test block for router
if __name__ == "__main__":
    routes = [
        ("223.1.1.0/24", "Link 0"),
        ("223.1.2.0/24", "Link 1"),
        ("223.1.3.0/24", "Link 2"),
        ("223.1.0.0/16", "Link 4 (ISP)")
    ]
    r = Router(routes)
    tests = {
        "223.1.1.100": "Link 0",
        "223.1.2.5": "Link 1",
        "223.1.250.1": "Link 4 (ISP)",
        "198.51.100.1": "Default Gateway"
    }
    for ip, expected in tests.items():
        result = r.route_packet(ip)
        print(ip, "->", result, "(expected:", expected, ")")

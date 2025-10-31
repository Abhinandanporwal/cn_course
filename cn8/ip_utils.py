
def ip_to_binary(ip_address: str) -> str:
    octets = ip_address.split('.')
    if len(octets) != 4:
        raise ValueError(f"Invalid IPv4 address: {ip_address}")
    bin_octets = []
    for o in octets:
        n = int(o)
        if n < 0 or n > 255:
            raise ValueError(f"Invalid octet value: {o}")
        bin_octets.append(f"{n:08b}")
    return ''.join(bin_octets)


def get_network_prefix(ip_cidr: str) -> str:
    try:
        ip_str, mask_str = ip_cidr.split('/')
    except ValueError:
        raise ValueError(f"Invalid CIDR notation: {ip_cidr}")
    mask_len = int(mask_str)
    if mask_len < 0 or mask_len > 32:
        raise ValueError(f"Invalid mask length: {mask_len}")
    ip_bin = ip_to_binary(ip_str)
    return ip_bin[:mask_len]


if __name__ == "__main__":
    print(ip_to_binary("192.168.1.1"))
    print(get_network_prefix("200.23.16.0/23"))

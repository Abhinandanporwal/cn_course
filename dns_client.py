import dns.resolver

def dns_client(domain="adobe.com"):
    try:
        print(f"Resolving DNS for: {domain}")

        try:
            for rdata in dns.resolver.resolve(domain, "A"):
                print("A Record:", rdata)
        except Exception:
            print("No A record found.")

        try:
            for rdata in dns.resolver.resolve(domain, "MX"):
                print("MX Record:", rdata)
        except Exception:
            print("No MX record found.")

        try:
            for rdata in dns.resolver.resolve(domain, "CNAME"):
                print("CNAME Record:", rdata)
        except Exception:
            print("No CNAME record found.")

        with open("dns_log.txt", "w") as f:
            f.write(f"DNS Query Results for {domain}\n")
            f.write("Check terminal output for record details.\n")

        print("Results saved to dns_log.txt")

    except Exception as e:
        print("DNS Error:", e)

if __name__ == "__main__":
    dns_client("adobe.com")
def scan_port(target_port, protocol="TCP"):
    print(f"Scanning port {target_port} using {protocol} protocol...")

# Call 1: Un-indented, passing exactly two arguments to override the default
scan_port(443, "UDP")

# Call 2: Un-indented, passing only ONE argument so the default TCP takes over
scan_port(22)
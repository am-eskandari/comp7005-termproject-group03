import re


def validate_ip(ip):
    """Validate IPv4 address format with graceful error handling."""
    try:
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if not pattern.match(ip):
            raise ValueError
        parts = ip.split(".")
        if any(int(part) < 0 or int(part) > 255 for part in parts):
            raise ValueError
    except ValueError:
        print(f"❌ Invalid IP address format: {ip}")
        print("IP address must be in the format 'X.X.X.X' with each octet between 0 and 255.")
        exit(1)
    return ip


def validate_port(port):
    """Validate port number with graceful error handling."""
    try:
        port = int(port)
        if not (1 <= port <= 65535):
            raise ValueError
    except ValueError:
        print(f"❌ Invalid port number: {port}. Must be an integer between 1 and 65535.")
        exit(1)
    return port

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
        if port <= 0:
            raise ValueError(f"Port numbers must be positive integers. Got: {port}")
        elif port < 1024:
            raise ValueError(f"Port {port} is valid but requires superuser access because it is below 1024.")
        elif port > 65535:
            raise ValueError(f"Port {port} exceeds the maximum allowable value (65535).")
    except ValueError as e:
        print(f"❌ {e}")
        exit(1)
    return port


def validate_chance(chance):
    """Validate drop or delay chance values."""
    try:
        # Convert the input to a float, regardless of type (handles strings or numbers)
        chance = float(chance)
        # Ensure the value is within the range [0.0, 1.0]
        if not (0.0 <= chance <= 1.0):
            raise ValueError(f"Chance value must be between 0.0 and 1.0. Got: {chance}")
    except ValueError as e:
        print(f"❌ Invalid chance value: {e}")
        exit(1)
    return chance


def validate_delay_time(delay_time):
    """Validate delay time in milliseconds or range."""
    try:
        if "-" in delay_time:
            min_val, max_val = map(int, delay_time.split("-"))
            # Validate that both values are positive and min is not greater than max
            if min_val < 0 or max_val < 0 or min_val > max_val:
                raise ValueError
            return min_val, max_val
        else:
            delay = int(delay_time)
            # Validate that the delay is non-negative (0 or positive)
            if delay < 0:
                raise ValueError
            return delay, delay
    except ValueError:
        print(f"❌ Invalid delay time: {delay_time}. Must be a non-negative integer or range (e.g., '100-500').")
        exit(1)

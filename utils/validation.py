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
        if not isinstance(chance, str) or chance.isdigit():
            raise ValueError(f"Chance value should be a decimal number. Got: {chance}")
        chance = float(chance)
        if not (0.0 <= chance <= 1.0):
            raise ValueError
    except ValueError:
        print(f"❌ Invalid chance value: {chance}. Must be a float between 0.0 and 1.0.")
        exit(1)
    return chance


def validate_delay_time(delay_time):
    """Validate delay time in milliseconds or range."""
    try:
        if not isinstance(delay_time, str) or delay_time.isdigit():
            raise ValueError(f"Delay time should be a positive integer or range. Got: {delay_time}")
        if "-" in delay_time:
            min_val, max_val = map(int, delay_time.split("-"))
            if min_val < 0 or max_val < 0 or min_val > max_val:
                raise ValueError(
                    f"Invalid delay range: {delay_time}. Minimum value must be less than or equal to maximum value, and both must be non-negative.")
            return min_val, max_val
        else:
            delay = int(delay_time)
            if delay < 0:
                raise ValueError(f"Delay time must be non-negative. Got: {delay}")
            return delay, delay
    except ValueError as e:
        print(f"❌ {e}")
        exit(1)

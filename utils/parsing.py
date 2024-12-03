import argparse

from utils.validation import validate_ip, validate_port, validate_chance, validate_delay_time


def parse_client():
    parser = argparse.ArgumentParser(description="UDP Client with Latency Tracking")
    parser.add_argument('--target-ip', required=True, help="Server IP address")
    parser.add_argument('--target-port', required=True, help="Server port")
    parser.add_argument('--timeout', required=True, help="Acknowledgment timeout in milliseconds")
    args = parser.parse_args()

    # Validate and process IP
    args.target_ip = validate_ip(args.target_ip)

    # Validate and process port
    args.target_port = validate_port(args.target_port)

    # Validate and process timeout
    try:
        timeout_ms = int(args.timeout)
        if timeout_ms <= 0:
            raise ValueError("Timeout must be a positive integer.")
    except ValueError as e:
        print(f"❌ Invalid timeout value: {args.timeout}. {e}")
        print("Timeout must be a positive integer in milliseconds.")
        exit(1)

    # Convert timeout to seconds for socket operations
    args.timeout = timeout_ms / 1000.0
    return args


def parse_proxy():
    parser = argparse.ArgumentParser(description="UDP Proxy Server with Logging and Delay Ranges")
    parser.add_argument('--listen-ip', required=True, help="Proxy server IP address")
    parser.add_argument('--listen-port', required=True, help="Proxy server port")
    parser.add_argument('--target-ip', required=True, help="Target server IP address")
    parser.add_argument('--target-port', required=True, help="Target server port")
    parser.add_argument('--client-drop', required=True, help="Drop chance (0.0 to 1.0) for client-to-server")
    parser.add_argument('--server-drop', required=True, help="Drop chance (0.0 to 1.0) for server-to-client")
    parser.add_argument('--client-delay', required=True, help="Delay chance (0.0 to 1.0) for client-to-server")
    parser.add_argument('--server-delay', required=True, help="Delay chance (0.0 to 1.0) for server-to-client")
    parser.add_argument('--client-delay-time', required=True,
                        help="Delay time for client-to-server (e.g., '100' or '100-500')")
    parser.add_argument('--server-delay-time', required=True,
                        help="Delay time for server-to-client (e.g., '100' or '100-500')")
    parser.add_argument('--control-port', required=True, help="Control port for dynamic configuration updates")
    args = parser.parse_args()

    # Validate arguments using validation functions
    args.listen_ip = validate_ip(args.listen_ip)
    args.listen_port = validate_port(args.listen_port)
    args.target_ip = validate_ip(args.target_ip)
    args.target_port = validate_port(args.target_port)
    args.control_port = validate_port(args.control_port)

    args.client_drop = validate_chance(args.client_drop)
    args.server_drop = validate_chance(args.server_drop)
    args.client_delay = validate_chance(args.client_delay)
    args.server_delay = validate_chance(args.server_delay)

    args.client_delay_time = validate_delay_time(args.client_delay_time)
    args.server_delay_time = validate_delay_time(args.server_delay_time)

    return args


def parse_server():
    parser = argparse.ArgumentParser(description="UDP Server with Latency Tracking")
    parser.add_argument('--listen-ip', required=True, help="IP address to bind")
    parser.add_argument('--listen-port', required=True, help="Port to listen on")
    arguments = parser.parse_args()

    # Validate and process IP
    arguments.listen_ip = validate_ip(arguments.listen_ip)

    # Validate and process port
    arguments.listen_port = validate_port(arguments.listen_port)

    return arguments

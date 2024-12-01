import argparse
import random
import socket
import threading
import time
from datetime import datetime

from utils.logger import proxy_logger, log_event
from utils.utils import handle_control
from utils.validation import validate_ip, validate_port, validate_chance, validate_delay_time

# Shared proxy configuration
proxy_config = {
    "client-drop": 0.0,
    "server-drop": 0.0,
    "client-delay": 0.0,
    "server-delay": 0.0,
    "client-delay-time": (0, 0),  # Tuple for range (min, max) in milliseconds
    "server-delay-time": (0, 0),  # Tuple for range (min, max) in milliseconds
}

# Cache for deduplication
dedup_cache = {
    "client_to_server": set(),
    "server_to_client": set(),
}

CACHE_TIMEOUT = 10  # Time in seconds to keep sequence numbers in cache


def clear_expired_cache():
    """Clear deduplication cache periodically to prevent memory bloat."""
    while True:
        time.sleep(CACHE_TIMEOUT)
        dedup_cache["client_to_server"].clear()
        dedup_cache["server_to_client"].clear()


def parse_arguments():
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


def udp_proxy(proxy_socket, server_ip, server_port):
    """
    A proxy server that forwards UDP packets with simulated unreliability.
    """
    client_address = None  # To keep track of the client address

    print(f"🚀 Proxy server started. Relaying packets between client and server.\n")

    while True:
        try:
            delay_time = 0  # Initialize delay_time to avoid unassigned variable error

            # Receive data from client or server
            start_time = datetime.now()
            data, addr = proxy_socket.recvfrom(65507)
            message = data.decode()

            # Handle "TERMINATE" messages
            if message == "TERMINATE":
                # Forward termination messages immediately to the server
                print(f"🚨 [Client -> Server] Termination message received from {addr}. Forwarding immediately.")
                destination = (server_ip, server_port)
                proxy_socket.sendto(data, destination)
                log_event(proxy_logger, 'Terminate', None, None, addr[0], addr[1], server_ip, server_port,
                          message, None)
                continue

            # Check if the message is an acknowledgment
            if message.startswith("ACK:"):
                seq_number = message.split(":")[1]
                is_ack = True
                message_content = None
            else:
                seq_number = message.split(":", 1)[0] if ":" in message else None
                is_ack = False
                message_content = message.split(":", 1)[1] if ":" in message else ""

            latency = (datetime.now() - start_time).total_seconds() * 1000

            # Identify if it's a client or server packet
            if addr != (server_ip, server_port):
                # Packet from the client
                client_address = addr  # Save the client address

                # Deduplication for client-to-server
                if not is_ack and seq_number in dedup_cache["client_to_server"]:
                    print(f"🔄 [Client -> Server] Duplicate packet [SEQ {seq_number}] from {addr}. Ignored.")
                    log_event(proxy_logger, 'Duplicate', seq_number, None, addr[0], addr[1], server_ip,
                              server_port, message_content, latency)
                    continue

                if not is_ack:
                    dedup_cache["client_to_server"].add(seq_number)

                if random.random() < proxy_config["client-drop"]:
                    print(f"❌ [Client -> Server] Dropped packet [SEQ {seq_number}] from {addr}")
                    log_event(proxy_logger, 'Dropped', seq_number, None, addr[0], addr[1], server_ip,
                              server_port, message_content, latency)
                    continue

                if random.random() < proxy_config["client-delay"]:
                    delay_time = random.randint(*proxy_config["client-delay-time"]) / 1000  # Convert ms to seconds
                    print(
                        f"⏳ [Client -> Server] Delayed packet [SEQ {seq_number}] from {addr} for {delay_time * 1000:.2f} ms")
                    time.sleep(delay_time)

                destination = (server_ip, server_port)
                print(f"✅ [Client -> Server] Forwarded packet [SEQ {seq_number}] to {destination}")
                log_event(proxy_logger, 'Forwarded', seq_number, None, addr[0], addr[1], server_ip, server_port,
                          message_content, latency)
            else:
                # Packet from the server
                if not client_address:
                    print("⚠️ No client address to forward to. Dropping packet.")
                    log_event(proxy_logger, 'Dropped', seq_number, None, addr[0], addr[1], server_ip,
                              server_port, message_content, latency)
                    continue

                # Deduplication for server-to-client
                if is_ack and seq_number in dedup_cache["server_to_client"]:
                    print(f"🔄 [Server -> Client] Duplicate acknowledgment [ACK {seq_number}] from {addr}. Ignored.")
                    log_event(proxy_logger, 'Duplicate', seq_number, seq_number, addr[0], addr[1],
                              client_address[0], client_address[1], None, latency)
                    continue

                if is_ack:
                    dedup_cache["server_to_client"].add(seq_number)

                if random.random() < proxy_config["server-drop"]:
                    print(f"❌ [Server -> Client] Dropped packet [SEQ {seq_number}] from {addr}")
                    log_event(proxy_logger, 'Dropped', seq_number, None, addr[0], addr[1], client_address[0],
                              client_address[1], None, latency)
                    continue

                if random.random() < proxy_config["server-delay"]:
                    delay_time = random.randint(*proxy_config["server-delay-time"]) / 1000  # Convert ms to seconds
                    print(
                        f"⏳ [Server -> Client] Delayed packet [SEQ {seq_number}] from {addr} for {delay_time * 1000:.2f} ms")
                    time.sleep(delay_time)

                destination = client_address
                print(f"✅ [Server -> Client] Forwarded packet [SEQ {seq_number}] to {destination}")
                log_event(proxy_logger, 'Forwarded', seq_number, seq_number, addr[0], addr[1], client_address[0],
                          client_address[1], None, latency)

            # Forward the packet
            proxy_socket.sendto(data, destination)

        except Exception as e:
            print(f"❌ Proxy server error: {e}")


def main():
    args = parse_arguments()

    # Proxy configuration initialization
    proxy_config["client-drop"] = args.client_drop
    proxy_config["server-drop"] = args.server_drop
    proxy_config["client-delay"] = args.client_delay
    proxy_config["server-delay"] = args.server_delay
    proxy_config["client-delay-time"] = args.client_delay_time
    proxy_config["server-delay-time"] = args.server_delay_time

    # Set up proxy socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    proxy_socket.bind((args.listen_ip, args.listen_port))
    print(f"🌐 Proxy server listening on {args.listen_ip}:{args.listen_port}")

    # Set up control socket
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    control_socket.bind((args.listen_ip, args.control_port))
    print(f"🔧 Control interface listening on {args.listen_ip}:{args.control_port}")

    threading.Thread(target=udp_proxy, args=(proxy_socket, args.target_ip, args.target_port), daemon=True).start()
    threading.Thread(target=handle_control, args=(control_socket, proxy_config), daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down proxy server. Goodbye!")


if __name__ == "__main__":
    main()

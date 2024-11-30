import socket
import random
import time
import argparse
import threading
import json
import csv
from datetime import datetime

# Shared proxy configuration
proxy_config = {
    "client-drop": 0.0,
    "server-drop": 0.0,
    "client-delay": 0.0,
    "server-delay": 0.0,
    "client-delay-time": 0.0,  # Now in milliseconds
    "server-delay-time": 0.0,  # Now in milliseconds
}

# Cache for deduplication
dedup_cache = {
    "client_to_server": set(),
    "server_to_client": set(),
}

CACHE_TIMEOUT = 10  # Time in seconds to keep sequence numbers in cache

LOG_FILE = "log_proxy.csv"

# Initialize the log file
with open(LOG_FILE, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([
        "Timestamp", "Event", "Sequence", "Acknowledgment",
        "Source IP", "Source Port", "Destination IP", "Destination Port",
        "Message", "Latency (ms)", "Drop Chance", "Delay Chance", "Delay Time (ms)"
    ])


def log_event(event, seq_number, ack_number, src_ip, src_port, dest_ip, dest_port, message, latency, drop_chance, delay_chance, delay_time):
    """Log an event to the CSV file."""
    with open(LOG_FILE, "a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), event, seq_number, ack_number,
            src_ip, src_port, dest_ip, dest_port, message, latency, drop_chance, delay_chance, delay_time
        ])


def clear_expired_cache():
    """Clear deduplication cache periodically to prevent memory bloat."""
    while True:
        time.sleep(CACHE_TIMEOUT)
        dedup_cache["client_to_server"].clear()
        dedup_cache["server_to_client"].clear()


def parse_arguments():
    parser = argparse.ArgumentParser(description="UDP Proxy Server with Logging")
    parser.add_argument('--listen-ip', required=True, help="Proxy server IP address")
    parser.add_argument('--listen-port', type=int, required=True, help="Proxy server port")
    parser.add_argument('--target-ip', required=True, help="Target server IP address")
    parser.add_argument('--target-port', type=int, required=True, help="Target server port")
    parser.add_argument('--client-drop', type=float, default=0.0, help="Drop chance (0.0 to 1.0) for client-to-server")
    parser.add_argument('--server-drop', type=float, default=0.0, help="Drop chance (0.0 to 1.0) for server-to-client")
    parser.add_argument('--client-delay', type=float, default=0.0, help="Delay chance (0.0 to 1.0) for client-to-server")
    parser.add_argument('--server-delay', type=float, default=0.0, help="Delay chance (0.0 to 1.0) for server-to-client")
    parser.add_argument('--client-delay-time', type=float, default=0.0,
                        help="Delay time for client-to-server in milliseconds")
    parser.add_argument('--server-delay-time', type=float, default=0.0,
                        help="Delay time for server-to-client in milliseconds")
    parser.add_argument('--control-port', type=int, default=4500, help="Port for dynamic configuration control")
    return parser.parse_args()


def udp_proxy(proxy_socket, server_ip, server_port):
    """
    A proxy server that forwards UDP packets with simulated unreliability.
    """
    client_address = None  # To keep track of the client address

    print(f"🚀 Proxy server started. Relaying packets between client and server.\n")

    while True:
        try:
            # Receive data from client or server
            start_time = datetime.now()
            data, addr = proxy_socket.recvfrom(65507)
            message = data.decode()

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
                    log_event("Duplicate", seq_number, None, addr[0], addr[1], server_ip, server_port, message_content, latency, proxy_config["client-drop"], proxy_config["client-delay"], 0)
                    continue

                if not is_ack:
                    dedup_cache["client_to_server"].add(seq_number)

                if random.random() < proxy_config["client-drop"]:
                    print(f"❌ [Client -> Server] Dropped packet [SEQ {seq_number}] from {addr}")
                    log_event("Dropped", seq_number, None, addr[0], addr[1], server_ip, server_port, message_content, latency, proxy_config["client-drop"], proxy_config["client-delay"], 0)
                    continue
                if random.random() < proxy_config["client-delay"]:
                    delay_time = proxy_config["client-delay-time"] / 1000  # Convert ms to seconds
                    print(f"⏳ [Client -> Server] Delayed packet [SEQ {seq_number}] from {addr} "
                          f"for {delay_time * 1000:.2f} ms")
                    time.sleep(delay_time)
                destination = (server_ip, server_port)
                print(f"✅ [Client -> Server] Forwarded packet [SEQ {seq_number}] to {destination}")
                log_event("Forwarded", seq_number, None, addr[0], addr[1], server_ip, server_port, message_content, latency, proxy_config["client-drop"], proxy_config["client-delay"], proxy_config["client-delay-time"])
            else:
                # Packet from the server
                if not client_address:
                    print("⚠️ No client address to forward to. Dropping packet.")
                    log_event("Dropped", seq_number, None, addr[0], addr[1], server_ip, server_port, message_content, latency, proxy_config["server-drop"], proxy_config["server-delay"], 0)
                    continue

                # Deduplication for server-to-client
                if is_ack and seq_number in dedup_cache["server_to_client"]:
                    print(f"🔄 [Server -> Client] Duplicate acknowledgment [ACK {seq_number}] from {addr}. Ignored.")
                    log_event("Duplicate", seq_number, seq_number, addr[0], addr[1], client_address[0], client_address[1], None, latency, proxy_config["server-drop"], proxy_config["server-delay"], 0)
                    continue

                if is_ack:
                    dedup_cache["server_to_client"].add(seq_number)

                if random.random() < proxy_config["server-drop"]:
                    print(f"❌ [Server -> Client] Dropped packet [SEQ {seq_number}] from {addr}")
                    log_event("Dropped", seq_number, None, addr[0], addr[1], client_address[0], client_address[1], None, latency, proxy_config["server-drop"], proxy_config["server-delay"], 0)
                    continue
                if random.random() < proxy_config["server-delay"]:
                    delay_time = proxy_config["server-delay-time"] / 1000  # Convert ms to seconds
                    print(f"⏳ [Server -> Client] Delayed packet [SEQ {seq_number}] from {addr} "
                          f"for {delay_time * 1000:.2f} ms")
                    time.sleep(delay_time)
                destination = client_address
                print(f"✅ [Server -> Client] Forwarded packet [SEQ {seq_number}] to {destination}")
                log_event("Forwarded", seq_number, seq_number, addr[0], addr[1], client_address[0], client_address[1], None, latency, proxy_config["server-drop"], proxy_config["server-delay"], proxy_config["server-delay-time"])

            # Forward the packet
            proxy_socket.sendto(data, destination)

        except Exception as e:
            print(f"❌ Proxy server error: {e}")


def handle_control(control_socket):
    """
    Control interface for dynamic parameter updates.
    """
    print(f"🛠️ Control interface active. Use the control port to dynamically update parameters.\n")
    while True:
        try:
            data, addr = control_socket.recvfrom(1024)
            command = data.decode().strip()
            print(f"📝 Received control command: {command}")

            if command.startswith("SET"):
                _, param, value = command.split()
                value = float(value)
                if param in proxy_config:
                    proxy_config[param] = value
                    response = f"✅ Updated {param} to {value}"
                    print(f"🔧 {response}")
                else:
                    response = f"❌ Invalid parameter: {param}"
                control_socket.sendto(response.encode(), addr)

            elif command.startswith("GET"):
                response = json.dumps(proxy_config)
                print(f"📤 Sent current configuration: {response}")
                control_socket.sendto(response.encode(), addr)

            else:
                response = "❌ Unknown command"
                print(f"⚠️ {response}")
                control_socket.sendto(response.encode(), addr)

        except Exception as e:
            print(f"❌ Error in control interface: {e}")


def main():
    args = parse_arguments()

    # Initialize proxy configuration from CLI arguments
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
    print(f"🛠️ Control interface listening on {args.listen_ip}:{args.control_port}")

    # Start proxy and control threads
    threading.Thread(target=udp_proxy, args=(proxy_socket, args.target_ip, args.target_port), daemon=True).start()
    threading.Thread(target=handle_control, args=(control_socket,), daemon=True).start()
    threading.Thread(target=clear_expired_cache, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down proxy server. Goodbye!")


if __name__ == "__main__":
    main()

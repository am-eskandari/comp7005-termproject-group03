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

# Dictionary to store delayed packets
delayed_packets = {
    "client-to-server": [],
    "server-to-client": []
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


ack_tracking_cache = {}  # Tracks ACK packets for potential retries


def process_delayed_packets():
    """Thread function to forward delayed packets once their delay time expires."""
    while True:
        current_time = time.time()
        for direction in ["client-to-server", "server-to-client"]:
            remaining_packets = []
            for packet in delayed_packets[direction]:
                send_time, data, destination, addr = packet
                if current_time >= send_time:
                    try:
                        proxy_socket.sendto(data, destination)
                        print(f"✅ [{addr} -> {destination}] Forwarded delayed packet [SEQ {data.decode()}]")
                        log_event(proxy_logger, 'Forwarded Delayed', None, None, addr[0], addr[1],
                                  destination[0], destination[1], None, None)
                    except Exception as e:
                        print(f"❌ Error forwarding delayed packet: {e}")
                else:
                    remaining_packets.append(packet)
            delayed_packets[direction] = remaining_packets
        time.sleep(0.01)  # Sleep briefly to prevent CPU overuse


def handle_drops_and_delays(seq_number, addr, message_content, is_ack, direction, proxy_socket, target_ip, target_port,
                            data):
    """
    Handles drops and delays for packets in both directions.
    """
    config_prefix = "client" if direction == "client-to-server" else "server"

    # Simulate drop
    if random.random() < proxy_config[f"{config_prefix}-drop"]:
        print(f"❌ [{direction}] Dropped packet [SEQ {seq_number}] from {addr}")
        log_event(proxy_logger, 'Dropped', seq_number, None, addr[0], addr[1], target_ip, target_port,
                  message_content, None)
        return False

    # Simulate delay
    if random.random() < proxy_config[f"{config_prefix}-delay"]:
        delay_time = random.randint(*proxy_config[f"{config_prefix}-delay-time"]) / 1000  # Convert ms to seconds
        send_time = time.time() + delay_time  # Calculate the future send time
        delayed_packets[direction].append((send_time, data, (target_ip, target_port), addr))
        print(
            f"⏳ [{direction}] Scheduled packet [SEQ {seq_number}] from {addr} to be forwarded after {delay_time * 1000:.2f} ms")
        log_event(proxy_logger, 'Delayed', seq_number, None, addr[0], addr[1], target_ip, target_port,
                  message_content, None)
        return False

    # Example conditional for is_ack
    if is_ack:
        print(f"🟢 Acknowledgment packet [SEQ {seq_number}] handled with delay or drop logic.")

    return True


def udp_proxy(proxy_socket, server_ip, server_port):
    """
    A proxy server that forwards UDP packets with simulated unreliability.
    """
    client_address = None  # To keep track of the client address

    # Dictionary to track timestamps for accurate latency reporting
    packet_timestamps = {}

    print(f"🚀 Proxy server started. Relaying packets between client and server.\n")

    while True:
        try:
            # Receive data from client or server
            receive_time = datetime.now()
            data, addr = proxy_socket.recvfrom(65507)
            message = data.decode()

            # Handle "TERMINATE" messages
            if message == "TERMINATE":
                print(f"🚨 [Client -> Server] Termination message received from {addr}. Forwarding immediately.")
                destination = (server_ip, server_port)
                proxy_socket.sendto(data, destination)
                log_event(proxy_logger, 'Terminate', None, None, addr[0], addr[1], server_ip, server_port,
                          message, None)
                continue

            # Check if the message is an acknowledgment or RESEND_ACK
            if message.startswith("ACK:"):
                seq_number = message.split(":")[1]
                is_ack = True
                message_content = None
            elif message.startswith("RESEND_ACK:"):
                seq_number = message.split(":")[1]
                print(f"🔄 Proxy received RESEND_ACK for SEQ {seq_number} from {addr}.")
                # Forward the RESEND_ACK without treating it as a normal sequence
                proxy_socket.sendto(data, (server_ip, server_port))
                continue
            else:
                seq_number = message.split(":", 1)[0] if ":" in message else None
                is_ack = False
                message_content = message.split(":", 1)[1] if ":" in message else ""

            try:
                seq_number = int(seq_number)  # Validate sequence number
            except ValueError:
                print(f"⚠️ Proxy ignored invalid sequence: {seq_number}.")
                continue

            # Handle client-to-server packets
            if addr != (server_ip, server_port):
                client_address = addr  # Save the client address

                # Handle drops and delays for client-to-server
                if not handle_drops_and_delays(seq_number, addr, message_content, is_ack, "client-to-server",
                                               proxy_socket, server_ip, server_port, data):
                    continue  # Packet was dropped, no need to forward

                destination = (server_ip, server_port)

            # Handle server-to-client packets
            else:
                if not client_address:
                    print("⚠️ No client address to forward to. Dropping packet.")
                    log_event(proxy_logger, 'Dropped', seq_number, None, addr[0], addr[1], server_ip,
                              server_port, message_content, None)
                    continue

                # Track acknowledgments for retries
                if is_ack:
                    ack_tracking_cache[seq_number] = (data, client_address)

                # Handle drops and delays for server-to-client
                if not handle_drops_and_delays(seq_number, addr, None, is_ack, "server-to-client", proxy_socket,
                                               client_address[0], client_address[1], data):
                    continue  # Packet was dropped, no need to forward

                destination = client_address

            # Calculate latency for forwarding
            forward_time = datetime.now()
            total_latency = (forward_time - receive_time).total_seconds() * 1000

            # Store the receive timestamp for tracking
            packet_timestamps[seq_number] = receive_time

            # Forward the packet
            proxy_socket.sendto(data, destination)
            print(f"✅ [{addr} -> {destination}] Forwarded packet [SEQ {seq_number}] (Latency: {total_latency:.2f} ms)")
            log_event(proxy_logger, 'Forwarded', seq_number, seq_number if is_ack else None, addr[0], addr[1],
                      destination[0], destination[1], None, total_latency)

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
    global proxy_socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    proxy_socket.bind((args.listen_ip, args.listen_port))
    print(f"🌐 Proxy server listening on {args.listen_ip}:{args.listen_port}")

    # Set up control socket
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    control_socket.bind((args.listen_ip, args.control_port))
    print(f"🔧 Control interface listening on {args.listen_ip}:{args.control_port}")

    # Start delayed packet handler thread
    threading.Thread(target=process_delayed_packets, daemon=True).start()

    threading.Thread(target=udp_proxy, args=(proxy_socket, args.target_ip, args.target_port), daemon=True).start()
    threading.Thread(target=handle_control, args=(control_socket, proxy_config), daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down proxy server. Goodbye!")


if __name__ == "__main__":
    main()

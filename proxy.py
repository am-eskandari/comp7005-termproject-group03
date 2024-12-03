import random
import socket
import threading
import time
from datetime import datetime

from utils.controller import handle_control
from utils.logger import proxy_logger, log_event
from utils.parsing import parse_proxy

# Shared proxy configuration
proxy_config = {
    "client-drop": 0.0,
    "server-drop": 0.0,
    "client-delay": 0.0,
    "server-delay": 0.0,
    "client-delay-time": (0, 0),  # Tuple for range (min, max) in milliseconds
    "server-delay-time": (0, 0),  # Tuple for range (min, max) in milliseconds
}

# Dictionary to store delayed packets
delayed_packets = {
    "client-to-server": [],
    "server-to-client": []
}

# Deduplication cache with timestamps
dedup_cache = {
    "client-to-server": {},  # Maps sequence numbers to their receive time
    "server-to-client": {}  # Same for ACKs
}
CACHE_TIMEOUT = 10  # Cache timeout in seconds

# Track last acknowledged sequence for handling retransmissions
last_acknowledged_sequence = {
    "client-to-server": 0,
    "server-to-client": 0
}


def is_retransmission(direction, seq_number):
    """
    Check if the packet is a retransmission based on the last acknowledged sequence number.
    """
    return seq_number > last_acknowledged_sequence[direction]


def cleanup_cache(direction):
    """
    Cleanup expired entries in the deduplication cache.
    """
    current_time = time.time()
    dedup_cache[direction] = {
        seq: ts for seq, ts in dedup_cache[direction].items()
        if current_time - ts < CACHE_TIMEOUT
    }


def clear_expired_cache():
    """Clear deduplication cache periodically to prevent memory bloat."""
    while True:
        time.sleep(CACHE_TIMEOUT)
        dedup_cache["client_to_server"].clear()
        dedup_cache["server_to_client"].clear()


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


# Shared lock for thread-safe access to proxy_config
proxy_config_lock = threading.Lock()


def handle_drops_and_delays(seq_number, addr, message_content, is_ack, direction, proxy_socket, target_ip, target_port,
                            data):
    """
    Handles drops and delays for packets in both directions.
    """
    config_prefix = "client" if direction == "client-to-server" else "server"

    # Acquire the lock to ensure thread-safe access to proxy_config
    print(f"🔒 Acquiring lock for drop/delay configuration...")
    with proxy_config_lock:
        print(f"🔑 Lock acquired for drop/delay configuration.")

        # Simulate drop
        if random.random() < proxy_config[f"{config_prefix}-drop"]:
            print(f"❌ [{direction}] Dropped packet [SEQ {seq_number}] from {addr}")
            log_event(proxy_logger, 'Dropped', seq_number, None, addr[0], addr[1], target_ip, target_port,
                      message_content, None)
            print(f"🔓 Lock released after drop check.")
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
            print(f"🔓 Lock released after delay scheduling.")
            return False

    print(f"🔓 Lock released after drop/delay handling.")

    # Example conditional for is_ack
    if is_ack:
        print(f"🟢 Acknowledgment packet [SEQ {seq_number}] handled with delay or drop logic.")

    return True


def udp_proxy(proxy_socket, server_ip, server_port):
    """
    A proxy server that forwards UDP packets with simulated unreliability.
    """
    client_address = None  # To keep track of the client address

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

            # Parse message type and sequence number
            if message.startswith("ACK:"):
                seq_number = int(message.split(":")[1])
                is_ack = True
                message_content = None
            elif message.startswith("RESEND_ACK:"):
                seq_number = int(message.split(":")[1])
                print(f"🔄 Proxy received RESEND_ACK for SEQ {seq_number} from {addr}.")
                proxy_socket.sendto(data, (server_ip, server_port))
                continue
            else:
                seq_number = int(message.split(":", 1)[0])
                is_ack = False
                message_content = message.split(":", 1)[1] if ":" in message else ""

            # Determine packet direction
            if addr != (server_ip, server_port):
                direction = "client-to-server"
                destination = (server_ip, server_port)
                client_address = addr
            else:
                direction = "server-to-client"
                if not client_address:
                    print("⚠️ No client address to forward to. Dropping packet.")
                    log_event(proxy_logger, 'Dropped', seq_number, None, addr[0], addr[1], server_ip,
                              server_port, message_content, None)
                    continue
                destination = client_address

            # Cleanup deduplication cache
            cleanup_cache(direction)

            # Check for duplicates or retransmissions
            if seq_number <= last_acknowledged_sequence[direction]:
                print(f"🔄 Duplicate or retransmitted packet [SEQ {seq_number}] detected in {direction}.")
                if seq_number == last_acknowledged_sequence[direction]:
                    print(f"🟢 Retransmission of acknowledged sequence {seq_number}. Forwarding.")
                else:
                    log_event(proxy_logger, 'Duplicate', seq_number, None, addr[0], addr[1], destination[0],
                              destination[1], None, None)
                    continue

            # Update deduplication cache and last acknowledged sequence
            dedup_cache[direction][seq_number] = time.time()
            if is_ack:
                last_acknowledged_sequence[direction] = max(last_acknowledged_sequence[direction], seq_number)

            # Handle drops and delays
            if not handle_drops_and_delays(seq_number, addr, message_content, is_ack, direction, proxy_socket,
                                           destination[0], destination[1], data):
                continue  # Packet was dropped or delayed, no need to forward

            # Forward the packet
            proxy_socket.sendto(data, destination)
            print(f"✅ [{addr} -> {destination}] Forwarded packet [SEQ {seq_number}]")
            log_event(proxy_logger, 'Forwarded', seq_number, seq_number if is_ack else None, addr[0], addr[1],
                      destination[0], destination[1], None, None)

        except Exception as e:
            print(f"❌ Proxy server error: {e}")


def main():
    args = parse_proxy()

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

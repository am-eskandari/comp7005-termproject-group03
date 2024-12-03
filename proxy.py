import random
import socket
import threading
import time
from datetime import datetime

from utils.controller import handle_control
from utils.logger import proxy_logger, log_event
from utils.parsing import parse_proxy


class DelayedPacketHandler:
    """Manages delayed packets in both directions."""

    def __init__(self):
        self.delayed_packets = {
            "client-to-server": [],
            "server-to-client": []
        }

    def add_packet(self, direction, send_time, data, destination, addr):
        self.delayed_packets[direction].append((send_time, data, destination, addr))

    def process_packets(self, proxy_socket):
        """Forward delayed packets once their delay time expires."""
        while True:
            current_time = time.time()
            for direction in ["client-to-server", "server-to-client"]:
                remaining_packets = []
                for packet in self.delayed_packets[direction]:
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
                self.delayed_packets[direction] = remaining_packets
            time.sleep(0.01)


class UDPProxy:
    """Encapsulates the UDP Proxy behavior."""

    def __init__(self, listen_ip, listen_port, target_ip, target_port, control_port, proxy_config):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.target_ip = target_ip
        self.target_port = target_port
        self.control_port = control_port
        self.proxy_config = proxy_config

        self.proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.client_address = None
        self.packet_timestamps = {}
        self.ack_tracking_cache = {}

        self.delayed_packet_handler = DelayedPacketHandler()

    def setup_sockets(self):
        """Bind the sockets for proxy and control communication."""
        self.proxy_socket.bind((self.listen_ip, self.listen_port))
        self.control_socket.bind((self.listen_ip, self.control_port))
        print(f"🌐 Proxy server listening on {self.listen_ip}:{self.listen_port}")
        print(f"🔧 Control interface listening on {self.listen_ip}:{self.control_port}")

    def handle_drops_and_delays(self, seq_number, addr, message_content, is_ack, direction, data):
        """Handles drops and delays for packets in both directions."""
        config_prefix = "client" if direction == "client-to-server" else "server"

        # Simulate drop
        if random.random() < self.proxy_config[f"{config_prefix}-drop"]:
            print(f"❌ [{direction}] Dropped packet [SEQ {seq_number}] from {addr}")
            log_event(proxy_logger, 'Dropped', seq_number, None, addr[0], addr[1],
                      self.target_ip, self.target_port, message_content, None)
            return False

        # Simulate delay
        if random.random() < self.proxy_config[f"{config_prefix}-delay"]:
            delay_time = random.randint(
                *self.proxy_config[f"{config_prefix}-delay-time"]) / 1000  # Convert ms to seconds
            send_time = time.time() + delay_time
            self.delayed_packet_handler.add_packet(direction, send_time, data, (self.target_ip, self.target_port), addr)
            print(f"⏳ [{direction}] Scheduled packet [SEQ {seq_number}] from {addr} to be forwarded after "
                  f"{delay_time * 1000:.2f} ms")
            log_event(proxy_logger, 'Delayed', seq_number, None, addr[0], addr[1],
                      self.target_ip, self.target_port, message_content, None)
            return False

        if is_ack:
            print(f"🟢 Acknowledgment packet [SEQ {seq_number}] handled with delay or drop logic.")
        return True

    def proxy_loop(self):
        """Main proxy loop for handling client-to-server and server-to-client packets."""
        print("🚀 Proxy server started. Relaying packets between client and server.\n")

        while True:
            try:
                # Receive data from client or server
                receive_time = datetime.now()
                data, addr = self.proxy_socket.recvfrom(65507)
                message = data.decode()

                # Handle "TERMINATE" messages
                if message == "TERMINATE":
                    print(f"🚨 [Client -> Server] Termination message received from {addr}. Forwarding immediately.")
                    self.proxy_socket.sendto(data, (self.target_ip, self.target_port))
                    log_event(proxy_logger, 'Terminate', None, None, addr[0], addr[1], self.target_ip, self.target_port,
                              message, None)
                    continue

                # Parse sequence number and direction
                seq_number, is_ack, message_content = self.parse_message(message)
                if seq_number is None:
                    continue  # Invalid sequence, ignore

                if addr != (self.target_ip, self.target_port):  # Client-to-server
                    self.client_address = addr
                    if not self.handle_drops_and_delays(seq_number, addr, message_content, is_ack,
                                                        "client-to-server", data):
                        continue
                    destination = (self.target_ip, self.target_port)
                else:  # Server-to-client
                    if not self.client_address:
                        print("⚠️ No client address to forward to. Dropping packet.")
                        continue
                    if not self.handle_drops_and_delays(seq_number, addr, None, is_ack,
                                                        "server-to-client", data):
                        continue
                    destination = self.client_address

                self.forward_packet(data, addr, destination, seq_number, receive_time)

            except Exception as e:
                print(f"❌ Proxy server error: {e}")

    @staticmethod
    def parse_message(message):
        """Parses the message and extracts sequence number and acknowledgment flag."""
        if message.startswith("ACK:"):
            seq_number = message.split(":")[1]
            is_ack = True
            message_content = None
        elif message.startswith("RESEND_ACK:"):
            seq_number = message.split(":")[1]
            print(f"🔄 Proxy received RESEND_ACK for SEQ {seq_number}.")
            return None, None, None  # RESEND_ACK is handled differently
        else:
            seq_number = message.split(":", 1)[0] if ":" in message else None
            is_ack = False
            message_content = message.split(":", 1)[1] if ":" in message else ""
        try:
            seq_number = int(seq_number)
        except ValueError:
            print(f"⚠️ Proxy ignored invalid sequence: {seq_number}.")
            return None, None, None
        return seq_number, is_ack, message_content

    def forward_packet(self, data, addr, destination, seq_number, receive_time):
        """Forward packets and log events."""
        self.proxy_socket.sendto(data, destination)
        forward_time = datetime.now()
        total_latency = (forward_time - receive_time).total_seconds() * 1000
        print(f"✅ [{addr} -> {destination}] Forwarded packet [SEQ {seq_number}] (Latency: {total_latency:.2f} ms)")
        log_event(proxy_logger, 'Forwarded', seq_number, None, addr[0], addr[1],
                  destination[0], destination[1], None, total_latency)


def main():
    args = parse_proxy()

    # Initialize proxy configuration
    proxy_config = {
        "client-drop": args.client_drop,
        "server-drop": args.server_drop,
        "client-delay": args.client_delay,
        "server-delay": args.server_delay,
        "client-delay-time": args.client_delay_time,
        "server-delay-time": args.server_delay_time,
    }

    # Create proxy instance
    udp_proxy = UDPProxy(
        listen_ip=args.listen_ip,
        listen_port=args.listen_port,
        target_ip=args.target_ip,
        target_port=args.target_port,
        control_port=args.control_port,
        proxy_config=proxy_config
    )

    # Setup sockets
    udp_proxy.setup_sockets()

    # Start threads
    threading.Thread(target=udp_proxy.proxy_loop, daemon=True).start()
    threading.Thread(target=udp_proxy.delayed_packet_handler.process_packets,
                     args=(udp_proxy.proxy_socket,), daemon=True).start()
    threading.Thread(target=handle_control, args=(udp_proxy.control_socket, proxy_config), daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down proxy server. Goodbye!")


if __name__ == "__main__":
    main()

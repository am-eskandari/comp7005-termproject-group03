import socket
import random
import time
import argparse
import threading
import json

# Shared proxy configuration
proxy_config = {
    "client-drop": 0.0,
    "server-drop": 0.0,
    "client-delay": 0.0,
    "server-delay": 0.0,
    "client-delay-time": 0.0,
    "server-delay-time": 0.0,
}


def parse_arguments():
    parser = argparse.ArgumentParser(description="UDP Proxy Server with Dynamic Configuration")
    parser.add_argument('--listen-ip', required=True, help="Proxy server IP address")
    parser.add_argument('--listen-port', type=int, required=True, help="Proxy server port")
    parser.add_argument('--target-ip', required=True, help="Target server IP address")
    parser.add_argument('--target-port', type=int, required=True, help="Target server port")
    parser.add_argument('--client-drop', type=float, default=0.0, help="Drop chance (0.0 to 1.0) for client-to-server")
    parser.add_argument('--server-drop', type=float, default=0.0, help="Drop chance (0.0 to 1.0) for server-to-client")
    parser.add_argument('--client-delay', type=float, default=0.0, help="Delay chance (0.0 to 1.0) for client-to-server")
    parser.add_argument('--server-delay', type=float, default=0.0, help="Delay chance (0.0 to 1.0) for server-to-client")
    parser.add_argument('--client-delay-time', type=float, default=0.0, help="Delay time for client-to-server (seconds)")
    parser.add_argument('--server-delay-time', type=float, default=0.0, help="Delay time for server-to-client (seconds)")
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
            data, addr = proxy_socket.recvfrom(65507)

            # Log incoming packet details
            if ":" in data.decode():
                seq_number, payload = data.decode().split(":", 1)
            else:
                seq_number, payload = None, data.decode()

            # Identify if it's a client or server packet
            if addr != (server_ip, server_port):
                # Packet from the client
                client_address = addr  # Save the client address
                if random.random() < proxy_config["client-drop"]:
                    print(f"❌ [Client -> Server] Dropped packet [SEQ {seq_number}] from {addr}")
                    continue
                if random.random() < proxy_config["client-delay"]:
                    print(f"⏳ [Client -> Server] Delayed packet [SEQ {seq_number}] from {addr} "
                          f"for {proxy_config['client-delay-time']} seconds")
                    time.sleep(proxy_config["client-delay-time"])
                destination = (server_ip, server_port)
                print(f"✅ [Client -> Server] Forwarded packet [SEQ {seq_number}] to {destination}")
            else:
                # Packet from the server
                if not client_address:
                    print("⚠️ No client address to forward to. Dropping packet.")
                    continue
                if random.random() < proxy_config["server-drop"]:
                    print(f"❌ [Server -> Client] Dropped packet [SEQ {seq_number}] from {addr}")
                    continue
                if random.random() < proxy_config["server-delay"]:
                    print(f"⏳ [Server -> Client] Delayed packet [SEQ {seq_number}] from {addr} "
                          f"for {proxy_config['server-delay-time']} seconds")
                    time.sleep(proxy_config["server-delay-time"])
                destination = client_address
                print(f"✅ [Server -> Client] Forwarded packet [SEQ {seq_number}] to {destination}")

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

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down proxy server. Goodbye!")


if __name__ == "__main__":
    main()

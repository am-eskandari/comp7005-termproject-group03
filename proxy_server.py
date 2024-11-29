import socket
import random
import time
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="UDP Proxy Server")
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
    return parser.parse_args()


def udp_proxy(listen_ip, listen_port, server_ip, server_port,
              client_drop=0.0, server_drop=0.0, client_delay=0.0,
              server_delay=0.0, client_delay_time=0.0, server_delay_time=0.0):
    """
    A proxy server that forwards UDP packets with simulated unreliability.
    """
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    proxy_socket.bind((listen_ip, listen_port))
    print(f"Proxy server listening on {listen_ip}:{listen_port}")

    client_address = None  # To keep track of the client address

    while True:
        try:
            # Receive data from client or server
            data, addr = proxy_socket.recvfrom(65507)

            # Identify if it's a client or server packet
            if addr != (server_ip, server_port):
                # Packet from the client
                client_address = addr  # Save the client address
                if random.random() < client_drop:
                    print(f"Dropping packet from client {addr}")
                    continue
                if random.random() < client_delay:
                    print(f"Delaying packet from client {addr} for {client_delay_time} seconds")
                    time.sleep(client_delay_time)
                destination = (server_ip, server_port)
                print(f"Forwarding packet from client {addr} to server {destination}")
            else:
                # Packet from the server
                if not client_address:
                    print("No client address to forward to. Dropping packet.")
                    continue
                if random.random() < server_drop:
                    print(f"Dropping packet from server {addr}")
                    continue
                if random.random() < server_delay:
                    print(f"Delaying packet from server {addr} for {server_delay_time} seconds")
                    time.sleep(server_delay_time)
                destination = client_address
                print(f"Forwarding packet from server {addr} to client {destination}")

            # Forward the packet
            proxy_socket.sendto(data, destination)

        except Exception as e:
            print(f"Proxy server error: {e}")



if __name__ == "__main__":
    args = parse_arguments()
    udp_proxy(
        args.listen_ip, args.listen_port, args.target_ip, args.target_port,
        args.client_drop, args.server_drop, args.client_delay, args.server_delay,
        args.client_delay_time, args.server_delay_time
    )

import socket
import random
import time

import socket
import random
import time


def udp_proxy(listen_ip, listen_port, server_ip, server_port, drop_chance=0.1, delay_chance=0.1, delay_time=0.2):
    """
    A proxy server that forwards UDP packets with simulated unreliability.

    Parameters:
    - listen_ip: IP address for the proxy to listen on.
    - listen_port: Port for the proxy to listen on.
    - server_ip: IP address of the target server.
    - server_port: Port of the target server.
    - drop_chance: Probability (0.0 to 1.0) of dropping a packet.
    - delay_chance: Probability (0.0 to 1.0) of delaying a packet.
    - delay_time: Fixed delay time in seconds for delayed packets.
    """
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    proxy_socket.bind((listen_ip, listen_port))
    print(f"Proxy server listening on {listen_ip}:{listen_port}")

    # Dictionary to map client addresses to server
    client_to_server = {}
    client_last_packet = {}  # Tracks the last packet from each client to manage retries

    while True:
        try:
            # Receive data from either the client or server
            data, addr = proxy_socket.recvfrom(65507)

            # If the packet is from a client
            if addr not in client_to_server and addr != (server_ip, server_port):
                client_to_server[addr] = (server_ip, server_port)
                client_last_packet[addr] = data
                print(f"Forwarding new packet from client {addr} to server {server_ip}:{server_port}")

            # If it's a retry or duplicate from the client
            elif addr in client_to_server:
                if data == client_last_packet[addr]:
                    print(f"Retry detected from client {addr}. Forwarding again to server {server_ip}:{server_port}")
                else:
                    client_last_packet[addr] = data
                    print(f"Forwarding updated packet from client {addr} to server {server_ip}:{server_port}")

            # If the packet is from the server
            elif addr == (server_ip, server_port):
                destination = next(client for client, server in client_to_server.items() if server == addr)
                print(f"Forwarding packet from server {addr} to client {destination}")
                proxy_socket.sendto(data, destination)
                continue  # Skip further handling for server packets

            else:
                print(f"Unexpected packet from {addr}. Ignoring.")
                continue

            # Simulate packet loss
            if random.random() < drop_chance:
                print(f"Dropping packet from {addr}")
                continue

            # Simulate packet delay
            if random.random() < delay_chance:
                print(
                    f"Delaying packet from {addr} to {client_to_server.get(addr, (server_ip, server_port))} for {delay_time} seconds")
                time.sleep(delay_time)

            # Forward the packet
            destination = client_to_server.get(addr, (server_ip, server_port))
            proxy_socket.sendto(data, destination)

        except Exception as e:
            print(f"Proxy server error: {e}")


if __name__ == "__main__":
    # Proxy listens on port 4000 and forwards to the server at 127.0.0.1:5000
    # Drop chance: 10%, Delay chance: 10%, Delay time: 0.2 seconds
    udp_proxy("127.0.0.1", 4000, "127.0.0.1", 5000, drop_chance=0.1, delay_chance=0.1, delay_time=0.2)

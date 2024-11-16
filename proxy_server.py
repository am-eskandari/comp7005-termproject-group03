import socket


def udp_proxy(listen_ip, listen_port, server_ip, server_port):
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    proxy_socket.bind((listen_ip, listen_port))
    print(f"Proxy server listening on {listen_ip}:{listen_port}")

    # Dictionary to map client addresses to their server counterparts
    client_to_server = {}

    while True:
        try:
            # Receive data from either the client or server
            data, addr = proxy_socket.recvfrom(65507)

            # If the packet is from a client
            if addr not in client_to_server and addr != (server_ip, server_port):
                client_to_server[addr] = (server_ip, server_port)
                print(f"Forwarding packet from client {addr} to server {server_ip}:{server_port}")
                proxy_socket.sendto(data, (server_ip, server_port))

            # If the packet is from the server
            elif addr == (server_ip, server_port):
                for client_addr in client_to_server.keys():
                    print(f"Forwarding packet from server {addr} to client {client_addr}")
                    proxy_socket.sendto(data, client_addr)

            else:
                # Ignore invalid packets
                print(f"Ignoring unexpected packet from {addr}: {data.decode()}")

        except Exception as e:
            print(f"Proxy server error: {e}")


if __name__ == "__main__":
    # Proxy listens on port 4000 for client messages and forwards them to the server at port 5000
    udp_proxy("127.0.0.1", 4000, "127.0.0.1", 5000)

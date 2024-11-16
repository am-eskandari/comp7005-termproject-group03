import socket


def udp_server(listen_ip, listen_port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the specified IP and port
    server_socket.bind((listen_ip, listen_port))
    print(f"Server listening on {listen_ip}:{listen_port}")

    # Run the server to receive packets
    while True:
        try:
            # Increase buffer size to handle larger UDP packets (up to 65507 bytes)
            data, addr = server_socket.recvfrom(65507)
            if not data:  # Check if the received data is empty
                print(f"Received an empty message from {addr}")
            else:
                print(f"Received message: {data.decode()} from {addr}")
        except Exception as e:
            # Handle decoding errors or other unexpected exceptions
            print(f"Error while receiving message: {e}")


if __name__ == "__main__":
    udp_server("127.0.0.1", 5000)

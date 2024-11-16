import socket

def udp_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        message = input("Enter message to send: ")
        client_socket.sendto(message.encode(), (server_ip, server_port))

if __name__ == "__main__":
    udp_client("127.0.0.1", 5000)

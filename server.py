import socket

def udp_server(listen_ip, listen_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((listen_ip, listen_port))
    print(f"Server listening on {listen_ip}:{listen_port}")
    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f"Received message: {data.decode()} from {addr}")

if __name__ == "__main__":
    udp_server("127.0.0.1", 5000)

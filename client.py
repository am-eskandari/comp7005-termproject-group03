import socket
import time
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="UDP Client")
    parser.add_argument('--target-ip', required=True, help="Server IP address")
    parser.add_argument('--target-port', type=int, required=True, help="Server port")
    parser.add_argument('--timeout', type=int, default=2, help="Acknowledgment timeout in seconds")
    return parser.parse_args()


def udp_client(server_ip, server_port, timeout=2):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a timeout for acknowledgment
    client_socket.settimeout(timeout)

    while True:
        message = input("Enter message to send: ")
        for attempt in range(3):  # Retry up to 3 times
            try:
                # Send the message to the server
                client_socket.sendto(message.encode(), (server_ip, server_port))
                print(f"Message sent: {message}")

                # Wait for an acknowledgment
                data, addr = client_socket.recvfrom(1024)
                print(f"Received acknowledgment: {data.decode()} from {addr}")
                break  # Exit the retry loop on successful acknowledgment
            except socket.timeout:
                print(f"Timeout! Retrying... (Attempt {attempt + 1})")
        else:
            # If all attempts fail, notify the user
            print("Failed to receive acknowledgment after 3 attempts.")

if __name__ == "__main__":
    args = parse_arguments()
    udp_client(args.target_ip, args.target_port, args.timeout)

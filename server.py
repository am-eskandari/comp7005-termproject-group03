import socket
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="UDP Server with Sequence Numbers")
    parser.add_argument('--listen-ip', required=True, help="IP address to bind")
    parser.add_argument('--listen-port', type=int, required=True, help="Port to listen on")
    return parser.parse_args()


def udp_server(listen_ip, listen_port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the specified IP and port
    server_socket.bind((listen_ip, listen_port))
    print(f"🚀 Server started and listening on {listen_ip}:{listen_port}")

    expected_sequence_number = 1  # Tracks the next expected sequence number

    print("\n📝 Waiting for messages...\n")

    # Run the server to receive packets
    while True:
        try:
            # Receive data from the client
            data, addr = server_socket.recvfrom(65507)
            if not data:
                print(f"⚠️ Received an empty message from {addr}")
            else:
                # Decode the data and extract the sequence number and message
                decoded_data = data.decode()
                sequence_number, message = decoded_data.split(":", 1)
                sequence_number = int(sequence_number)

                # Check if the received sequence number matches the expected one
                if sequence_number == expected_sequence_number:
                    print(f"✅ [SEQ {sequence_number}] Received: '{message}' from {addr}")
                    expected_sequence_number += 1  # Increment the expected sequence number
                else:
                    print(
                        f"🔄 [OUT-OF-ORDER] Expected SEQ {expected_sequence_number}, but got SEQ {sequence_number} from {addr}"
                    )

                # Send acknowledgment back with the sequence number
                ack_message = f"ACK:{sequence_number}"
                server_socket.sendto(ack_message.encode(), addr)
                print(f"📤 Sent acknowledgment: {ack_message}\n")

        except Exception as e:
            # Handle unexpected exceptions
            print(f"❌ Error while processing message: {e}")


if __name__ == "__main__":
    args = parse_arguments()
    udp_server(args.listen_ip, args.listen_port)

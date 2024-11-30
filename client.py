import socket
import time
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="UDP Client with Sequence Numbers")
    parser.add_argument('--target-ip', required=True, help="Server IP address")
    parser.add_argument('--target-port', type=int, required=True, help="Server port")
    parser.add_argument('--timeout', type=int, default=2, help="Acknowledgment timeout in seconds")
    return parser.parse_args()


def udp_client(server_ip, server_port, timeout=2):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a timeout for acknowledgment
    client_socket.settimeout(timeout)

    sequence_number = 1  # Tracks the sequence number for each message

    print(f"🚀 Client started. Sending messages to {server_ip}:{server_port}\n")

    while True:
        try:
            # Get the message input from the user
            message = input("📤 Enter message to send (or type 'exit' to quit): ")
            if message.lower() == "exit":
                print("👋 Exiting client. Goodbye!")
                break

            # Prepare the message with the sequence number
            message_with_seq = f"{sequence_number}:{message}"

            for attempt in range(3):  # Retry up to 3 times
                try:
                    # Send the message to the server
                    client_socket.sendto(message_with_seq.encode(), (server_ip, server_port))
                    print(f"✅ [SEQ {sequence_number}] Sent: '{message}'")

                    # Wait for an acknowledgment
                    data, addr = client_socket.recvfrom(1024)
                    ack = data.decode()

                    # Check if the acknowledgment corresponds to the sent sequence number
                    if ack == f"ACK:{sequence_number}":
                        print(f"📥 [ACK {sequence_number}] Received from {addr}\n")
                        sequence_number += 1  # Increment the sequence number for the next message
                        break  # Exit the retry loop on successful acknowledgment
                    else:
                        print(f"⚠️ Unexpected ACK: {ack} (Expected: ACK:{sequence_number})")

                except socket.timeout:
                    print(f"⏳ Timeout! Retrying... (Attempt {attempt + 1})")
            else:
                # If all attempts fail, notify the user
                print(f"❌ Failed to receive acknowledgment for SEQ {sequence_number} after 3 attempts.\n")

        except KeyboardInterrupt:
            print("\n👋 Exiting client. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    args = parse_arguments()
    udp_client(args.target_ip, args.target_port, args.timeout)

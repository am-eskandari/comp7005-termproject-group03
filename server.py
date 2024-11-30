import socket
import argparse
import csv
from datetime import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(description="UDP Server with Latency Tracking")
    parser.add_argument('--listen-ip', required=True, help="IP address to bind")
    parser.add_argument('--listen-port', type=int, required=True, help="Port to listen on")
    return parser.parse_args()


def udp_server(listen_ip, listen_port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the specified IP and port
    server_socket.bind((listen_ip, listen_port))
    print(f"🚀 Server started and listening on {listen_ip}:{listen_port}")

    # Initialize sequence tracking and logging
    expected_sequence_number = 1  # Tracks the next expected sequence number
    csv_file_path = "log_server.csv"

    # Open the CSV file for logging
    with open(csv_file_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the CSV header
        csv_writer.writerow(["Timestamp", "Event", "Sequence", "Acknowledgment",
                             "Source IP", "Source Port", "Destination IP", "Destination Port",
                             "Message", "Latency (ms)"])

        print("\n📝 Waiting for messages...\n")

        while True:
            try:
                # Receive data from the client
                start_time = datetime.now()
                data, addr = server_socket.recvfrom(65507)
                receive_time = datetime.now()
                latency_ms = (receive_time - start_time).total_seconds() * 1000

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
                        event = "Received"
                        expected_sequence_number += 1  # Increment the expected sequence number
                    else:
                        print(
                            f"🔄 [OUT-OF-ORDER] Expected SEQ {expected_sequence_number}, "
                            f"but got SEQ {sequence_number} from {addr}"
                        )
                        event = "Out-of-Order"

                    # Send acknowledgment back with the sequence number
                    ack_message = f"ACK:{sequence_number}"
                    server_socket.sendto(ack_message.encode(), addr)
                    print(f"📤 Sent acknowledgment: {ack_message} (Latency: {latency_ms:.2f} ms)\n")

                    # Log the event to the CSV
                    csv_writer.writerow([receive_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                                         event, sequence_number, sequence_number,
                                         addr[0], addr[1], listen_ip, listen_port,
                                         message, f"{latency_ms:.2f}"])

            except KeyboardInterrupt:
                print("\n👋 Server shutting down. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error while processing message: {e}")


if __name__ == "__main__":
    args = parse_arguments()
    udp_server(args.listen_ip, args.listen_port)

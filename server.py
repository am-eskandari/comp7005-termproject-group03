import argparse
import socket
from datetime import datetime

from utils.logger import server_logger, log_event
from utils.validation import validate_ip, validate_port


def parse_arguments():
    parser = argparse.ArgumentParser(description="UDP Server with Latency Tracking")
    parser.add_argument('--listen-ip', required=True, help="IP address to bind")
    parser.add_argument('--listen-port', required=True, help="Port to listen on")
    arguments = parser.parse_args()

    # Validate and process IP
    arguments.listen_ip = validate_ip(arguments.listen_ip)

    # Validate and process port
    arguments.listen_port = validate_port(arguments.listen_port)

    return arguments


def udp_server(listen_ip, listen_port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the specified IP and port
    server_socket.bind((listen_ip, listen_port))
    print(f"🚀 Server started and listening on {listen_ip}:{listen_port}")

    # Initialize sequence tracking
    expected_sequence_number = 1  # Tracks the next expected sequence number

    print("\n🗑 Waiting for messages...\n")

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
                # Decode the data
                decoded_data = data.decode()

                # Check if the message is a termination signal
                if decoded_data == "TERMINATE":
                    print(f"👋 Client {addr} has terminated the session. Resetting sequence.")
                    expected_sequence_number = 1  # Reset sequence number for new clients
                    log_event(server_logger, "Terminate", expected_sequence_number, None, addr[0], addr[1], listen_ip,
                              listen_port, None, latency_ms)
                    continue

                # Extract the sequence number and message
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

                # Log the received event
                log_event(server_logger, event, sequence_number, None, addr[0], addr[1], listen_ip, listen_port,
                          message, latency_ms)

                # Send acknowledgment back with the sequence number
                ack_message = f"ACK:{sequence_number}"
                server_socket.sendto(ack_message.encode(), addr)
                print(f"📤 Sent acknowledgment: {ack_message} (Latency: {latency_ms:.2f} ms)\n")

                # Log the acknowledgment event
                log_event(server_logger, "Acknowledged", sequence_number, sequence_number, listen_ip, listen_port,
                          addr[0], addr[1], None, latency_ms)

        except KeyboardInterrupt:
            print("\n👋 Server shutting down. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error while processing message: {e}")


if __name__ == "__main__":
    parsed_args = parse_arguments()
    udp_server(parsed_args.listen_ip, parsed_args.listen_port)

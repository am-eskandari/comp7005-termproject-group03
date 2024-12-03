import argparse
import socket
from datetime import datetime

from utils.logger import client_logger, log_event
from utils.validation import validate_ip, validate_port


def parse_arguments():
    parser = argparse.ArgumentParser(description="UDP Client with Latency Tracking")
    parser.add_argument('--target-ip', required=True, help="Server IP address")
    parser.add_argument('--target-port', required=True, help="Server port")
    parser.add_argument('--timeout', required=True, help="Acknowledgment timeout in milliseconds")
    args = parser.parse_args()

    # Validate and process IP
    args.target_ip = validate_ip(args.target_ip)

    # Validate and process port
    args.target_port = validate_port(args.target_port)

    # Validate and process timeout
    try:
        timeout_ms = int(args.timeout)
        if timeout_ms <= 0:
            raise ValueError("Timeout must be a positive integer.")
    except ValueError as e:
        print(f"❌ Invalid timeout value: {args.timeout}. {e}")
        print("Timeout must be a positive integer in milliseconds.")
        exit(1)

    # Convert timeout to seconds for socket operations
    args.timeout = timeout_ms / 1000.0
    return args


def udp_client(server_ip, server_port, timeout=2):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a timeout for acknowledgment
    client_socket.settimeout(timeout)

    sequence_number = 1  # Tracks the sequence number for each message
    auto_send_count = 9  # Number of additional messages to auto-send

    # Dictionary to store the send timestamp for each sequence
    send_timestamps = {}

    print(f"🚀 Client started. Sending messages to {server_ip}:{server_port}\n")

    source_ip = None
    source_port = None

    try:
        while True:
            # Get the first message input from the user
            message = input("📤 Enter message to send (or type 'exit' to quit): ")
            if message.lower() == "exit":
                # Send a termination message to the server
                terminate_message = "TERMINATE"
                client_socket.sendto(terminate_message.encode(), (server_ip, server_port))
                print("👋 Sent termination message to server. Exiting client.")
                break

            # Prepare the message with the sequence number
            message_with_seq = f"{sequence_number}:{message}"

            # Store the send timestamp for the sequence number
            send_timestamps[sequence_number] = datetime.now()

            for attempt in range(5):  # Retry up to 5 times
                try:
                    # Send the first message
                    client_socket.sendto(message_with_seq.encode(), (server_ip, server_port))

                    # Capture the source IP and port after sending
                    source_ip, source_port = client_socket.getsockname()

                    print(f"✅ [SEQ {sequence_number}] Sent: '{message}' "
                          f"(From {source_ip}:{source_port} to {server_ip}:{server_port})")

                    # Log the sent event
                    log_event(client_logger, "Sent", sequence_number, None,
                              source_ip, source_port, server_ip, server_port, message, None)

                    # Wait for an acknowledgment
                    data, addr = client_socket.recvfrom(1024)
                    ack_message = data.decode()  # Decode the received message

                    # Parse acknowledgment (expecting "ACK:<sequence>")
                    if ack_message.startswith("ACK:"):
                        ack = int(ack_message.split(":")[1])
                    else:
                        raise ValueError(f"Unexpected acknowledgment format: {ack_message}")

                    # Check if the acknowledgment corresponds to the sent sequence number
                    if ack == sequence_number:
                        # Use the original send timestamp to calculate latency
                        if ack in send_timestamps:
                            latency_ms = (datetime.now() - send_timestamps[ack]).total_seconds() * 1000
                            print(f"📥 [ACK {ack}] Received from {addr} (Latency: {latency_ms:.2f} ms)\n")
                            log_event(client_logger, "Acknowledged", sequence_number, ack,
                                      addr[0], addr[1], server_ip, server_port, None, latency_ms)
                            # Clean up the timestamp for the acknowledged sequence number
                            del send_timestamps[ack]
                        else:
                            print(f"⚠️ No timestamp found for ACK {ack}.")

                        sequence_number += 1  # Increment the sequence number for the next message
                        break  # Exit the retry loop on successful acknowledgment
                    else:
                        print(f"⚠️ Unexpected ACK: {ack} (Expected: {sequence_number})")
                        log_event(client_logger, "Unexpected ACK", sequence_number, ack,
                                  addr[0], addr[1], server_ip, server_port, None, None)

                except socket.timeout:
                    # Log the retransmit event
                    if source_ip is not None and source_port is not None:
                        log_event(client_logger, "Retransmit", sequence_number, None,
                                  source_ip, source_port, server_ip, server_port, message, None)
                    print(f"⏳ Timeout! Retrying... (Attempt {attempt + 1})")
            else:
                # If all attempts fail, notify the user and log the failure
                if source_ip is not None and source_port is not None:
                    log_event(client_logger, "Failed", sequence_number, None,
                              source_ip, source_port, server_ip, server_port, message, None)
                print(f"❌ Failed to receive acknowledgment for SEQ {sequence_number} after 5 attempts.\n")

            # Automatically send additional messages
            for i in range(auto_send_count):
                auto_message = f"hello there {i + 2}"
                message_with_seq = f"{sequence_number}:{auto_message}"
                send_timestamps[sequence_number] = datetime.now()  # Track timestamp for auto-send messages
                for attempt in range(5):
                    try:
                        client_socket.sendto(message_with_seq.encode(), (server_ip, server_port))
                        print(f"✅ [SEQ {sequence_number}] Sent: '{auto_message}'")

                        # Wait for acknowledgment
                        data, addr = client_socket.recvfrom(1024)
                        ack_message = data.decode()
                        if ack_message.startswith("ACK:"):
                            ack = int(ack_message.split(":")[1])
                            if ack == sequence_number:
                                latency_ms = (datetime.now() - send_timestamps[ack]).total_seconds() * 1000
                                print(f"📥 [ACK {ack}] Received for '{auto_message}' (Latency: {latency_ms:.2f} ms)\n")
                                del send_timestamps[ack]  # Clean up timestamp
                                sequence_number += 1
                                break
                    except socket.timeout:
                        print(f"⏳ Timeout for '{auto_message}'! Retrying... (Attempt {attempt + 1})")
                else:
                    print(f"❌ Failed to send '{auto_message}' after 5 attempts.")

    except KeyboardInterrupt:
        print("\n👋 Exiting client. Sending termination message to server...")
        terminate_message = "TERMINATE"
        try:
            client_socket.sendto(terminate_message.encode(), (server_ip, server_port))
            print("🚨 Termination message sent successfully.")
        except Exception as e:
            print(f"❌ Failed to send termination message: {e}")
        finally:
            print("👋 Goodbye!")


if __name__ == "__main__":
    parsed_args = parse_arguments()
    udp_client(parsed_args.target_ip, parsed_args.target_port, parsed_args.timeout)

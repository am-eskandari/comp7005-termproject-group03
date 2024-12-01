import argparse
import csv
import re
import socket
from datetime import datetime


def validate_ip(ip):
    """Validate IPv4 address format with graceful error handling."""
    try:
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if not pattern.match(ip):
            raise ValueError
        parts = ip.split(".")
        if any(int(part) < 0 or int(part) > 255 for part in parts):
            raise ValueError
    except ValueError:
        print(f"❌ Invalid IP address format: {ip}")
        print("IP address must be in the format 'X.X.X.X' with each octet between 0 and 255.")
        exit(1)
    return ip


def validate_port(port):
    """Validate port number with graceful error handling."""
    try:
        port = int(port)
        if not (1 <= port <= 65535):
            raise ValueError
    except ValueError:
        print(f"❌ Invalid port number: {port}. Must be an integer between 1 and 65535.")
        exit(1)
    return port


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

    # Open a CSV file for logging
    with open("log_client.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write CSV header
        csv_writer.writerow(["Timestamp", "Event", "Sequence", "Acknowledgment",
                             "Source IP", "Source Port", "Destination IP", "Destination Port",
                             "Message", "Latency (ms)"])

        print(f"🚀 Client started. Sending messages to {server_ip}:{server_port}\n")

        try:
            while True:
                # Get the message input from the user
                message = input("📤 Enter message to send (or type 'exit' to quit): ")
                if message.lower() == "exit":
                    # Send a termination message to the server
                    terminate_message = "TERMINATE"
                    client_socket.sendto(terminate_message.encode(), (server_ip, server_port))
                    print("👋 Sent termination message to server. Exiting client.")
                    break

                # Prepare the message with the sequence number
                message_with_seq = f"{sequence_number}:{message}"
                send_time = None  # To track when the message is sent

                for attempt in range(10):  # Retry up to 10 times
                    try:
                        # Send the message to the server
                        send_time = datetime.now()
                        client_socket.sendto(message_with_seq.encode(), (server_ip, server_port))

                        # Capture the source IP and port after sending
                        source_ip, source_port = client_socket.getsockname()

                        print(f"✅ [SEQ {sequence_number}] Sent: '{message}' "
                              f"(From {source_ip}:{source_port} to {server_ip}:{server_port})")

                        # Log the sent event
                        timestamp = send_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                        csv_writer.writerow([timestamp, "Sent", sequence_number, None,
                                             source_ip, source_port, server_ip, server_port, message, None])

                        # Wait for an acknowledgment
                        data, addr = client_socket.recvfrom(1024)
                        ack_message = data.decode()  # Decode the received message

                        # Parse acknowledgment (expecting "ACK:<sequence>")
                        if ack_message.startswith("ACK:"):
                            ack = int(ack_message.split(":")[1])
                        else:
                            raise ValueError(f"Unexpected acknowledgment format: {ack_message}")

                        receive_time = datetime.now()

                        # Check if the acknowledgment corresponds to the sent sequence number
                        if ack == sequence_number:
                            latency_ms = (receive_time - send_time).total_seconds() * 1000
                            print(f"📥 [ACK {ack}] Received from {addr} (Latency: {latency_ms:.2f} ms)\n")
                            timestamp = receive_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                            csv_writer.writerow([timestamp, "Acknowledged", sequence_number, ack,
                                                 addr[0], addr[1], server_ip, server_port, None, f"{latency_ms:.2f}"])
                            sequence_number += 1  # Increment the sequence number for the next message
                            break  # Exit the retry loop on successful acknowledgment
                        else:
                            print(f"⚠️ Unexpected ACK: {ack} (Expected: {sequence_number})")
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                            csv_writer.writerow([timestamp, "Unexpected ACK", sequence_number, ack,
                                                 addr[0], addr[1], server_ip, server_port, None, None])

                    except socket.timeout:
                        # Log the retransmit event
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        csv_writer.writerow([timestamp, "Retransmit", sequence_number, None,
                                             source_ip, source_port, server_ip, server_port, message, None])
                        print(f"⏳ Timeout! Retrying... (Attempt {attempt + 1})")
                else:
                    # If all attempts fail, notify the user and log the failure
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    csv_writer.writerow([timestamp, "Failed", sequence_number, None,
                                         source_ip, source_port, server_ip, server_port, message, None])
                    print(f"❌ Failed to receive acknowledgment for SEQ {sequence_number} after 10 attempts.\n")

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
    args = parse_arguments()
    udp_client(args.target_ip, args.target_port, args.timeout)

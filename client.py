import socket
from datetime import datetime

from utils.parsing import parse_client


def udp_client(server_ip, server_port, timeout=2):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a timeout for acknowledgment
    client_socket.settimeout(timeout)

    sequence_number = 1  # Tracks the sequence number for each message
    auto_send_count = 4  # Number of additional messages to auto-send

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

            while True:
                # Prepare the message with the sequence number
                message_with_seq = f"{sequence_number}:{message}"

                # Store the send timestamp for the sequence number
                send_timestamps[sequence_number] = datetime.now()

                for attempt in range(5):  # Retry up to 5 times
                    try:
                        # Send the message
                        client_socket.sendto(message_with_seq.encode(), (server_ip, server_port))

                        # Capture the source IP and port after sending
                        source_ip, source_port = client_socket.getsockname()

                        print(f"✅ [SEQ {sequence_number}] Sent: '{message}' "
                              f"(From {source_ip}:{source_port} to {server_ip}:{server_port})")

                        # Wait for an acknowledgment
                        data, addr = client_socket.recvfrom(1024)
                        ack_message = data.decode()  # Decode the received message

                        # Parse acknowledgment (expecting "ACK:<sequence>")
                        if ack_message.startswith("ACK:"):
                            ack = int(ack_message.split(":")[1])
                            if ack == sequence_number:
                                latency_ms = (datetime.now() - send_timestamps[sequence_number]).total_seconds() * 1000
                                print(f"📥 [ACK {ack}] Received from {addr} (Latency: {latency_ms:.2f} ms)\n")

                                # Clean up the timestamp for the acknowledged sequence number
                                del send_timestamps[sequence_number]
                                sequence_number += 1  # Increment for the next message
                                break  # Exit the retry loop on successful acknowledgment
                            else:
                                print(f"⚠️ Unexpected ACK: {ack} (Expected: {sequence_number})")

                    except socket.timeout:
                        print(f"⏳ Timeout! Retrying SEQ {sequence_number}... (Attempt {attempt + 1})")

                else:
                    # If all attempts fail, log and move to the next message
                    print(f"❌ Failed to receive acknowledgment for SEQ {sequence_number} after 5 attempts.\n")
                    break  # Exit the loop for this message

                # Exit after retries if acknowledgment is not received
                break

            # Automatically send additional messages
            for i in range(auto_send_count):
                auto_message = f"hi {i + 2}"
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
    parsed_args = parse_client()
    udp_client(parsed_args.target_ip, parsed_args.target_port, parsed_args.timeout)

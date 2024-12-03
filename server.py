import socket
from datetime import datetime

from utils.logger import server_logger, log_event
from utils.parsing import parse_server

# Cache for deduplication and acknowledgment
dedup_cache = set()
acknowledgment_cache = {}  # Maps sequence numbers to acknowledgment messages
CACHE_TIMEOUT = 10  # Time in seconds to keep sequence numbers in cache


def cleanup_cache():
    """Clean up expired entries in the acknowledgment cache."""
    now = datetime.now()
    expired_keys = [seq for seq, (ack, timestamp) in acknowledgment_cache.items() if
                    (now - timestamp).total_seconds() > CACHE_TIMEOUT]
    for key in expired_keys:
        del acknowledgment_cache[key]


def udp_server(listen_ip, listen_port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((listen_ip, listen_port))
    print(f"🚀 Server started and listening on {listen_ip}:{listen_port}")

    # Sequence tracking
    expected_sequence_number = 1
    last_acknowledged_sequence = 0  # Tracks the highest sequence acknowledged
    processed_sequences = set()  # Tracks processed sequence numbers
    acknowledgment_cache = {}  # Cache for sent acknowledgments
    packet_buffer = {}  # Buffer for out-of-order packets

    print("\n🗑 Waiting for messages...\n")

    while True:
        try:
            cleanup_cache()

            # Receive data from the client
            data, addr = server_socket.recvfrom(65507)
            receive_time = datetime.now()

            if not data:
                print(f"⚠️ Received an empty message from {addr}")
                continue

            decoded_data = data.decode()

            # Handle termination signal
            if decoded_data == "TERMINATE":
                print(f"👋 Client {addr} has terminated the session. Resetting sequence.")
                expected_sequence_number = 1
                last_acknowledged_sequence = 0
                processed_sequences.clear()
                acknowledgment_cache.clear()
                packet_buffer.clear()
                log_event(server_logger, "Terminate", expected_sequence_number, None, addr[0], addr[1], listen_ip,
                          listen_port, None, None)
                continue

            # Handle RESEND_ACK
            if decoded_data.startswith("RESEND_ACK:"):
                sequence_number = int(decoded_data.split(":")[1])
                if sequence_number in acknowledgment_cache:
                    ack_message, _ = acknowledgment_cache[sequence_number]
                    server_socket.sendto(ack_message.encode(), addr)
                    print(f"📤 Resent acknowledgment: {ack_message} for SEQ {sequence_number}")
                else:
                    print(f"⚠️ RESEND_ACK requested for SEQ {sequence_number}, but no such acknowledgment exists.")
                continue

            # Parse the sequence number and message
            try:
                sequence_number, message = decoded_data.split(":", 1)
                sequence_number = int(sequence_number)
            except ValueError:
                print(f"⚠️ Malformed packet received from {addr}: {decoded_data}")
                continue

            # Handle duplicate packets
            if sequence_number <= last_acknowledged_sequence:
                print(f"🔄 Duplicate or retransmitted packet [SEQ {sequence_number}] from {addr}. Ignored.")
                # Resend the acknowledgment for duplicates
                if sequence_number in acknowledgment_cache:
                    ack_message, _ = acknowledgment_cache[sequence_number]
                    server_socket.sendto(ack_message.encode(), addr)
                    print(f"📤 Resent acknowledgment for duplicate SEQ {sequence_number}")
                continue

            # Handle out-of-order packets
            if sequence_number > expected_sequence_number:
                print(f"🔄 [OUT-OF-ORDER] Buffering SEQ {sequence_number}. Expected: {expected_sequence_number}")
                packet_buffer[sequence_number] = (message, addr, receive_time)
                continue

            # Process the current packet
            print(f"✅ [SEQ {sequence_number}] Received: '{message}' from {addr}")
            log_event(server_logger, "Received", sequence_number, None, addr[0], addr[1], listen_ip, listen_port,
                      message, None)

            # Send acknowledgment for the current sequence
            ack_message = f"ACK:{sequence_number}"
            acknowledgment_cache[sequence_number] = (ack_message, datetime.now())
            server_socket.sendto(ack_message.encode(), addr)
            print(f"📤 Sent acknowledgment: {ack_message}")

            last_acknowledged_sequence = sequence_number
            expected_sequence_number += 1

            # Process buffered packets in order
            while expected_sequence_number in packet_buffer:
                buffered_message, buffered_addr, buffered_time = packet_buffer.pop(expected_sequence_number)
                print(f"✅ [SEQ {expected_sequence_number}] Processed from buffer: '{buffered_message}'")
                ack_message = f"ACK:{expected_sequence_number}"
                acknowledgment_cache[expected_sequence_number] = (ack_message, datetime.now())
                server_socket.sendto(ack_message.encode(), buffered_addr)
                print(f"📤 Sent acknowledgment: {ack_message} for buffered SEQ {expected_sequence_number}")
                log_event(server_logger, "Received (Buffered)", expected_sequence_number, None, buffered_addr[0],
                          buffered_addr[1], listen_ip, listen_port, buffered_message, None)
                last_acknowledged_sequence = expected_sequence_number
                expected_sequence_number += 1

        except KeyboardInterrupt:
            print("\n👋 Server shutting down. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error while processing message: {e}")


if __name__ == "__main__":
    parsed_args = parse_server()
    udp_server(parsed_args.listen_ip, parsed_args.listen_port)

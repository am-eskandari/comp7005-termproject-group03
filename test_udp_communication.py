import socket
import threading
import pytest
import time

# Define the server function to run in a separate thread
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", 5000))
    while True:
        try:
            # Increased buffer size to handle large UDP packets
            data, addr = server_socket.recvfrom(65507)
            if data.decode() == "TERMINATE":
                print("Shutting down server.", flush=True)
                break
            print(f"Server received: {data.decode()} from {addr}", flush=True)
            server_socket.sendto(b"ACK", addr)
        except Exception as e:
            print(f"Error in server: {e}", flush=True)
            break
    server_socket.close()

# Start the server in a separate thread
@pytest.fixture(scope="module", autouse=True)
def start_server():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Allow server to start
    yield
    udp_client_send("TERMINATE")  # Gracefully shut down the server
    server_thread.join(timeout=10)  # Ensure server thread stops

# Client helper function
def udp_client_send(message, server_ip="127.0.0.1", server_port=5000):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(message.encode(), (server_ip, server_port))
    client_socket.close()

# Test cases

def test_simple_message(capfd):
    """Test if the server receives a single message."""
    udp_client_send("Hello, Server!")
    time.sleep(0.5)  # Allow time for server to process
    captured = capfd.readouterr()
    assert "Server received: Hello, Server!" in captured.out

def test_multiple_messages(capfd):
    """Test if the server receives multiple sequential messages."""
    messages = ["Message 1", "Message 2", "Message 3"]
    for msg in messages:
        udp_client_send(msg)
        time.sleep(0.2)  # Small delay between messages
    captured = capfd.readouterr()
    for msg in messages:
        assert f"Server received: {msg}" in captured.out

def test_empty_message(capfd):
    """Test if the server can handle an empty message."""
    udp_client_send("")
    time.sleep(0.5)  # Allow time for server to process
    captured = capfd.readouterr()
    assert "Server received: " in captured.out

def test_large_message(capfd):
    """Test if the server can handle a large message."""
    large_message = "A" * 1400  # Adjust message size to avoid fragmentation issues
    udp_client_send(large_message)
    time.sleep(0.5)  # Allow time for server to process
    captured = capfd.readouterr()
    assert f"Server received: {large_message}" in captured.out

def test_acknowledgment_handling(capfd):
    """Test if the server sends an acknowledgment and the client receives it."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(2)

    # Send a message and wait for an acknowledgment
    client_socket.sendto("Test Message".encode(), ("127.0.0.1", 5000))
    try:
        data, addr = client_socket.recvfrom(1024)
        assert data.decode() == "ACK"
    except socket.timeout:
        pytest.fail("Acknowledgment not received within the timeout period.")
    finally:
        client_socket.close()

def test_client_retry(capfd):
    """Test if the client retries sending a message when no acknowledgment is received."""
    # Simulate no server response by not starting a server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)

    message = "Retry Test"
    retry_attempts = 3

    for attempt in range(retry_attempts):
        try:
            client_socket.sendto(message.encode(), ("127.0.0.1", 5000))
            client_socket.recvfrom(1024)  # Wait for acknowledgment (will timeout)
        except socket.timeout:
            pass  # Expected behavior
    captured = capfd.readouterr()
    assert captured.out.count("Timeout! Retrying...") == retry_attempts
    client_socket.close()

def test_successful_acknowledgment_after_retry(capfd):
    """Test if the client processes an acknowledgment after retrying."""

    # Define a temporary server with delayed acknowledgment
    def delayed_ack_server():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(("127.0.0.1", 5000))
        data, addr = server_socket.recvfrom(65507)
        time.sleep(2.5)  # Deliberate delay to exceed client timeout
        server_socket.sendto(b"ACK", addr)
        server_socket.close()

    server_thread = threading.Thread(target=delayed_ack_server, daemon=True)
    server_thread.start()

    # Client sends message and retries
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(2)

    try:
        client_socket.sendto("Delayed ACK Test".encode(), ("127.0.0.1", 5000))
        data, addr = client_socket.recvfrom(1024)  # This will receive the delayed ACK
        assert data.decode() == "ACK"
    except socket.timeout:
        pytest.fail("Client failed to process delayed acknowledgment.")
    finally:
        client_socket.close()

def test_multiple_acknowledgments(capfd):
    """Test if the server sends acknowledgments for multiple sequential messages."""
    messages = ["Msg 1", "Msg 2", "Msg 3"]
    for msg in messages:
        udp_client_send(msg)
        time.sleep(0.2)
    captured = capfd.readouterr()
    assert captured.out.count("ACK") == len(messages)

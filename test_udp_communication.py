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
            print(f"Server received: {data.decode()} from {addr}")
        except Exception as e:
            print(f"Error in server: {e}")
            break
    server_socket.close()

# Start the server in a separate thread
@pytest.fixture(scope="module", autouse=True)
def start_server():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Allow server to start
    yield
    server_thread.join()

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

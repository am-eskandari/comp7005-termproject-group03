import itertools
import subprocess
import time

# Define the parameter ranges you want to test
client_drop_values = [0.0, 0.1, 0.2, 0.3]
server_drop_values = [0.0, 0.1, 0.2, 0.3]
client_delay_values = [0.0, 0.1, 0.2, 0.3]
server_delay_values = [0.0, 0.1, 0.2, 0.3]
client_delay_time_values = ["100", "200", "300", "100-500"]
server_delay_time_values = ["200", "300", "400", "200-600"]

# Generate all possible combinations of parameters
parameter_combinations = list(itertools.product(
    client_drop_values, server_drop_values,
    client_delay_values, server_delay_values,
    client_delay_time_values, server_delay_time_values
))


# Function to start the server
def start_server(ip, port):
    return subprocess.Popen(["python3", "server.py", f"--listen-ip={ip}", f"--listen-port={port}"])


# Function to start the proxy server
def start_proxy_server(listen_ip, listen_port, target_ip, target_port, control_port, **params):
    # Extract parameters and pass to the proxy server
    cmd = ["python3", "proxy.py", f"--listen-ip={listen_ip}", f"--listen-port={listen_port}",
           f"--target-ip={target_ip}", f"--target-port={target_port}", f"--control-port={control_port}"]
    for param, value in params.items():
        cmd.append(f"--{param}={value}")
    return subprocess.Popen(cmd)


# Function to start the client
def start_client(proxy_ip, proxy_port, timeout):
    return subprocess.Popen(
        ["python3", "client.py", f"--target-ip={proxy_ip}", f"--target-port={proxy_port}", f"--timeout={timeout}"])


# Function to update proxy server settings dynamically using nc
def update_proxy_parameters(control_ip, control_port, param, value):
    command = f"echo 'SET {param} {value}' | nc -u {control_ip} {control_port}"
    subprocess.run(command, shell=True)


# Function to run the full test cycle
def run_test_cycle(server_ip, proxy_ip, control_ip, server_port, proxy_port, timeout, params):
    # Start the server and proxy server
    server_process = start_server(server_ip, server_port)
    time.sleep(2)  # Wait for the server to start

    proxy_process = start_proxy_server(proxy_ip, proxy_port, server_ip, server_port, control_port, **params)
    time.sleep(2)  # Wait for the proxy server to start

    # Dynamically set parameters for the proxy server
    for param, value in params.items():
        update_proxy_parameters(control_ip, control_port, param, value)
        time.sleep(1)  # Wait a moment after setting each parameter

    # Start the client
    client_process = start_client(proxy_ip, proxy_port, timeout)
    client_process.wait()

    # Wait for the proxy and server to finish
    proxy_process.wait()
    server_process.wait()


# Main function to iterate through all combinations and run tests
def main():
    # All components running on the same machine (use localhost)
    server_ip = "127.0.0.1"  # Server machine IP (localhost)
    proxy_ip = "127.0.0.1"  # Proxy machine IP (localhost)
    control_ip = "127.0.0.1"  # Control machine IP (localhost)
    server_port = 5000
    proxy_port = 4000
    timeout = 1
    control_port = 4500

    # Loop over all parameter combinations
    for params in parameter_combinations:
        test_params = {
            "client-drop": params[0],
            "server-drop": params[1],
            "client-delay": params[2],
            "server-delay": params[3],
            "client-delay-time": params[4],
            "server-delay-time": params[5]
        }
        print(f"Running test with parameters: {test_params}")
        run_test_cycle(server_ip, proxy_ip, control_ip, server_port, proxy_port, timeout, test_params)


if __name__ == "__main__":
    main()

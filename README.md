# Reliable Communication Protocol Using UDP

This project implements a **reliable communication protocol** using UDP to address challenges like packet loss and
delays. The system includes the following components:

- **Client**: Sends messages to the server via the proxy.
- **Server**: Receives and acknowledges messages from the client.
- **Proxy Server**: Simulates unreliable network conditions with configurable parameters and supports dynamic updates
  via a control socket.

### **Key Features**

- **Dynamic Parameter Adjustment**: Modify drop rates, delay probabilities, and delay times in real-time using the
  control socket.
- **Flexible Delay Configuration**: Supports both fixed and range-based delay times (e.g., `200-600ms`).
- **Real-Time Network Simulation**: Emulates packet loss, delay, and retransmission scenarios to test system
  reliability.
- **Configurable Drop and Delay Settings**: Tailor network conditions to mimic various real-world scenarios.

This project, developed and tested on **Arch Linux**, demonstrates how to improve UDP communication reliability through
acknowledgment and retransmission mechanisms, addressing packet loss and delay challenges.

---

### **Documentation Links**

- [Test Case Configurations](https://github.com/am-eskandari/comp7005-termproject-group03/blob/main/docs/configurations.md):
  Explore combinations of parameters tested for drop and delay scenarios.
- [Test Commands](https://github.com/am-eskandari/comp7005-termproject-group03/blob/main/docs/tests.md): Review
  the
  commands used to execute and validate the test cases.

---

## **0. Setup Instructions**

---

### **Prerequisites**

- Tested on: **Arch Linux**, **Manjaro**, **Ubuntu**
- Python version: **3.12 or higher**
- Required libraries:
    - `socket`
    - `argparse`
    - `threading`

---

### **Installation**

1. Ensure Python is installed:
   ```bash
   sudo pacman -S python
   ```
2. Install `netcat` (for control parameter updates):
   ```bash
   sudo pacman -S openbsd-netcat
   ```

---

### **Device Discovery and Communication Verification**

Before running the system, ensure that all devices (client, server, and proxy) can communicate with each other on the
same network.

---

#### **1. Check Device IPs**

Use the `ip addr` command to find the IP addresses of devices on the same network:

```bash
ip addr
```

- Look for the IP address under the appropriate network interface (e.g., `eth0`, `wlan0`).
- Note the IP addresses for the client, server, and proxy machines.

---

#### **2. Verify Port Availability**

Ensure that the required ports (e.g., `4000`, `4500`, `5000`) are not in use. Use the `netstat` or `ss` command:

```bash
sudo netstat -tuln | grep <PORT>
```

or

```bash
sudo ss -tuln | grep <PORT>
```

If the port is in use, stop the conflicting process or use a different port for your application.

---

#### **3. Test Network Connectivity**

Use the `ping` command to ensure that devices can communicate:

```bash
ping <DEVICE_IP>
```

- Replace `<DEVICE_IP>` with the IP address of another device (e.g., the server or proxy).
- Ensure packets are sent and received successfully. If not, check firewall settings or network configurations.

---

## **1. How to Run**

### **1. Start the Server**

Run the server to listen for incoming messages:

```bash
python server.py --listen-ip <IP> --listen-port <PORT>
```

**Example:**

```bash
python server.py --listen-ip 127.0.0.1 --listen-port 5000
```

### **2. Start the Proxy Server**

The proxy server relays packets between the client and server while simulating network conditions. It also provides a *
*control interface** for dynamic parameter updates.

Run the proxy server:

```bash
python proxy.py --listen-ip <IP> --listen-port <PORT> \
--target-ip <SERVER_IP> --target-port <SERVER_PORT> \
--client-drop <VALUE> --server-drop <VALUE> \
--client-delay <VALUE> --server-delay <VALUE> \
--client-delay-time <MILLISECONDS_OR_RANGE> --server-delay-time <MILLISECONDS_OR_RANGE> \
--control-port <PORT>
```

**Example:**

```bash
python proxy.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0.1 --server-drop 0.2 \
--client-delay 0.3 --server-delay 0.4 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

### **3. Start the Client**

Run the client to send messages to the server via the proxy:

```bash
python client.py --target-ip <PROXY_IP> --target-port <PROXY_PORT> --timeout <SECONDS>
```

**Example:**

```bash
python client.py --target-ip 127.0.0.1 --target-port 4000 --timeout 1
```

---

### **Final Network Check**

1. Ensure all devices are on the same subnet (e.g., `192.168.1.x`).
2. Confirm successful pings between devices.
3. Verify that required ports are not blocked by firewalls.

---

## **2. Changing Parameters Dynamically**

The proxy server supports **dynamic parameter updates** using the control socket (e.g., via **Netcat**).

### **Steps to Change Parameters**

---

1. Send a command to the control socket:
   ```bash
   echo "SET <PARAMETER> <VALUE>" | nc -u <CONTROL_IP> <CONTROL_PORT>
   ```

2. Available parameters:
    - `client-drop`: Drop chance for client-to-server packets (0.0 to 1.0).
    - `server-drop`: Drop chance for server-to-client packets (0.0 to 1.0).
    - `client-delay`: Delay chance for client-to-server packets (0.0 to 1.0).
    - `server-delay`: Delay chance for server-to-client packets (0.0 to 1.0).
    - `client-delay-time`: Delay time for client-to-server packets (milliseconds or range, e.g., `100-500`).
    - `server-delay-time`: Delay time for server-to-client packets (milliseconds or range, e.g., `200-600`).

### **Examples**

- Set client drop chance to 30%:
  ```bash
  echo "SET client-drop 0.3" | nc -u 127.0.0.1 4500
  ```
- Set server delay to 50%:
  ```bash
  echo "SET server-delay 0.5" | nc -u 127.0.0.1 4500
  ```
- Set client delay time to a range (100-500 ms):
  ```bash
  echo "SET client-delay-time 100-500" | nc -u 127.0.0.1 4500
  ```

---

## **3. Command-Line Arguments for Each File**

### **Client**

| Argument        | Description                       | Example                 |
|-----------------|-----------------------------------|-------------------------|
| `--target-ip`   | IP address of the proxy server.   | `--target-ip 127.0.0.1` |
| `--target-port` | Port of the proxy server.         | `--target-port 4000`    |
| `--timeout`     | Timeout for acknowledgment (sec). | `--timeout 1`           |

---

### **Server**

| Argument        | Description                       | Example                 |
|-----------------|-----------------------------------|-------------------------|
| `--listen-ip`   | IP address to bind the server.    | `--listen-ip 127.0.0.1` |
| `--listen-port` | Port for the server to listen on. | `--listen-port 5000`    |

---

### **Proxy Server**

| Argument              | Description                                   | Example                       |
|-----------------------|-----------------------------------------------|-------------------------------|
| `--listen-ip`         | IP address to bind the proxy.                 | `--listen-ip 127.0.0.1`       |
| `--listen-port`       | Port to listen for client packets.            | `--listen-port 4000`          |
| `--target-ip`         | IP address of the server.                     | `--target-ip 127.0.0.1`       |
| `--target-port`       | Port of the server.                           | `--target-port 5000`          |
| `--client-drop`       | Drop chance (0.0 to 1.0) for client packets.  | `--client-drop 0.1`           |
| `--server-drop`       | Drop chance (0.0 to 1.0) for server packets.  | `--server-drop 0.2`           |
| `--client-delay`      | Delay chance (0.0 to 1.0) for client packets. | `--client-delay 0.3`          |
| `--server-delay`      | Delay chance (0.0 to 1.0) for server packets. | `--server-delay 0.4`          |
| `--client-delay-time` | Delay time for client packets (ms or range).  | `--client-delay-time 100-500` |
| `--server-delay-time` | Delay time for server packets (ms or range).  | `--server-delay-time 200-600` |
| `--control-port`      | Port for the control socket.                  | `--control-port 4500`         |

---

## **5. CSV Logging Format**

The packets are logged as CSVs, below is the format for each CSV files.

---

### **1. Client Logging (`log_client.csv`)**

| Column             | Description                                                     |
|--------------------|-----------------------------------------------------------------|
| `Timestamp`        | Time of the event (in microseconds precision).                  |
| `Event`            | Type of event (`Sent`, `Retransmit`, `Failed`, `Acknowledged`). |
| `Sequence`         | Sequence number of the packet.                                  |
| `Acknowledgment`   | Acknowledgment number received from the server.                 |
| `Source IP`        | Source IP address of the packet.                                |
| `Source Port`      | Source port of the packet.                                      |
| `Destination IP`   | Destination IP address of the packet.                           |
| `Destination Port` | Destination port of the packet.                                 |
| `Message`          | Message content of the packet.                                  |
| `Latency (ms)`     | Time taken for acknowledgment in milliseconds (if applicable).  |

---

### **2. Server Logging (`log_server.csv`)**

| Column             | Description                                       |
|--------------------|---------------------------------------------------|
| `Timestamp`        | Time of the event (in microseconds precision).    |
| `Event`            | Type of event (`Received`, `Out-of-Order`).       |
| `Sequence`         | Sequence number of the packet.                    |
| `Acknowledgment`   | Acknowledgment number sent to the client.         |
| `Source IP`        | Source IP address of the packet.                  |
| `Source Port`      | Source port of the packet.                        |
| `Destination IP`   | Destination IP address of the packet.             |
| `Destination Port` | Destination port of the packet.                   |
| `Message`          | Message content of the packet.                    |
| `Latency (ms)`     | Time taken to process the packet in milliseconds. |

---

### **3. Proxy Logging (`log_proxy.csv`)**

| Column             | Description                                                                       |
|--------------------|-----------------------------------------------------------------------------------|
| `Timestamp`        | Time of the event (in microseconds precision).                                    |
| `Event`            | Type of event (`Forwarded`, `Dropped`, `Duplicate`).                              |
| `Direction`        | Direction of the packet (`CTS` for Client-to-Server, `STC` for Server-to-Client). |
| `Sequence`         | Sequence number of the packet.                                                    |
| `Acknowledgment`   | Acknowledgment number (if applicable).                                            |
| `Source IP`        | Source IP address of the packet.                                                  |
| `Source Port`      | Source port of the packet.                                                        |
| `Destination IP`   | Destination IP address of the packet.                                             |
| `Destination Port` | Destination port of the packet.                                                   |
| `Message`          | Message content of the packet.                                                    |
| `Latency (ms)`     | Simulated delay or processing time in milliseconds.                               |
| `Drop Chance`      | Configured drop chance for the packet.                                            |
| `Delay Chance`     | Configured delay chance for the packet.                                           |
| `Delay Time (ms)`  | Simulated delay time for the packet in milliseconds.                              |

---


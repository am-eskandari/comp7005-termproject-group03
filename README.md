# Reliable Communication Protocol Using UDP

This project implements a **reliable communication protocol** using UDP, addressing challenges like packet loss and delays. It includes:
- A **client** for sending messages.
- A **server** for receiving and acknowledging messages.
- A **proxy server** to simulate unreliable network conditions with configurable parameters.

The proxy server allows **dynamic parameter updates** via a dedicated **control socket**, enabling real-time adjustments without restarting the server.

---

## **Setup Instructions**

### **Prerequisites**
- Tested on: **Arch Linux**, **Manjaro**, **Ubuntu**
- Python version: **3.12 or higher**
- Required libraries:
  - `socket`
  - `argparse`
  - `threading`

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

## **How to Run**

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
The proxy server relays packets between the client and server while simulating network conditions. It also provides a **control interface** for dynamic parameter updates.

Run the proxy server:
```bash
python proxy_server.py --listen-ip <IP> --listen-port <PORT> \
--target-ip <SERVER_IP> --target-port <SERVER_PORT> \
--client-drop <VALUE> --server-drop <VALUE> \
--client-delay <VALUE> --server-delay <VALUE> \
--client-delay-time <MILLISECONDS_OR_RANGE> --server-delay-time <MILLISECONDS_OR_RANGE> \
--control-port <PORT>
```

**Example:**
```bash
python proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
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

## **Changing Parameters Dynamically**

The proxy server supports **dynamic parameter updates** using the control socket (e.g., via **Netcat**).

### **Steps to Change Parameters**
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

## **Command-Line Arguments for Each File**

### **Client**
| Argument          | Description                       | Example                     |
|--------------------|-----------------------------------|-----------------------------|
| `--target-ip`      | IP address of the proxy server.   | `--target-ip 127.0.0.1`     |
| `--target-port`    | Port of the proxy server.         | `--target-port 4000`        |
| `--timeout`        | Timeout for acknowledgment (sec).| `--timeout 1`               |

---

### **Server**
| Argument          | Description                       | Example                     |
|--------------------|-----------------------------------|-----------------------------|
| `--listen-ip`      | IP address to bind the server.    | `--listen-ip 127.0.0.1`     |
| `--listen-port`    | Port for the server to listen on. | `--listen-port 5000`        |

---

### **Proxy Server**
| Argument            | Description                                     | Example                       |
|----------------------|-------------------------------------------------|-------------------------------|
| `--listen-ip`        | IP address to bind the proxy.                   | `--listen-ip 127.0.0.1`       |
| `--listen-port`      | Port to listen for client packets.              | `--listen-port 4000`          |
| `--target-ip`        | IP address of the server.                       | `--target-ip 127.0.0.1`       |
| `--target-port`      | Port of the server.                             | `--target-port 5000`          |
| `--client-drop`      | Drop chance (0.0 to 1.0) for client packets.    | `--client-drop 0.1`           |
| `--server-drop`      | Drop chance (0.0 to 1.0) for server packets.    | `--server-drop 0.2`           |
| `--client-delay`     | Delay chance (0.0 to 1.0) for client packets.   | `--client-delay 0.3`          |
| `--server-delay`     | Delay chance (0.0 to 1.0) for server packets.   | `--server-delay 0.4`          |
| `--client-delay-time`| Delay time for client packets (ms or range).    | `--client-delay-time 100-500` |
| `--server-delay-time`| Delay time for server packets (ms or range).    | `--server-delay-time 200-600` |
| `--control-port`     | Port for the control socket.                    | `--control-port 4500`         |

---

## **CSV Logging Format**

The packets are logged as CSVs, below is the format for each CSV files.

---

### **1. Client Logging (`log_client.csv`)**
| Column             | Description                                     |
|---------------------|-------------------------------------------------|
| `Timestamp`         | Time of the event (in microseconds precision).  |
| `Event`             | Type of event (`Sent`, `Retransmit`, `Failed`, `Acknowledged`). |
| `Sequence`          | Sequence number of the packet.                 |
| `Acknowledgment`    | Acknowledgment number received from the server. |
| `Source IP`         | Source IP address of the packet.               |
| `Source Port`       | Source port of the packet.                     |
| `Destination IP`    | Destination IP address of the packet.          |
| `Destination Port`  | Destination port of the packet.                |
| `Message`           | Message content of the packet.                |
| `Latency (ms)`      | Time taken for acknowledgment in milliseconds (if applicable). |

---

### **2. Server Logging (`log_server.csv`)**
| Column             | Description                                     |
|---------------------|-------------------------------------------------|
| `Timestamp`         | Time of the event (in microseconds precision).  |
| `Event`             | Type of event (`Received`, `Out-of-Order`).     |
| `Sequence`          | Sequence number of the packet.                 |
| `Acknowledgment`    | Acknowledgment number sent to the client.       |
| `Source IP`         | Source IP address of the packet.               |
| `Source Port`       | Source port of the packet.                     |
| `Destination IP`    | Destination IP address of the packet.          |
| `Destination Port`  | Destination port of the packet.                |
| `Message`           | Message content of the packet.                |
| `Latency (ms)`      | Time taken to process the packet in milliseconds. |

---

### **3. Proxy Logging (`log_proxy.csv`)**
| Column             | Description                                     |
|---------------------|-------------------------------------------------|
| `Timestamp`         | Time of the event (in microseconds precision).  |
| `Event`             | Type of event (`Forwarded`, `Dropped`, `Duplicate`). |
| `Sequence`          | Sequence number of the packet.                 |
| `Acknowledgment`    | Acknowledgment number (if applicable).          |
| `Source IP`         | Source IP address of the packet.               |
| `Source Port`       | Source port of the packet.                     |
| `Destination IP`    | Destination IP address of the packet.          |
| `Destination Port`  | Destination port of the packet.                |
| `Message`           | Message content of the packet.                |
| `Latency (ms)`      | Simulated delay or processing time in milliseconds. |
| `Drop Chance`       | Configured drop chance for the packet.          |
| `Delay Chance`      | Configured delay chance for the packet.         |
| `Delay Time (ms)`   | Simulated delay time for the packet in milliseconds. |

---

## **Project Highlights**
- Dynamic parameter adjustment using **control socket**.
- Support for **fixed or range-based delay times** in milliseconds.
- Real-time simulation of unreliable networks.
- Configurable packet drop and delay settings.
- 
This project was developed and tested on **Arch Linux** using Python. It demonstrates how to enhance UDP communication reliability through acknowledgment and retransmission mechanisms, along with handling packet loss and delay.

---

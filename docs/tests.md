# **Reliable UDP Protocol: Setup and Testing Guide**

This document provides comprehensive instructions for configuring, running, and testing a reliable UDP protocol
implementation using a client-proxy-server architecture.

---

## **Test Environment Setup**

### **1. Connecting to Lab Computers**

1. **Find the IP Address**:
    - Check the sticker on the desktop for the IP address, or use the CLI on the machine to retrieve it.
    - Lab computers use a subnet of `192.168.0.x`.

2. **Check Connectivity**:
    - Use the `ping` command to ensure the target machine is reachable:
      ```bash
      ping <ipofthecomputer>
      ```

3. **Connect via SSH**:
    - Use SSH to log in to the machine:
      ```bash
      ssh developer@<ipofthecomputer>
      ```
    - Credentials:
        - **Username**: `developer`
        - **Password**: `StaRs@L3`

---

### **2. Start the Server**

SSH into the server machine (`192.168.0.20`) and start the server process:

   ```bash
   ssh developer@192.168.0.20
   python server.py --listen-ip 192.168.0.20 --listen-port 5000
   ```

---

### **3. Start the Proxy (Default Configuration: Test Case 0)**

SSH into the proxy machine (`192.168.0.20`) and start the proxy server with the default settings:

   ```bash
   ssh developer@192.168.0.20
   python proxy.py --listen-ip 192.168.0.20 --listen-port 4000 \
   --target-ip 192.168.0.20 --target-port 5000 \
   --client-drop 0 --server-drop 0 \
   --client-delay 0 --server-delay 0 \
   --client-delay-time 0 --server-delay-time 0 \
   --control-port 4500
   ```

#### **Dynamic Proxy Configuration**

Modify proxy parameters dynamically without restarting the server by sending commands to the control port (`4500`):

   ```bash
   echo "SET client-drop 0.3 SET server-delay 0.5 SET client-delay-time 200" | nc -u 192.168.0.20 4500
   ```

##### Available Parameters

| Parameter           | Description                                             | Example Values   |
|---------------------|---------------------------------------------------------|------------------|
| `client-drop`       | Drop chance for client-to-server packets (0.0 to 1.0).  | `0.3` (30%)      |
| `server-drop`       | Drop chance for server-to-client packets (0.0 to 1.0).  | `0.5` (50%)      |
| `client-delay`      | Delay chance for client-to-server packets (0.0 to 1.0). | `0.7` (70%)      |
| `server-delay`      | Delay chance for server-to-client packets (0.0 to 1.0). | `1.0` (100%)     |
| `client-delay-time` | Delay time for client-to-server packets in ms or range. | `500`, `100-500` |
| `server-delay-time` | Delay time for server-to-client packets in ms or range. | `200`, `200-600` |

---

### **4. Run the Client**

Directly execute the client on the machine (`192.168.0.88`) to test communication:

   ```bash
   python client.py --target-ip 192.168.0.20 --target-port 4000 --timeout 2000
   ```

---

### **5. Verify Logs**

Review the following log files to confirm communication details and results:

- `packet_logs_client.log`
- `packet_logs_server.log`
- `packet_logs_proxy.log`
- `packet_logs_control.log`

---

## **Additional Setup and Troubleshooting**

### **1. Transferring Files**

1. **Copy the File**:
   Use the `scp` command to transfer your script to the appropriate machine. For example:
   ```bash
   scp "/path/to/script.py" developer@192.168.0.20:/home/developer/Public/
   ```

2. **Verify the File**:
   SSH into the machine and confirm the file is present:
   ```bash
   ssh developer@192.168.0.20
   ls -l /home/developer/Public/
   ```

3. **Navigate to the Directory**:
   Move to the directory where the file is located:
   ```bash
   cd /home/developer/Public/
   ```

---

### **2. Killing a Specific Port**

If a port is already in use, you can free it up by killing the process using it:

1. Find the process:
   ```bash
   sudo lsof -i UDP:5000
   ```

2. Kill the process:
   ```bash
   sudo kill -9 <PID>
   ```

3. Alternatively, immediately free the port:
   ```bash
   sudo fuser -k 5000/udp
   ```

---

### **3. Clearing `nftables` Rules**

Ensure no conflicting network rules:

- **List Active Rules**:
  ```bash
  sudo nft list ruleset
  ```
- **Flush Rules**:
  ```bash
  sudo nft flush ruleset
  ```

---

## **Testing with Sample Inputs**

Use the following inputs on the client side to validate the protocol's behavior under various scenarios:

1. **Short Message**
   ```text
   Hello, Server! This is a test message from the client.
   ```

2. **Medium-Length Message**
   ```text
   Reliable communication protocols are essential for maintaining seamless data transfer in unreliable networks.
   ```

3. **Long Message**
   ```text
   This project tests a reliable communication protocol using UDP. The system incorporates a proxy server to simulate real-world network conditions, including packet loss and delays, while dynamically adjusting parameters. The goal is to enhance data integrity and reliability over an unreliable medium.
   ```

4. **Repeating Pattern**
   ```text
   ABC123ABC123ABC123ABC123ABC123ABC123ABC123ABC123ABC123ABC123
   ```

5. **Edge Case (Symbols and Numbers)**
   ```text
   1234567890!@#$%^&*()_+-=~`<>?/.,[]{}|;:'"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
   ```

---

# **Test Scenarios and Configurations**

---

### **1. Baseline Scenario (No Drop or Delay)**

This scenario tests the protocol under ideal network conditions, with no packet drops or delays. It establishes a
baseline for comparing the performance of other configurations.

#### **Test Case 1: No Drop, No Delay**

```bash
echo "SET client-drop=0.0 server-drop=0.0 client-delay=0.0 server-delay=0.0 client-delay-time=0 server-delay-time=0" | nc -u 192.168.0.47 4500
```

---

### **2. Scenarios with Delays (No Packet Drops)**

#### **2.1 Client-Side Delays**

These scenarios apply delays only to the client. This helps test how the system responds to slower message transmission
from the client.

#### **Test Case 2: 50% Client Delay (0.5 Probability)**

```bash
echo "SET client-drop=0.0 server-drop=0.0 client-delay=0.5 server-delay=0.0 client-delay-time=100-500 server-delay-time=0" | nc -u 192.168.0.47 4500
```

#### **Test Case 3: 100% Client Delay (1.0 Probability)**

```bash
echo "SET client-drop=0.0 server-drop=0.0 client-delay=1.0 server-delay=0.0 client-delay-time=100-500 server-delay-time=0" | nc -u 192.168.0.47 4500
```

---

#### **2.2 Server-Side Delays**

These scenarios apply delays only to the server. This evaluates the system's handling of slower message responses from
the server.

#### **Test Case 4: 50% Server Delay (0.5 Probability)**

```bash
echo "SET client-drop=0.0 server-drop=0.0 client-delay=0.0 server-delay=0.5 client-delay-time=0 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

#### **Test Case 5: 100% Server Delay (1.0 Probability)**

```bash
echo "SET client-drop=0.0 server-drop=0.0 client-delay=0.0 server-delay=1.0 client-delay-time=0 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

---

#### **2.3 Combined Client and Server Delays**

These scenarios introduce delays on both the client and server sides simultaneously to analyze the compounded effects of
delays.

#### **Test Case 6: 50% Client Delay (0.5) and 50% Server Delay (0.5)**

```bash
echo "SET client-drop=0.0 server-drop=0.0 client-delay=0.5 server-delay=0.5 client-delay-time=100-500 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

#### **Test Case 7: 100% Client Delay (1.0) and 100% Server Delay (1.0)**

```bash
echo "SET client-drop=0.0 server-drop=0.0 client-delay=1.0 server-delay=1.0 client-delay-time=100-500 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

#### **Test Case 8: 50% Client Delay (0.5) and 100% Server Delay (1.0)**

```bash
echo "SET client-drop=0.0 server-drop=0.0 client-delay=0.5 server-delay=1.0 client-delay-time=100-500 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

#### **Test Case 9: 100% Client Delay (1.0) and 50% Server Delay (0.5)**

```bash
echo "SET client-drop=0.0 server-drop=0.0 client-delay=1.0 server-delay=0.5 client-delay-time=100-500 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

---

### **3. Drop Configurations (No Delay)**

#### **3.1 Client-Side Drops**

These tests simulate packet drops occurring only on the client side.

#### **Test Case 10: 50% Client Drop (0.5 Probability)**

```bash
echo "SET client-drop=0.5 server-drop=0.0 client-delay=0.0 server-delay=0.0 client-delay-time=0 server-delay-time=0" | nc -u 192.168.0.47 4500
```

#### **Test Case 11: 100% Client Drop (1.0 Probability)**

```bash
echo "SET client-drop=1.0 server-drop=0.0 client-delay=0.0 server-delay=0.0 client-delay-time=0 server-delay-time=0" | nc -u 192.168.0.47 4500
```

---

#### **3.2 Server-Side Drops**

These tests simulate packet drops occurring only on the server side.

#### **Test Case 12: 50% Server Drop (0.5 Probability)**

```bash
echo "SET client-drop=0.0 server-drop=0.5 client-delay=0.0 server-delay=0.0 client-delay-time=0 server-delay-time=0" | nc -u 192.168.0.47 4500
```

#### **Test Case 13: 100% Server Drop (1.0 Probability)**

```bash
echo "SET client-drop=0.0 server-drop=1.0 client-delay=0.0 server-delay=0.0 client-delay-time=0 server-delay-time=0" | nc -u 192.168.0.47 4500
```

---

#### **3.3 Combined Client and Server Drops**

These tests simulate packet drops occurring on both the client and server sides simultaneously.

#### **Test Case 14: 50% Client Drop (0.5) and 50% Server Drop (0.5)**

```bash
echo "SET client-drop=0.5 server-drop=0.5 client-delay=0.0 server-delay=0.0 client-delay-time=0 server-delay-time=0" | nc -u 192.168.0.47 4500
```

#### **Test Case 15: 100% Client Drop (1.0) and 50% Server Drop (0.5)**

```bash
echo "SET client-drop=1.0 server-drop=0.5 client-delay=0.0 server-delay=0.0 client-delay-time=0 server-delay-time=0" | nc -u 192.168.0.47 4500
```

#### **Test Case 16: 50% Client Drop (0.5) and 100% Server Drop (1.0)**

```bash
echo "SET client-drop=0.5 server-drop=1.0 client-delay=0.0 server-delay=0.0 client-delay-time=0 server-delay-time=0" | nc -u 192.168.0.47 4500
```

#### **Test Case 17: 100% Client Drop (1.0) and 100% Server Drop (1.0)**

```bash
echo "SET client-drop=1.0 server-drop=1.0 client-delay=0.0 server-delay=0.0 client-delay-time=0 server-delay-time=0" | nc -u 192.168.0.47 4500
```

---

## **4. Client Drop + Delay Configurations**

This section explores the combined effects of client-side drop and delay probabilities to analyze how packet loss and
latency interact on the client side.

---

### **4.1 Client Drop with Delay**

```bash
# Test Case 18: 50% Client Drop (0.5) + 50% Client Delay (0.5)
echo "SET client-drop=0.5 server-drop=0.0 client-delay=0.5 server-delay=0.0 client-delay-time=100-500 server-delay-time=0" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 19: 50% Client Drop (0.5) + 100% Client Delay (1.0)
echo "SET client-drop=0.5 server-drop=0.0 client-delay=1.0 server-delay=0.0 client-delay-time=100-500 server-delay-time=0" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 20: 100% Client Drop (1.0) + 50% Client Delay (0.5)
echo "SET client-drop=1.0 server-drop=0.0 client-delay=0.5 server-delay=0.0 client-delay-time=100-500 server-delay-time=0" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 21: 100% Client Drop (1.0) + 100% Client Delay (1.0)
echo "SET client-drop=1.0 server-drop=0.0 client-delay=1.0 server-delay=0.0 client-delay-time=100-500 server-delay-time=0" | nc -u 192.168.0.47 4500
```

---

## **5. Server Drop + Delay Configurations**

This section examines the combined effects of server-side drop and delay probabilities to understand how these factors
affect server behavior independently.

---

### **5.1 Server Drop with Delay**

```bash
# Test Case 22: 50% Server Drop (0.5) + 50% Server Delay (0.5)
echo "SET client-drop=0.0 server-drop=0.5 client-delay=0.0 server-delay=0.5 client-delay-time=0 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 23: 50% Server Drop (0.5) + 100% Server Delay (1.0)
echo "SET client-drop=0.0 server-drop=0.5 client-delay=0.0 server-delay=1.0 client-delay-time=0 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 24: 100% Server Drop (1.0) + 50% Server Delay (0.5)
echo "SET client-drop=0.0 server-drop=1.0 client-delay=0.0 server-delay=0.5 client-delay-time=0 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 25: 100% Server Drop (1.0) + 100% Server Delay (1.0)
echo "SET client-drop=0.0 server-drop=1.0 client-delay=0.0 server-delay=1.0 client-delay-time=0 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

---

## **6. Combined Client and Server Drop + Delay Configurations**

This section explores the interaction between drop and delay probabilities across both the client and server
simultaneously, ensuring thorough testing of symmetric and asymmetric conditions.

---

```bash
# Test Case 26: 50% Client Drop (0.5) + 50% Server Drop (0.5) + 50% Client Delay (0.5) + 50% Server Delay (0.5)
echo "SET client-drop=0.5 server-drop=0.5 client-delay=0.5 server-delay=0.5 client-delay-time=100-500 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 27: 100% Client Drop (1.0) + 50% Server Drop (0.5) + 100% Client Delay (1.0) + 50% Server Delay (0.5)
echo "SET client-drop=1.0 server-drop=0.5 client-delay=1.0 server-delay=0.5 client-delay-time=100-500 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 28: 50% Client Drop (0.5) + 100% Server Drop (1.0) + 50% Client Delay (0.5) + 100% Server Delay (1.0)
echo "SET client-drop=0.5 server-drop=1.0 client-delay=0.5 server-delay=1.0 client-delay-time=100-500 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 29: 100% Client Drop (1.0) + 100% Server Drop (1.0) + 100% Client Delay (1.0) + 100% Server Delay (1.0)
echo "SET client-drop=1.0 server-drop=1.0 client-delay=1.0 server-delay=1.0 client-delay-time=100-500 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 30: 50% Client Drop (0.5) + 0% Server Drop (0.0) + 50% Client Delay (0.5) + 100% Server Delay (1.0)
echo "SET client-drop=0.5 server-drop=0.0 client-delay=0.5 server-delay=1.0 client-delay-time=100-500 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 31: 0% Client Drop (0.0) + 50% Server Drop (0.5) + 100% Client Delay (1.0) + 50% Server Delay (0.5)
echo "SET client-drop=0.0 server-drop=0.5 client-delay=1.0 server-delay=0.5 client-delay-time=100-500 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 32: 50% Client Drop (0.5) + 100% Server Drop (1.0) + 100% Client Delay (1.0) + 0% Server Delay (0.0)
echo "SET client-drop=0.5 server-drop=1.0 client-delay=1.0 server-delay=0.0 client-delay-time=100-500 server-delay-time=0" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 33: 100% Client Drop (1.0) + 50% Server Drop (0.5) + 0% Client Delay (0.0) + 100% Server Delay (1.0)
echo "SET client-drop=1.0 server-drop=0.5 client-delay=0.0 server-delay=1.0 client-delay-time=0 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 34: 50% Client Drop (0.5) + 100% Server Drop (1.0) + 50% Client Delay (0.5) + 0% Server Delay (0.0)
echo "SET client-drop=0.5 server-drop=1.0 client-delay=0.5 server-delay=0.0 client-delay-time=100-500 server-delay-time=0" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 35: 0% Client Drop (0.0) + 50% Server Drop (0.5) + 50% Client Delay (0.5) + 50% Server Delay (0.5)
echo "SET client-drop=0.0 server-drop=0.5 client-delay=0.5 server-delay=0.5 client-delay-time=100-500 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 36: 50% Client Drop (0.5) + 0% Server Drop (0.0) + 100% Client Delay (1.0) + 50% Server Delay (0.5)
echo "SET client-drop=0.5 server-drop=0.0 client-delay=1.0 server-delay=0.5 client-delay-time=100-500 server-delay-time=200-600" | nc -u 192.168.0.47 4500
```

---

## **7. Additional Delay Time Test Cases**

This section focuses on specific delay time configurations to evaluate the protocol's behavior under edge cases related
to fixed and extended delays.

---

### **Server and Client Set-Up**

For all the tests in this section, use the following commands:

#### **1. Start the Server**

```bash
python server.py --listen-ip 192.168.0.19 --listen-port 5000
```

#### **2. Start the Proxy**

Use the commands provided in the test cases below.

#### **3. Start the Client**

```bash
python client.py --target-ip 192.168.0.20 --target-port 4000 --timeout 1000
```

---

### **7.1 Fixed Delay Time Test**

This test sets a fixed delay time of **500 ms** on either the client or server side, instead of an interval, to evaluate
the protocol's handling of consistent delay.

#### **Commands for Fixed Delay Time Test**

```bash
# Test Case 37: Fixed 500 ms Client Delay
echo "SET client-drop=0.0 server-drop=0.0 client-delay=0.5 server-delay=0.0 client-delay-time=500 server-delay-time=0" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 38: Fixed 500 ms Server Delay
echo "SET client-drop=0.0 server-drop=0.0 client-delay=0.0 server-delay=0.5 client-delay-time=0 server-delay-time=500" | nc -u 192.168.0.47 4500
```

---

### **7.2 Extended Delay Beyond Retry Timeout**

This test sets a delay longer than the client's retry timeout to evaluate how the protocol handles extreme delay
scenarios.

#### **Commands for Extended Delay Beyond Retry Timeout**

```bash
# Test Case 39: Client Delay Beyond Retry Timeout
echo "SET client-drop=0.0 server-drop=0.0 client-delay=1.0 server-delay=0.0 client-delay-time=2000 server-delay-time=0" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 40: Server Delay Beyond Retry Timeout
echo "SET client-drop=0.0 server-drop=0.0 client-delay=0.0 server-delay=1.0 client-delay-time=0 server-delay-time=2000" | nc -u 192.168.0.47 4500
```

```bash
# Test Case 41: Both Client and Server Delay Beyond Retry Timeout
echo "SET client-drop=0.0 server-drop=0.0 client-delay=1.0 server-delay=1.0 client-delay-time=2000 server-delay-time=2000" | nc -u 192.168.0.47 4500
```

---

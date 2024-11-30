# **Test Case Compilation for Reliable UDP Protocol**

This document lists all the test cases to verify the reliability of the UDP protocol implementation under various drop
and delay configurations. Use these commands to execute the tests and validate the protocol's behavior.

## **Execution Steps**

1. **Start the server**:
   ```bash
   python3 server.py --listen-ip 127.0.0.1 --listen-port 5000
   ```

2. **Run the proxy server** using one of the above configurations.

3. **Start the client**:
   ```bash
   python3 client.py --target-ip 127.0.0.1 --target-port 4000 --timeout 2
   ```

4. **Collect Logs**:
    - Verify `log_client.csv`, `log_server.csv`, and `log_proxy.csv` for results.

---

# Test Configurations

---

## **1. Base Case (No Drop or Delay)**

```bash
# Test Case 1: No Drop, No Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

---

## **2. Delay Configurations (No Drop)**

This section explores the impact of delay configurations on the client and server, including various combinations of
delay probabilities.

### **2.1 Client Delay Only**

```bash
# Test Case 2: 50% Client Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 50 --server-delay 0 \
--client-delay-time 100-500 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 5: 100% Client Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 100 --server-delay 0 \
--client-delay-time 100-500 --server-delay-time 0 \
--control-port 4500
```

---

### **2.2 Server Delay Only**

```bash
# Test Case 3: 50% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 0 --server-delay 50 \
--client-delay-time 0 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 6: 100% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 0 --server-delay 100 \
--client-delay-time 0 --server-delay-time 200-600 \
--control-port 4500
```

---

### **2.3 Combined Client and Server Delay**

```bash
# Test Case 4: 50% Client Delay and 50% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 50 --server-delay 50 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 7: 100% Client Delay and 100% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 100 --server-delay 100 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 8: 50% Client Delay and 100% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 50 --server-delay 100 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 9: 100% Client Delay and 50% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 100 --server-delay 50 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

---

## **3. Drop Configurations (No Delay)**

This section explores the effects of packet drops without any delay interference.

---

### **3.1 Client Drop Only**

```bash
# Test Case 10: 50% Client Drop
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 0 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 11: 100% Client Drop
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 0 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

---

### **3.2 Server Drop Only**

```bash
# Test Case 12: 50% Server Drop
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 50 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 13: 100% Server Drop
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 100 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

---

### **3.3 Combined Client and Server Drop**

```bash
# Test Case 14: 50% Client Drop and 50% Server Drop
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 50 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 15: 100% Client Drop and 50% Server Drop
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 50 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 16: 50% Client Drop and 100% Server Drop
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 100 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 17: 100% Client Drop and 100% Server Drop
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 100 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

---

## **4. Client Drop + Delay Configurations**

This section explores the combined effects of client-side drop and delay probabilities to analyze how packet loss and
latency interact on the client side.

---

### **4.1 Client Drop with Delay**

```bash
# Test Case 18: 50% Client Drop + 50% Client Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 0 \
--client-delay 50 --server-delay 0 \
--client-delay-time 100-500 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 19: 50% Client Drop + 100% Client Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 0 \
--client-delay 100 --server-delay 0 \
--client-delay-time 100-500 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 20: 100% Client Drop + 50% Client Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 0 \
--client-delay 50 --server-delay 0 \
--client-delay-time 100-500 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 21: 100% Client Drop + 100% Client Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 0 \
--client-delay 100 --server-delay 0 \
--client-delay-time 100-500 --server-delay-time 0 \
--control-port 4500
```

---

## **5. Server Drop + Delay Configurations**

This section examines the combined effects of server-side drop and delay probabilities to understand how these factors
affect server behavior independently.

---

### **5.1 Server Drop with Delay**

```bash
# Test Case 22: 50% Server Drop + 50% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 50 \
--client-delay 0 --server-delay 50 \
--client-delay-time 0 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 23: 50% Server Drop + 100% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 50 \
--client-delay 0 --server-delay 100 \
--client-delay-time 0 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 24: 100% Server Drop + 50% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 100 \
--client-delay 0 --server-delay 50 \
--client-delay-time 0 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 25: 100% Server Drop + 100% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 100 \
--client-delay 0 --server-delay 100 \
--client-delay-time 0 --server-delay-time 200-600 \
--control-port 4500
```

---

## **6. Combined Client and Server Drop + Delay Configurations**

This section explores the interaction between drop and delay probabilities across both the client and server
simultaneously, ensuring thorough testing of symmetric and asymmetric conditions.

---

```bash
# Test Case 26: 50% Client Drop + 50% Server Drop + 50% Client Delay + 50% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 50 \
--client-delay 50 --server-delay 50 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 27: 100% Client Drop + 50% Server Drop + 100% Client Delay + 50% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 50 \
--client-delay 100 --server-delay 50 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 28: 50% Client Drop + 100% Server Drop + 50% Client Delay + 100% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 100 \
--client-delay 50 --server-delay 100 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 29: 100% Client Drop + 100% Server Drop + 100% Client Delay + 100% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 100 \
--client-delay 100 --server-delay 100 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 30: 50% Client Drop + 0% Server Drop + 50% Client Delay + 100% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 0 \
--client-delay 50 --server-delay 100 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 31: 0% Client Drop + 50% Server Drop + 100% Client Delay + 50% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 50 \
--client-delay 100 --server-delay 50 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 32: 50% Client Drop + 100% Server Drop + 100% Client Delay + 0% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 100 \
--client-delay 100 --server-delay 0 \
--client-delay-time 100-500 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 33: 100% Client Drop + 50% Server Drop + 0% Client Delay + 100% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 50 \
--client-delay 0 --server-delay 100 \
--client-delay-time 0 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 34: 50% Client Drop + 100% Server Drop + 50% Client Delay + 0% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 100 \
--client-delay 50 --server-delay 0 \
--client-delay-time 100-500 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 35: 0% Client Drop + 50% Server Drop + 50% Client Delay + 50% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 50 \
--client-delay 50 --server-delay 50 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 36: 50% Client Drop + 0% Server Drop + 100% Client Delay + 50% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 0 \
--client-delay 100 --server-delay 50 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

---

Here’s a new section for the additional test cases, along with server, client, and proxy configurations to test these
scenarios.

---

## **7. Additional Delay Time Test Cases**

This section focuses on specific delay time configurations to evaluate the protocol's behavior under edge cases related
to fixed and extended delay times.

### **7.1 Fixed Delay Time Test**

This test sets a fixed delay time of **500 ms** on either the client or server side, instead of an interval, to evaluate
the protocol's handling of consistent delay.


---

#### **Commands for Fixed Delay Time Test**

```bash
# Test Case 37: Fixed 500 ms Client Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 50 --server-delay 0 \
--client-delay-time 500 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 38: Fixed 500 ms Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 0 --server-delay 50 \
--client-delay-time 0 --server-delay-time 500 \
--control-port 4500
```

---

### **7.2 Extended Delay Beyond Retry Timeout**

This test sets a delay longer than the client's retry timeout to evaluate how the protocol handles extreme delay
scenarios.

---

#### **Commands for Extended Delay Beyond Retry Timeout**

```bash
# Test Case 39: Client Delay Beyond Retry Timeout
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 100 --server-delay 0 \
--client-delay-time 2000 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 40: Server Delay Beyond Retry Timeout
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 0 --server-delay 100 \
--client-delay-time 0 --server-delay-time 2000 \
--control-port 4500
```

```bash
# Test Case 41: Both Client and Server Delay Beyond Retry Timeout
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 100 --server-delay 100 \
--client-delay-time 2000 --server-delay-time 2000 \
--control-port 4500
```

---

### **Server and Client Commands**

For all the above tests, use the following commands to start the server and client:

#### **Start the Server**

```bash
python3 server.py --listen-ip 127.0.0.1 --listen-port 5000
```

#### **Start the Client**

```bash
python3 client.py --target-ip 127.0.0.1 --target-port 4000 --timeout 1
```

---

## **8. Changing Parameters Dynamically**

The proxy server supports **dynamic parameter updates** using the control socket (e.g., via **Netcat**). This allows you
to modify drop chances, delay probabilities, and delay times without restarting the proxy server.

---

### **8.1 Steps to Change Parameters**

1. **Start the Proxy Server**  
   Run the proxy server with the base case configuration:
   ```bash
   python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
   --target-ip 127.0.0.1 --target-port 5000 \
   --client-drop 0 --server-drop 0 \
   --client-delay 0 --server-delay 0 \
   --client-delay-time 0 --server-delay-time 0 \
   --control-port 4500
   ```

2. **Modify Parameters Dynamically**  
   Use Netcat (`nc`) to send commands to the control socket and modify parameters.

#### **Available Parameters**

| Parameter           | Description                                             | Example Values   |
|---------------------|---------------------------------------------------------|------------------|
| `client-drop`       | Drop chance for client-to-server packets (0.0 to 1.0).  | `0.3` (30%)      |
| `server-drop`       | Drop chance for server-to-client packets (0.0 to 1.0).  | `0.5` (50%)      |
| `client-delay`      | Delay chance for client-to-server packets (0.0 to 1.0). | `0.7` (70%)      |
| `server-delay`      | Delay chance for server-to-client packets (0.0 to 1.0). | `1.0` (100%)     |
| `client-delay-time` | Delay time for client-to-server packets in ms or range. | `100`, `100-500` |
| `server-delay-time` | Delay time for server-to-client packets in ms or range. | `200`, `200-600` |

---

### **8.2 Example Test Flow**

Below is an example of testing parameter changes dynamically.

1. **Start with the Base Case**  
   Run the client and server alongside the proxy server with no drops or delays.

    - **Server:**
      ```bash
      python3 server.py --listen-ip 127.0.0.1 --listen-port 5000
      ```
    - **Client:**
      ```bash
      python3 client.py --target-ip 127.0.0.1 --target-port 4000 --timeout 1
      ```
    - **Proxy:**
      ```bash
      python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
      --target-ip 127.0.0.1 --target-port 5000 \
      --client-drop 0 --server-drop 0 \
      --client-delay 0 --server-delay 0 \
      --client-delay-time 0 --server-delay-time 0 \
      --control-port 4500
      ```

2. **Modify Parameters Dynamically**  
   Test the effect of parameter changes step-by-step.

    - **Set Client Drop Chance to 30%**  
      Introduce a moderate drop rate for client-to-server packets:
      ```bash
      echo "SET client-drop 0.3" | nc -u 127.0.0.1 4500
      ```

    - **Set Server Delay to 50%**  
      Simulate latency on server-to-client packets:
      ```bash
      echo "SET server-delay 0.5" | nc -u 127.0.0.1 4500
      ```

    - **Set Client Delay Time to Fixed 200 ms**  
      Introduce a consistent delay for client-to-server packets:
      ```bash
      echo "SET client-delay-time 200" | nc -u 127.0.0.1 4500
      ```

    - **Set Server Drop Chance to 100%**  
      Simulate complete loss of server-to-client packets:
      ```bash
      echo "SET server-drop 1.0" | nc -u 127.0.0.1 4500
      ```

3. **Observe Behavior**  
   Monitor the client and server logs to observe how the protocol handles the dynamically updated conditions. Look for
   retransmissions, timeouts, and acknowledgment delays in the logs.

---
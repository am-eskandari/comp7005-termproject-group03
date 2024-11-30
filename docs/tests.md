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

## **2. Delay Configurations (No Drop)**

This section focuses on delay scenarios without introducing any packet drops to evaluate the impact of latency on the
protocol. It includes configurations for client-only delays, server-only delays, and combined client and server delays.

---

### **Client Delay Only**

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
# Test Case 3: 100% Client Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 100 --server-delay 0 \
--client-delay-time 100-500 --server-delay-time 0 \
--control-port 4500
```

---

### **Server Delay Only**

```bash
# Test Case 4: 50% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 0 --server-delay 50 \
--client-delay-time 0 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# Test Case 5: 100% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 0 --server-delay 100 \
--client-delay-time 0 --server-delay-time 200-600 \
--control-port 4500
```

---

### **Combined Client and Server Delay**

```bash
# Test Case 6: 50% Client Delay and 50% Server Delay
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

Below are the explicit bash commands for the **Drop Configurations (No Delay)** test cases. Each command is tailored to
match the configurations outlined in the table:

---

### **Client Drop Only**

```bash
# Test Case 8: 50% Client Drop, No Server Drop, No Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 0 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 9: 100% Client Drop, No Server Drop, No Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 0 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

---

### **Server Drop Only**

```bash
# Test Case 10: No Client Drop, 50% Server Drop, No Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 50 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 11: No Client Drop, 100% Server Drop, No Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 100 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

---

### **Combined Client and Server Drop**

```bash
# Test Case 12: 50% Client Drop, 50% Server Drop, No Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 50 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 13: 100% Client Drop, 50% Server Drop, No Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 50 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 14: 50% Client Drop, 100% Server Drop, No Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 100 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

```bash
# Test Case 15: 100% Client Drop, 100% Server Drop, No Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 100 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

---

### **Summary**

This section includes all commands necessary to test:

1. **Client Drop Only** at 50% and 100%.
2. **Server Drop Only** at 50% and 100%.
3. **Combined Client and Server Drop** with symmetrical and asymmetrical drop probabilities.

Let me know if further adjustments are required!


---

## **4. Client Drop + Delay Configurations**

```bash
# 50% Client Drop + 50% Client Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 0 \
--client-delay 50 --server-delay 0 \
--client-delay-time 100-500 --server-delay-time 0 \
--control-port 4500
```

```bash
# 100% Client Drop + 100% Client Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 0 \
--client-delay 100 --server-delay 0 \
--client-delay-time 100-500 --server-delay-time 0 \
--control-port 4500
```

---

## **5. Server Drop + Delay Configurations**

```bash
# 50% Server Drop + 50% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 50 \
--client-delay 0 --server-delay 50 \
--client-delay-time 0 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# 100% Server Drop + 100% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 100 \
--client-delay 0 --server-delay 100 \
--client-delay-time 0 --server-delay-time 200-600 \
--control-port 4500
```

---

## **6. Combined Client and Server Drop + Delay Configurations**

```bash
# 50% Drop and Delay on Both Client and Server
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 50 \
--client-delay 50 --server-delay 50 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# 100% Client Drop and Delay + 50% Server Drop and Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 50 \
--client-delay 100 --server-delay 50 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# 100% Drop and Delay on Both Client and Server
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 100 \
--client-delay 100 --server-delay 100 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

---
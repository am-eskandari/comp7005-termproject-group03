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
# Test Case 5: 100% Client Delay
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

### **Combined Client and Server Delay**

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

### **Client Drop Only**

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

### **Server Drop Only**

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

### **Combined Client and Server Drop**

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

### **Client Drop with Delay**

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

### **Server Drop with Delay**

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


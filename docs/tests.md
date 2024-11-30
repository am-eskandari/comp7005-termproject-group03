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

## **1. Base Case and Delay Configurations (No Drop)**

### **Base Case**

```bash
# No Drop, No Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

### **Delay Configurations**

```bash
# 50% Client Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 50 --server-delay 0 \
--client-delay-time 100-500 --server-delay-time 0 \
--control-port 4500
```

```bash
# 50% Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 0 --server-delay 50 \
--client-delay-time 0 --server-delay-time 200-600 \
--control-port 4500
```

```bash
# 100% Client and Server Delay
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 100 --server-delay 100 \
--client-delay-time 100-500 --server-delay-time 200-600 \
--control-port 4500
```

---

## **2. Drop Configurations (No Delay)**

### **Client Drop Configurations**

```bash
# 50% Client Drop
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 50 --server-drop 0 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

```bash
# 100% Client Drop
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 100 --server-drop 0 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

### **Server Drop Configurations**

```bash
# 50% Server Drop
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 50 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

```bash
# 100% Server Drop
python3 proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
--target-ip 127.0.0.1 --target-port 5000 \
--client-drop 0 --server-drop 100 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

---

## **3. Client Drop + Delay Configurations**

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

## **4. Server Drop + Delay Configurations**

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

## **5. Combined Client and Server Drop + Delay Configurations**

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
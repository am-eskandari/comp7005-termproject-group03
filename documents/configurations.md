### **Base Case**
- **0% Drop, 0% Delay Chance**
  ```bash
  python proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
  --target-ip 127.0.0.1 --target-port 5000 \
  --client-drop 0.0 --server-drop 0.0 \
  --client-delay 0.0 --server-delay 0.0 \
  --client-delay-time 0 --server-delay-time 0 \
  --control-port 4500
  ```

### **Unique Test Configurations**

#### **1. Drop Chance Only (No Delay Chance)**
- **50% Drop, 0% Delay**
  ```bash
  python proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
  --target-ip 127.0.0.1 --target-port 5000 \
  --client-drop 0.5 --server-drop 0.5 \
  --client-delay 0.0 --server-delay 0.0 \
  --client-delay-time 0 --server-delay-time 0 \
  --control-port 4500
  ```
- **100% Drop, 0% Delay**
  ```bash
  python proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
  --target-ip 127.0.0.1 --target-port 5000 \
  --client-drop 1.0 --server-drop 1.0 \
  --client-delay 0.0 --server-delay 0.0 \
  --client-delay-time 0 --server-delay-time 0 \
  --control-port 4500
  ```

#### **2. Delay Chance Only (No Drop Chance)**
- **0% Drop, 50% Delay**
  ```bash
  python proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
  --target-ip 127.0.0.1 --target-port 5000 \
  --client-drop 0.0 --server-drop 0.0 \
  --client-delay 0.5 --server-delay 0.5 \
  --client-delay-time 0 --server-delay-time 0 \
  --control-port 4500
  ```
- **0% Drop, 100% Delay**
  ```bash
  python proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
  --target-ip 127.0.0.1 --target-port 5000 \
  --client-drop 0.0 --server-drop 0.0 \
  --client-delay 1.0 --server-delay 1.0 \
  --client-delay-time 0 --server-delay-time 0 \
  --control-port 4500
  ```

#### **3. Combined Drop and Delay Chances**
- **50% Drop, 50% Delay**
  ```bash
  python proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
  --target-ip 127.0.0.1 --target-port 5000 \
  --client-drop 0.5 --server-drop 0.5 \
  --client-delay 0.5 --server-delay 0.5 \
  --client-delay-time 0 --server-delay-time 0 \
  --control-port 4500
  ```
- **100% Drop, 50% Delay**
  ```bash
  python proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
  --target-ip 127.0.0.1 --target-port 5000 \
  --client-drop 1.0 --server-drop 1.0 \
  --client-delay 0.5 --server-delay 0.5 \
  --client-delay-time 0 --server-delay-time 0 \
  --control-port 4500
  ```
- **50% Drop, 100% Delay**
  ```bash
  python proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
  --target-ip 127.0.0.1 --target-port 5000 \
  --client-drop 0.5 --server-drop 0.5 \
  --client-delay 1.0 --server-delay 1.0 \
  --client-delay-time 0 --server-delay-time 0 \
  --control-port 4500
  ```
- **100% Drop, 100% Delay**
  ```bash
  python proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
  --target-ip 127.0.0.1 --target-port 5000 \
  --client-drop 1.0 --server-drop 1.0 \
  --client-delay 1.0 --server-delay 1.0 \
  --client-delay-time 0 --server-delay-time 0 \
  --control-port 4500
  ```

#### **4. Delay Time Longer than Retry Timeout (No Drop)**
- **1500 ms Delay, 0% Delay Chance**
  ```bash
  python proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
  --target-ip 127.0.0.1 --target-port 5000 \
  --client-drop 0.0 --server-drop 0.0 \
  --client-delay 0.0 --server-delay 0.0 \
  --client-delay-time 1500 --server-delay-time 1500 \
  --control-port 4500
  ```
- **1500 ms Delay, 50% Delay Chance**
  ```bash
  python proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
  --target-ip 127.0.0.1 --target-port 5000 \
  --client-drop 0.0 --server-drop 0.0 \
  --client-delay 0.5 --server-delay 0.5 \
  --client-delay-time 1500 --server-delay-time 1500 \
  --control-port 4500
  ```
- **1500 ms Delay, 100% Delay Chance**
  ```bash
  python proxy_server.py --listen-ip 127.0.0.1 --listen-port 4000 \
  --target-ip 127.0.0.1 --target-port 5000 \
  --client-drop 0.0 --server-drop 0.0 \
  --client-delay 1.0 --server-delay 1.0 \
  --client-delay-time 1500 --server-delay-time 1500 \
  --control-port 4500
  ```

### **Summary**
1. **Start the Server** (common for all tests):
   ```bash
   python server.py --listen-ip 127.0.0.1 --listen-port 5000
   ```
2. **Start the Proxy Server** with each of the above commands (change parameters for each test).
3. **Start the Client** (common for all tests):
   ```bash
   python client.py --target-ip 127.0.0.1 --target-port 4000 --timeout 1
   ```

These combinations represent **10 distinct configurations** with the base case included. Each scenario should be run in **three separate terminals**: one for the server, one for the proxy server, and one for the client.
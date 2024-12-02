# **Guide to Setting Up and Running the Test**

This guide provides step-by-step instructions for setting up and running a client-proxy-server test using specific IP
addresses and ports.

---

## **1. Clearing `nftables`**

### **Step 1: Check Current Rules**

To view the active `nftables` rules:

```bash
sudo nft list ruleset
```

### **Step 2: Flush All Rules**

To clear all active rules while retaining tables and chains:

```bash
sudo nft flush ruleset
```

This ensures there are no conflicting network configurations during the test.

---

## **2. Connecting to Lab Computers**

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

## **3. Transferring Files**

1. **Copy the File**:
   Use the `scp` command to transfer your script to the appropriate machine. For example:
   ```bash
   scp "/home/Ymir/Documents/Code Repository/BCIT/BScACS/comp7005-termproject-group03/proxy_server.py" developer@192.168.0.19:/home/developer/Public/
   ```

2. **Verify the File**:
   SSH into the machine and confirm the file is present:
   ```bash
   ssh developer@192.168.0.19
   ls -l /home/developer/Public/
   ```

3. **Navigate to the Directory**:
   Move to the directory where the file is located:
   ```bash
   cd /home/developer/Public/
   ```

---

## **4. Killing a Specific Port**

If a port is already in use, you can free it up by killing the process using it.

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

## **5. Current Setup for the Test**

### **Server Configuration**

Run the server on `192.168.0.18`:

```bash
python3 server.py --listen-ip 192.168.0.18 --listen-port 5000
```

### **Proxy Configuration**

Run the proxy server on `192.168.0.19`:

```bash
python3 proxy_server.py --listen-ip 192.168.0.19 --listen-port 4000 \
--target-ip 192.168.0.18 --target-port 5000 \
--client-drop 0 --server-drop 0 \
--client-delay 0 --server-delay 0 \
--client-delay-time 0 --server-delay-time 0 \
--control-port 4500
```

### **Client Configuration**

Run the client on `192.168.0.88`:

```bash
python3 client.py --target-ip 192.168.0.19 --target-port 4000 --timeout 1
```

---

## **6. Workflow to Run the Test**

1. **Start the Server**:
    - SSH into `192.168.0.18` and run the server:
      ```bash
      ssh developer@192.168.0.18
      python3 server.py --listen-ip 192.168.0.18 --listen-port 5000
      ```

2. **Start the Proxy Server**:
    - SSH into `192.168.0.19` and run the proxy server:
      ```bash
      ssh developer@192.168.0.19
      python3 proxy_server.py --listen-ip 192.168.0.19 --listen-port 4000 \
      --target-ip 192.168.0.18 --target-port 5000 \
      --client-drop 0 --server-drop 0 \
      --client-delay 0 --server-delay 0 \
      --client-delay-time 0 --server-delay-time 0 \
      --control-port 4500
      ```

3. **Run the Client**:
    - SSH into `192.168.0.88` and run the client:
      ```bash
      ssh Ymir@192.168.0.88
      python3 client.py --target-ip 192.168.0.19 --target-port 4000 --timeout 1
      ```

4. **Monitor Logs**:
    - Observe the logs on each machine to ensure proper communication between the client, proxy, and server.

---

## **7. Additional Notes**

- If network configurations change or additional tests require varying parameters, update the proxy server settings
  using its control port (`4500`). For example:
  ```bash
  echo "SET client-drop 0.3, SET server-delay 0.5, SET client-delay-time 200" | nc -u 192.168.0.19 4500
  ```
- Ensure each script is tested independently before integrating all components for the test.

---

ls -R > repo_structure.txt

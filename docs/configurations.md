# **Test Case Configuration List**

Each table organizes the test cases logically to cover all possible configurations of client and server drop and delay
parameters. Below is an explanation for each table and the reasoning behind the selected configurations:

### **Key Considerations for the Configurations**

1. **Coverage:** The configurations comprehensively test individual and combined effects of drop and delay on the client
   and server.
2. **Separation of Concerns:** Isolating client and server impacts helps identify specific weaknesses or inefficiencies
   in the protocol.
3. **Symmetry and Asymmetry:** Testing both symmetric and asymmetric conditions ensures the protocol is robust under
   varied network conditions.
4. **Extreme Cases:** Including 100% probabilities for drop and delay tests the upper bounds of the system's resilience.

---

### **1. Base Case and Delay Configurations (No Drop)**

This table isolates delay configurations without introducing any packet drops. It serves as a baseline for understanding
the impact of delays alone.

- **Base Case (Test Case 1):** No drop or delay, serving as the control test to verify that the system works without
  interference.
- **Client Delay Only (Test Cases 2, 5):** Tests the impact of 50% and 100% delay probabilities on the client side while
  keeping the server unaffected.
- **Server Delay Only (Test Cases 3, 6):** Tests the impact of 50% and 100% delay probabilities on the server side while
  keeping the client unaffected.
- **Combined Client and Server Delay (Test Cases 4, 7):** Evaluates scenarios where both client and server experience
  delays simultaneously, using 50% or 100% probabilities for each.

| Test Case | Client Drop (%) | Server Drop (%) | Client Delay (%) | Server Delay (%) | Delay Time (ms)                              | Description                          |
|-----------|-----------------|-----------------|------------------|------------------|----------------------------------------------|--------------------------------------|
| 1         | 0               | 0               | 0                | 0                | 0                                            | No drop or delay (Base Case)         |
| 2         | 0               | 0               | 50               | 0                | 100-500 (client-side)                        | 50% delay on client only             |
| 3         | 0               | 0               | 0                | 50               | 200-600 (server-side)                        | 50% delay on server only             |
| 4         | 0               | 0               | 50               | 50               | 100-500 (client-side), 200-600 (server-side) | 50% delay on both client and server  |
| 5         | 0               | 0               | 100              | 0                | 100-500 (client-side)                        | 100% delay on client only            |
| 6         | 0               | 0               | 0                | 100              | 200-600 (server-side)                        | 100% delay on server only            |
| 7         | 0               | 0               | 100              | 100              | 100-500 (client-side), 200-600 (server-side) | 100% delay on both client and server |

---

### **2. Drop Configurations (No Delay)**

This table focuses exclusively on drop scenarios to understand the effects of packet loss without any delay
interference.

- **Client Drop Only (Test Cases 8, 9):** Tests the effect of 50% and 100% packet drop probabilities on the client side
  while keeping the server unaffected.
- **Server Drop Only (Test Cases 10, 11):** Tests the effect of 50% and 100% packet drop probabilities on the server
  side while keeping the client unaffected.
- **Combined Client and Server Drop (Test Cases 12-15):** Covers scenarios where both client and server experience
  drops, either symmetrically (50%/50%, 100%/100%) or asymmetrically (50%/100%, 100%/50%).

| Test Case | Client Drop (%) | Server Drop (%) | Client Delay (%) | Server Delay (%) | Delay Time (ms) | Description                         |
|-----------|-----------------|-----------------|------------------|------------------|-----------------|-------------------------------------|
| 8         | 50              | 0               | 0                | 0                | 0               | 50% drop on client only             |
| 9         | 100             | 0               | 0                | 0                | 0               | 100% drop on client only            |
| 10        | 0               | 50              | 0                | 0                | 0               | 50% drop on server only             |
| 11        | 0               | 100             | 0                | 0                | 0               | 100% drop on server only            |
| 12        | 50              | 50              | 0                | 0                | 0               | 50% drop on both client and server  |
| 13        | 100             | 50              | 0                | 0                | 0               | 100% client drop, 50% server drop   |
| 14        | 50              | 100             | 0                | 0                | 0               | 50% client drop, 100% server drop   |
| 15        | 100             | 100             | 0                | 0                | 0               | 100% drop on both client and server |

---

### **3. Client Drop + Delay Configurations**

This table combines client-side drop and delay probabilities to observe how packet loss and latency interact for the
client.

- **Client Drop with Delay (Test Cases 16-19):** Includes combinations of 50% and 100% probabilities for both drop and
  delay on the client side, while the server is unaffected.

| Test Case | Client Drop (%) | Server Drop (%) | Client Delay (%) | Server Delay (%) | Delay Time (ms)       | Description                      |
|-----------|-----------------|-----------------|------------------|------------------|-----------------------|----------------------------------|
| 16        | 50              | 0               | 50               | 0                | 100-500 (client-side) | 50% drop + 50% delay on client   |
| 17        | 50              | 0               | 100              | 0                | 100-500 (client-side) | 50% drop + 100% delay on client  |
| 18        | 100             | 0               | 50               | 0                | 100-500 (client-side) | 100% drop + 50% delay on client  |
| 19        | 100             | 0               | 100              | 0                | 100-500 (client-side) | 100% drop + 100% delay on client |

---

### **4. Server Drop + Delay Configurations**

This table combines server-side drop and delay probabilities to analyze how these factors affect server behavior
independently.

- **Server Drop with Delay (Test Cases 20-23):** Includes combinations of 50% and 100% probabilities for both drop and
  delay on the server side, while the client is unaffected.

| Test Case | Client Drop (%) | Server Drop (%) | Client Delay (%) | Server Delay (%) | Delay Time (ms)       | Description                      |
|-----------|-----------------|-----------------|------------------|------------------|-----------------------|----------------------------------|
| 20        | 0               | 50              | 0                | 50               | 200-600 (server-side) | 50% drop + 50% delay on server   |
| 21        | 0               | 50              | 0                | 100              | 200-600 (server-side) | 50% drop + 100% delay on server  |
| 22        | 0               | 100             | 0                | 50               | 200-600 (server-side) | 100% drop + 50% delay on server  |
| 23        | 0               | 100             | 0                | 100              | 200-600 (server-side) | 100% drop + 100% delay on server |

---

### **5. Combined Client and Server Drop + Delay Configurations**

This table explores the interaction between drop and delay probabilities across both the client and server
simultaneously.

- **Symmetric Configurations (Test Case 24):** Both client and server experience 50% drop and delay probabilities,
  testing equal conditions on both ends.
- **Asymmetric Configurations (Test Cases 25, 26):** The client experiences 100% drop and delay, while the server
  experiences 50%, and vice versa, testing unbalanced conditions.
- **Maximum Stress Configuration (Test Case 27):** Both client and server experience 100% drop and delay probabilities,
  simulating the most challenging scenario.

| Test Case | Client Drop (%) | Server Drop (%) | Client Delay (%) | Server Delay (%) | Delay Time (ms)                              | Description                                       |
|-----------|-----------------|-----------------|------------------|------------------|----------------------------------------------|---------------------------------------------------|
| 24        | 50              | 50              | 50               | 50               | 100-500 (client-side), 200-600 (server-side) | 50% drop and delay on both client and server      |
| 25        | 100             | 50              | 100              | 50               | 100-500 (client-side), 200-600 (server-side) | 100% client drop + delay, 50% server drop + delay |
| 26        | 50              | 100             | 50               | 100              | 100-500 (client-side), 200-600 (server-side) | 50% client drop + delay, 100% server drop + delay |
| 27        | 100             | 100             | 100              | 100              | 100-500 (client-side), 200-600 (server-side) | 100% drop and delay on both client and server     |

---

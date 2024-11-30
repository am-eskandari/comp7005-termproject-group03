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

## **1. Base Case (No Drop or Delay)**

This section serves as the control test, verifying the functionality of the system under ideal conditions with no drop
or delay configurations.

| Test Case | Client Drop (%) | Server Drop (%) | Client Delay (%) | Server Delay (%) | Delay Time (ms) | Description                  |
|-----------|-----------------|-----------------|------------------|------------------|-----------------|------------------------------|
| 1         | 0               | 0               | 0                | 0                | 0               | No drop or delay (Base Case) |

---

## **2. Delay Configurations (No Drop)**

This section explores the impact of delay configurations on the client and server, including various combinations of
delay probabilities.

#### **Client Delay Only**

- **Test Case 2:** 50% delay probability on the client side, server unaffected.
- **Test Case 5:** 100% delay probability on the client side, server unaffected.

#### **Server Delay Only**

- **Test Case 3:** 50% delay probability on the server side, client unaffected.
- **Test Case 6:** 100% delay probability on the server side, client unaffected.

#### **Combined Client and Server Delay**

- **Test Case 4:** 50% delay probability on both client and server sides.
- **Test Case 7:** 100% delay probability on both client and server sides.

#### **Mixed Client and Server Delay**

- **Test Case 8:** 50% delay on the client side and 100% delay on the server side.
- **Test Case 9:** 100% delay on the client side and 50% delay on the server side.

| Test Case | Client Drop (%) | Server Drop (%) | Client Delay (%) | Server Delay (%) | Delay Time (ms)                              | Description                          |
|-----------|-----------------|-----------------|------------------|------------------|----------------------------------------------|--------------------------------------|
| 2         | 0               | 0               | 50               | 0                | 100-500 (client-side)                        | 50% delay on client only             |
| 3         | 0               | 0               | 0                | 50               | 200-600 (server-side)                        | 50% delay on server only             |
| 4         | 0               | 0               | 50               | 50               | 100-500 (client-side), 200-600 (server-side) | 50% delay on both client and server  |
| 5         | 0               | 0               | 100              | 0                | 100-500 (client-side)                        | 100% delay on client only            |
| 6         | 0               | 0               | 0                | 100              | 200-600 (server-side)                        | 100% delay on server only            |
| 7         | 0               | 0               | 100              | 100              | 100-500 (client-side), 200-600 (server-side) | 100% delay on both client and server |
| 8         | 0               | 0               | 50               | 100              | 100-500 (client-side), 200-600 (server-side) | 50% delay on client, 100% on server  |
| 9         | 0               | 0               | 100              | 50               | 100-500 (client-side), 200-600 (server-side) | 100% delay on client, 50% on server  |

---

## **3. Drop Configurations (No Delay)**

This section explores the effects of packet drops without any delay interference.

- **Client Drop Only (Test Cases 10, 11):** Examines the impact of 50% and 100% packet drop probabilities on the client
  side, with the server unaffected.
- **Server Drop Only (Test Cases 12, 13):** Evaluates the impact of 50% and 100% packet drop probabilities on the server
  side, with the client unaffected.
- **Combined Client and Server Drop (Test Cases 14-17):** Tests scenarios where both client and server experience packet
  drops, either symmetrically (50%/50%, 100%/100%) or asymmetrically (50%/100%, 100%/50%).

| Test Case | Client Drop (%) | Server Drop (%) | Client Delay (%) | Server Delay (%) | Delay Time (ms) | Description                         |
|-----------|-----------------|-----------------|------------------|------------------|-----------------|-------------------------------------|
| 10        | 50              | 0               | 0                | 0                | 0               | 50% drop on client only             |
| 11        | 100             | 0               | 0                | 0                | 0               | 100% drop on client only            |
| 12        | 0               | 50              | 0                | 0                | 0               | 50% drop on server only             |
| 13        | 0               | 100             | 0                | 0                | 0               | 100% drop on server only            |
| 14        | 50              | 50              | 0                | 0                | 0               | 50% drop on both client and server  |
| 15        | 100             | 50              | 0                | 0                | 0               | 100% client drop, 50% server drop   |
| 16        | 50              | 100             | 0                | 0                | 0               | 50% client drop, 100% server drop   |
| 17        | 100             | 100             | 0                | 0                | 0               | 100% drop on both client and server |

--- 

## **4. Client Drop + Delay Configurations**

This section explores the combined effects of client-side drop and delay probabilities to analyze how packet loss and
latency interact on the client side.

- **Client Drop with Delay (Test Cases 18-21):** Includes combinations of 50% and 100% probabilities for both drop and
  delay on the client side, while the server remains unaffected.

| Test Case | Client Drop (%) | Server Drop (%) | Client Delay (%) | Server Delay (%) | Delay Time (ms)       | Description                      |
|-----------|-----------------|-----------------|------------------|------------------|-----------------------|----------------------------------|
| 18        | 50              | 0               | 50               | 0                | 100-500 (client-side) | 50% drop + 50% delay on client   |
| 19        | 50              | 0               | 100              | 0                | 100-500 (client-side) | 50% drop + 100% delay on client  |
| 20        | 100             | 0               | 50               | 0                | 100-500 (client-side) | 100% drop + 50% delay on client  |
| 21        | 100             | 0               | 100              | 0                | 100-500 (client-side) | 100% drop + 100% delay on client |

---

## **5. Server Drop + Delay Configurations**

This section examines the combined effects of server-side drop and delay probabilities to understand how these factors
affect server behavior independently.

- **Server Drop with Delay (Test Cases 22-25):** Includes combinations of 50% and 100% probabilities for both drop and
  delay on the server side, while the client remains unaffected.

| Test Case | Client Drop (%) | Server Drop (%) | Client Delay (%) | Server Delay (%) | Delay Time (ms)       | Description                      |
|-----------|-----------------|-----------------|------------------|------------------|-----------------------|----------------------------------|
| 22        | 0               | 50              | 0                | 50               | 200-600 (server-side) | 50% drop + 50% delay on server   |
| 23        | 0               | 50              | 0                | 100              | 200-600 (server-side) | 50% drop + 100% delay on server  |
| 24        | 0               | 100             | 0                | 50               | 200-600 (server-side) | 100% drop + 50% delay on server  |
| 25        | 0               | 100             | 0                | 100              | 200-600 (server-side) | 100% drop + 100% delay on server |

---

## **6. Combined Client and Server Drop + Delay Configurations**

This section explores the interaction between drop and delay probabilities across both the client and server
simultaneously, ensuring thorough testing of symmetric and asymmetric conditions.

- **Symmetric Configurations:** Both client and server experience identical drop and delay probabilities (e.g., 50% drop
  and 50% delay).
- **Asymmetric Configurations:** The client and server experience differing drop and delay probabilities, such as 100%
  client drop + delay and 50% server drop + delay.
- **Maximum Stress Configuration:** Both client and server experience 100% drop and 100% delay probabilities, simulating
  the most challenging scenario.

| Test Case | Client Drop (%) | Server Drop (%) | Client Delay (%) | Server Delay (%) | Delay Time (ms)                              | Description                                          |
|-----------|-----------------|-----------------|------------------|------------------|----------------------------------------------|------------------------------------------------------|
| 26        | 50              | 50              | 50               | 50               | 100-500 (client-side), 200-600 (server-side) | 50% drop and delay on both client and server         |
| 27        | 100             | 50              | 100              | 50               | 100-500 (client-side), 200-600 (server-side) | 100% client drop + delay, 50% server drop + delay    |
| 28        | 50              | 100             | 50               | 100              | 100-500 (client-side), 200-600 (server-side) | 50% client drop + delay, 100% server drop + delay    |
| 29        | 100             | 100             | 100              | 100              | 100-500 (client-side), 200-600 (server-side) | 100% drop and delay on both client and server        |
| 30        | 50              | 0               | 50               | 100              | 100-500 (client-side), 200-600 (server-side) | 50% client drop + delay, server delay only           |
| 31        | 0               | 50              | 100              | 50               | 100-500 (client-side), 200-600 (server-side) | Server drop + delay, client delay only               |
| 32        | 50              | 100             | 100              | 0                | 100-500 (client-side)                        | 50% client drop, 100% client delay, server drop only |
| 33        | 100             | 50              | 0                | 100              | 200-600 (server-side)                        | 100% server drop, 50% server delay, client drop only |
| 34        | 50              | 100             | 50               | 0                | 100-500 (client-side)                        | 50% client drop, server drop only                    |
| 35        | 0               | 50              | 50               | 50               | 100-500 (client-side), 200-600 (server-side) | Client delay + server drop and delay                 |
| 36        | 50              | 0               | 100              | 50               | 100-500 (client-side), 200-600 (server-side) | Client drop + delay, server delay only               |

---

## **7. Additional Delay Time Test Cases**

This section focuses on specific delay time configurations to evaluate the protocol's behavior under edge cases related
to fixed and extended delay times.

### **7.1 Fixed Delay Time Test**

This test sets a fixed delay time of **500 ms** on either the client or server side, instead of an interval, to evaluate
the protocol's handling of consistent delay.

| Test Case | Client Drop (%) | Server Drop (%) | Client Delay (%) | Server Delay (%) | Delay Time (ms) | Description                  |
|-----------|-----------------|-----------------|------------------|------------------|-----------------|------------------------------|
| 37        | 0               | 0               | 50               | 0                | 500             | Fixed 500 ms delay on client |
| 38        | 0               | 0               | 0                | 50               | 500             | Fixed 500 ms delay on server |

---

### **7.2 Extended Delay Beyond Retry Timeout**

This test sets a delay longer than the client's retry timeout to evaluate how the protocol handles extreme delay
scenarios.

| Test Case | Client Drop (%) | Server Drop (%) | Client Delay (%) | Server Delay (%) | Delay Time (ms) | Description                                 |
|-----------|-----------------|-----------------|------------------|------------------|-----------------|---------------------------------------------|
| 39        | 0               | 0               | 100              | 0                | 2000            | Client delay beyond retry timeout           |
| 40        | 0               | 0               | 0                | 100              | 2000            | Server delay beyond retry timeout           |
| 41        | 0               | 0               | 100              | 100              | 2000            | Both client and server delay beyond timeout |

---


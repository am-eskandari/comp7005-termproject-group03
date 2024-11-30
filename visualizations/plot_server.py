import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
data = pd.read_csv("../data/log_server.csv")

# Convert the timestamp to datetime for easier grouping and plotting
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Add a second-level time grouping
data['Second'] = data['Timestamp'].dt.floor('s')  # Use lowercase 's' to avoid warnings

# Count events per second for different categories
events_per_second = data.groupby(['Second', 'Event']).size().unstack(fill_value=0)

# Ensure all event types are present
received = events_per_second.get('Received', pd.Series(0, index=events_per_second.index))
out_of_order = events_per_second.get('Out-of-Order', pd.Series(0, index=events_per_second.index))

# Compute latency (mean latency per second)
latency = data[data['Latency (ms)'].notnull()].groupby('Second')['Latency (ms)'].mean()

# Plot Received and Out-of-Order packets
plt.figure(figsize=(10, 6))
plt.plot(received.index, received.values, label='Received Packets', marker='o', color='blue')
plt.plot(out_of_order.index, out_of_order.values, label='Out-of-Order Packets', marker='x', color='orange')
plt.title('Received and Out-of-Order Packets Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Packets per Second')
plt.legend()
plt.grid()
plt.show()

# Plot Latency
plt.figure(figsize=(10, 6))
plt.plot(latency.index, latency.values, label='Latency (ms)', marker='o', color='purple')
plt.title('Latency Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Latency (ms)')
plt.legend()
plt.grid()
plt.show()

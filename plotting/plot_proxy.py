import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
data = pd.read_csv("../log_proxy.csv")

# Convert the timestamp to datetime for easier grouping and plotting
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Add a second-level time grouping
data['Second'] = data['Timestamp'].dt.floor('s')  # Use lowercase 's'

# Count events per second for different categories
events_per_second = data.groupby(['Second', 'Event']).size().unstack(fill_value=0)

# Ensure all event types are present
forwarded = events_per_second.get('Forwarded', pd.Series(0, index=events_per_second.index))
dropped = events_per_second.get('Dropped', pd.Series(0, index=events_per_second.index))
duplicate = events_per_second.get('Duplicate', pd.Series(0, index=events_per_second.index))

# Compute mean latency (ms) per second
latency = data[data['Latency (ms)'].notnull()].groupby('Second')['Latency (ms)'].mean()

# Compute mean delay time (ms) per second
delay_time = data[data['Delay Time (ms)'] > 0].groupby('Second')['Delay Time (ms)'].mean()

# Plot Forwarded, Dropped, and Duplicate packets
plt.figure(figsize=(10, 6))
plt.plot(forwarded.index, forwarded.values, label='Forwarded Packets', marker='o', color='green')
plt.plot(dropped.index, dropped.values, label='Dropped Packets', marker='x', color='red')
plt.plot(duplicate.index, duplicate.values, label='Duplicate Packets', marker='^', color='orange')
plt.title('Packet Events Over Time')
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

# Plot Delay Time
plt.figure(figsize=(10, 6))
plt.plot(delay_time.index, delay_time.values, label='Delay Time (ms)', marker='o', color='blue')
plt.title('Delay Time Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Delay Time (ms)')
plt.legend()
plt.grid()
plt.show()

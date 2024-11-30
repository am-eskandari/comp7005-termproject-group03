import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
data = pd.read_csv("../data/log_client.csv")

# Convert the timestamp to datetime for easier grouping and plotting
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Add a second-level time grouping
data['Second'] = data['Timestamp'].dt.floor('s')  # Use lowercase 's'

# Count events per second for different categories
events_per_second = data.groupby(['Second', 'Event']).size().unstack(fill_value=0)

# Ensure all event types are properly initialized
sent = events_per_second['Sent'] if 'Sent' in events_per_second else pd.Series(0, index=events_per_second.index)
acknowledged = events_per_second['Acknowledged'] if 'Acknowledged' in events_per_second else pd.Series(0, index=events_per_second.index)
retransmit = events_per_second['Retransmit'] if 'Retransmit' in events_per_second else pd.Series(0, index=events_per_second.index)
failed = events_per_second['Failed'] if 'Failed' in events_per_second else pd.Series(0, index=events_per_second.index)

# Compute latency (mean latency per second)
latency = data[data['Latency (ms)'].notnull()].groupby('Second')['Latency (ms)'].mean()

# Plot Sent and Acknowledged packets
plt.figure(figsize=(10, 6))
plt.plot(sent.index, sent.values, label='Sent Packets', marker='o', color='blue')
plt.plot(acknowledged.index, acknowledged.values, label='Acknowledged Packets', marker='x', color='green')
plt.title('Packets Sent and Acknowledged Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Packets per Second')
plt.legend()
plt.grid()
plt.show()

# Plot Retransmitted and Failed packets
plt.figure(figsize=(10, 6))
plt.plot(retransmit.index, retransmit.values, label='Retransmitted Packets', marker='o', color='orange')
plt.plot(failed.index, failed.values, label='Failed Packets', marker='x', color='red')
plt.title('Retransmitted and Failed Packets Over Time')
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

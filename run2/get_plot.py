import os
import re
import pandas as pd
import matplotlib.pyplot as plt

# Initialize lists to store data from each file
data = []

# Define the pattern to extract relevant values from the log files
pattern = r"Threads:\s+(\d+).*?Block size:\s+(\d+).*?Total size:\s+([\d.]+)\s+GB.*?CPU\s:\s+([\d.]+).*?DSA\s:\s+([\d.]+).*?CPU Prefault\(latency\):\s+([\d.]+).*?CPU Prefault\(BW\):\s+([\d.]+).*?DSA Prefault\(latency\):\s+([\d.]+).*?DSA Prefault\(BW\):\s+([\d.]+)"

# Iterate over each file in the current directory
for filename in os.listdir("."):
    if filename.endswith(".log"):  # Assumes log files have a .txt extension
        with open(filename, 'r') as file:
            content = file.read()
            match = re.search(pattern, content, re.DOTALL)
            if match:
                # Extract data from the regex groups
                threads, block_size, total_size, cpu_perf, dsa_perf, cpu_latency, cpu_bw, dsa_latency, dsa_bw = match.groups()
                
                # Append data to list
                data.append({
                    "Threads": int(threads),
                    "Block Size (B)": int(block_size),
                    "Total Size (GB)": float(total_size),
                    "CPU Performance (GB/s)": float(cpu_perf),
                    "DSA Performance (GB/s)": float(dsa_perf),
                    "CPU Latency": float(cpu_latency),
                    "DSA Latency": float(dsa_latency),
                    "CPU Bandwidth (GB/s)": float(cpu_bw),
                    "DSA Bandwidth (GB/s)": float(dsa_bw),
                })

# Convert the data list to a pandas DataFrame
df = pd.DataFrame(data)

print(len(df))

# Plot CPU and DSA Performance
plt.figure(figsize=(10, 5))
plt.plot(df["Threads"], df["CPU Performance (GB/s)"], label="CPU Performance (GB/s)", marker='o')
plt.plot(df["Threads"], df["DSA Performance (GB/s)"], label="DSA Performance (GB/s)", marker='o')
plt.xlabel("Threads")
plt.ylabel("Performance (GB/s)")
plt.title("CPU vs DSA Performance")
plt.legend()
plt.savefig("cpu_dsa_performance.png")

# Plot CPU and DSA Latency
plt.figure(figsize=(10, 5))
plt.plot(df["Threads"], df["CPU Latency"], label="CPU Latency", marker='o')
plt.plot(df["Threads"], df["DSA Latency"], label="DSA Latency", marker='o')
plt.xlabel("Threads")
plt.ylabel("Latency")
plt.title("CPU vs DSA Latency")
plt.legend()
plt.savefig("cpu_dsa_latency.png")

# Plot CPU and DSA Bandwidth
plt.figure(figsize=(10, 5))
plt.plot(df["Threads"], df["CPU Bandwidth (GB/s)"], label="CPU Bandwidth (GB/s)", marker='o')
plt.plot(df["Threads"], df["DSA Bandwidth (GB/s)"], label="DSA Bandwidth (GB/s)", marker='o')
plt.xlabel("Threads")
plt.ylabel("Bandwidth (GB/s)")
plt.title("CPU vs DSA Bandwidth")
plt.legend()
plt.savefig("cpu_dsa_bandwidth.png")

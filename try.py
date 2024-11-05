import os
import re
import pandas as pd
import matplotlib.pyplot as plt

# Define regex patterns for extracting CPU and DSA latency and bandwidth from the logs
cpu_latency_pattern = r"CPU\s*Prefault\(latency\):\s*([\d.]+)"
cpu_bw_pattern = r"CPU\s*Prefault\(BW\):\s*([\d.]+)\(GB/s\)"
dsa_latency_pattern = r"DSA\s*Prefault\(latency\):\s*([\d.]+)"
dsa_bw_pattern = r"DSA\s*Prefault\(BW\):\s*([\d.]+)\(GB/s\)"

# Initialize dictionaries to collect data for different configurations and operations
latency_data = {
    "write": {
        "DSA-1thread": [],
        "DSA-4threads": [],
        "CPU-1thread": [],
        "CPU-4threads": []
    },
    "read": {
        "DSA-1thread": [],
        "DSA-4threads": [],
        "CPU-1thread": [],
        "CPU-4threads": []
    }
}
throughput_data = {
    "write": {
        "DSA-1thread": [],
        "DSA-4threads": [],
        "CPU-1thread": [],
        "CPU-4threads": []
    },
    "read": {
        "DSA-1thread": [],
        "DSA-4threads": [],
        "CPU-1thread": [],
        "CPU-4threads": []
    }
}

# Initialize list for test cases
test_cases = []

# Process each log file in the directory
filenames = os.listdir('./run1')
filenames = [filename for filename in filenames if filename.endswith('.log')]
filenames.sort(key=lambda x: int(re.search(r"latency_(\d+)_", x).group(1)))
print(filenames)
for filename in filenames:
    if filename.endswith('.log'):
        # Determine configuration and operation (read or write) based on filename
        if "_nthreads_1" in filename:
            if "_d_r" in filename:
                config = "-1thread"
                operation = "write"
            else:
                config = "-1thread"
                operation = "read"
        elif "_nthreads_4" in filename:
            if "_d_r" in filename:
                config = "-4threads"
                operation = "write"
            else:
                config = "-4threads"
                operation = "read"
        else:
            print(f"Warning: Unknown configuration in filename {filename}")
            continue  # Skip files that don't match the expected pattern

        # Set block size based on file naming convention (assumed)
        block_size = 4096 if "4096" in filename else 8192

        # Extract the test case (e.g., 399, 766) from the filename
        test_case_match = re.search(r"latency_(\d+)_", filename)
        if test_case_match:
            test_case = int(test_case_match.group(1))
            if test_case not in test_cases:
                test_cases.append(test_case)

        # Read file content
        with open("run1/"+filename, 'r') as file1, open("run2/"+filename, 'r') as file2:
            log_data1 = file1.read()
            log_data2 = file2.read()

            # Extract CPU and DSA latency and bandwidth values using regex
            cpu_latency_match1 = re.search(cpu_latency_pattern, log_data1)
            cpu_bw_match1 = re.search(cpu_bw_pattern, log_data1)
            dsa_latency_match1 = re.search(dsa_latency_pattern, log_data1)
            dsa_bw_match1 = re.search(dsa_bw_pattern, log_data1)

            cpu_latency_match2 = re.search(cpu_latency_pattern, log_data2)
            cpu_bw_match2 = re.search(cpu_bw_pattern, log_data2)
            dsa_latency_match2 = re.search(dsa_latency_pattern, log_data2)
            dsa_bw_match2 = re.search(dsa_bw_pattern, log_data2)


            # Check for CPU latency and bandwidth matches
            if cpu_latency_match1 and cpu_bw_match1:
                cpu_latency_value = float(cpu_latency_match1.group(1)) + float(cpu_latency_match2.group(1)) / 2
                cpu_bandwidth_value = float(cpu_bw_match1.group(1)) + float(cpu_bw_match2.group(1)) / 2
            else:
                print(f"Warning: Missing CPU latency or bandwidth data in {filename}")
                cpu_latency_value = None
                cpu_bandwidth_value = None

            # Check for DSA latency and bandwidth matches
            if dsa_latency_match1 and dsa_bw_match1:
                dsa_latency_value = float(dsa_latency_match1.group(1)) + float(dsa_latency_match2.group(1)) / 2
                dsa_bandwidth_value = float(dsa_bw_match1.group(1)) + float(dsa_bw_match2.group(1)) / 2
            else:
                print(f"Warning: Missing DSA latency or bandwidth data in {filename}")
                dsa_latency_value = None
                dsa_bandwidth_value = None

            # Append values to lists if latency data was found
            if cpu_latency_value is not None and cpu_bandwidth_value is not None:
                latency_data[operation]["CPU"+config].append(cpu_latency_value)
                throughput_data[operation]["CPU"+config].append((cpu_bandwidth_value * 1024 * 1024) / block_size)
            if dsa_latency_value is not None and dsa_bandwidth_value is not None:
                latency_data[operation]["DSA"+config].append(dsa_latency_value)
                throughput_data[operation]["DSA"+config].append((dsa_bandwidth_value * 1024 * 1024) / block_size)

# Sort test cases for consistent plotting
test_cases
print(test_cases)
# Continue with creating DataFrames and plotting as previously outlined
# For latency and throughput plots separated by read and write

# print all the lengths of the lists
print(latency_data)
print(len(latency_data["write"]["DSA-1thread"]))
print(len(latency_data["write"]["DSA-4threads"]))
print(len(latency_data["write"]["CPU-1thread"]))
print(len(latency_data["write"]["CPU-4threads"]))

# Create DataFrames for latency and throughput, separated by read and write operations
latency_write_df = pd.DataFrame({
    "Test Case": test_cases,
    "DSA-1thread": latency_data["write"]["DSA-1thread"],
    "DSA-4threads": latency_data["write"]["DSA-4threads"],
    "CPU-1thread": latency_data["write"]["CPU-1thread"],
    "CPU-4threads": latency_data["write"]["CPU-4threads"]
})
latency_read_df = pd.DataFrame({
    "Test Case": test_cases,
    "DSA-1thread": latency_data["read"]["DSA-1thread"],
    "DSA-4threads": latency_data["read"]["DSA-4threads"],
    "CPU-1thread": latency_data["read"]["CPU-1thread"],
    "CPU-4threads": latency_data["read"]["CPU-4threads"]
})
throughput_write_df = pd.DataFrame({
    "Test Case": test_cases,
    "DSA-1thread": throughput_data["write"]["DSA-1thread"],
    "DSA-4threads": throughput_data["write"]["DSA-4threads"],
    "CPU-1thread": throughput_data["write"]["CPU-1thread"],
    "CPU-4threads": throughput_data["write"]["CPU-4threads"]
})
throughput_read_df = pd.DataFrame({
    "Test Case": test_cases,
    "DSA-1thread": throughput_data["read"]["DSA-1thread"],
    "DSA-4threads": throughput_data["read"]["DSA-4threads"],
    "CPU-1thread": throughput_data["read"]["CPU-1thread"],
    "CPU-4threads": throughput_data["read"]["CPU-4threads"]
})

# Plotting code continues here as in the previous example

# Plot latency and throughput for read and write separately
plt.figure(figsize=(18, 12))

# Write Latency Plot
plt.subplot(2, 2, 1)
plt.plot(latency_write_df['Test Case'], latency_write_df['DSA-1thread'], label='DSA-1thread', marker='o', color='blue')
plt.plot(latency_write_df['Test Case'], latency_write_df['DSA-4threads'], label='DSA-4threads', marker='o', color='orange')
plt.plot(latency_write_df['Test Case'], latency_write_df['CPU-1thread'], label='CPU-1thread', marker='o', color='gray')
plt.plot(latency_write_df['Test Case'], latency_write_df['CPU-4threads'], label='CPU-4threads', marker='o', color='yellow')
plt.xlabel('Test Cases')
plt.ylabel('Latency (ms)')
plt.title('Write Latency Comparison')
plt.legend()

# Read Latency Plot
plt.subplot(2, 2, 2)
plt.plot(latency_read_df['Test Case'], latency_read_df['DSA-1thread'], label='DSA-1thread', marker='o', color='blue')
plt.plot(latency_read_df['Test Case'], latency_read_df['DSA-4threads'], label='DSA-4threads', marker='o', color='orange')
plt.plot(latency_read_df['Test Case'], latency_read_df['CPU-1thread'], label='CPU-1thread', marker='o', color='gray')
plt.plot(latency_read_df['Test Case'], latency_read_df['CPU-4threads'], label='CPU-4threads', marker='o', color='yellow')
plt.xlabel('Test Cases')
plt.ylabel('Latency (ms)')
plt.title('Read Latency Comparison')
plt.legend()

# Write Throughput Plot
plt.subplot(2, 2, 3)
plt.plot(throughput_write_df['Test Case'], throughput_write_df['DSA-1thread'], label='DSA-1thread', marker='o', color='blue')
plt.plot(throughput_write_df['Test Case'], throughput_write_df['DSA-4threads'], label='DSA-4threads', marker='o', color='orange')
plt.plot(throughput_write_df['Test Case'], throughput_write_df['CPU-1thread'], label='CPU-1thread', marker='o', color='gray')
plt.plot(throughput_write_df['Test Case'], throughput_write_df['CPU-4threads'], label='CPU-4threads', marker='o', color='yellow')
plt.xlabel('Test Cases')
plt.ylabel('Throughput (OPS)')
plt.title('Write Throughput Comparison')
plt.legend()

# Read Throughput Plot
plt.subplot(2, 2, 4)
plt.plot(throughput_read_df['Test Case'], throughput_read_df['DSA-1thread'], label='DSA-1thread', marker='o', color='blue')
plt.plot(throughput_read_df['Test Case'], throughput_read_df['DSA-4threads'], label='DSA-4threads', marker='o', color='orange')
plt.plot(throughput_read_df['Test Case'], throughput_read_df['CPU-1thread'], label='CPU-1thread', marker='o', color='gray')
plt.plot(throughput_read_df['Test Case'], throughput_read_df['CPU-4threads'], label='CPU-4threads', marker='o', color='yellow')
plt.xlabel('Test Cases')
plt.ylabel('Throughput (OPS)')
plt.title('Read Throughput Comparison')
plt.legend()

plt.tight_layout()
plt.show()
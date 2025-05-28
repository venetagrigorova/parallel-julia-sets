#!/usr/bin/env python3
import subprocess
import csv
from statistics import mean
import matplotlib.pyplot as plt

THREADS = [1, 2, 4, 8, 16, 24, 32]
OUTPUT_CSV = "weak_scaling_results.csv"
PLOT_FILE = "weak_scaling_plot.png"

def run_filter(p, r):
    times = []
    for _ in range(3):
        result = subprocess.run(
            ["./bin/filter_runner", "-i", "./contrib/input1.png", "-p", str(p), "-r", str(r)],
            capture_output=True, text=True
        )
        try:
            time = float(result.stdout.strip().split(",")[3])
            times.append(time)
        except Exception as e:
            print(f"Error parsing output: {result.stdout}")
            times.append(None)
    return times

results = []

with open(OUTPUT_CSV, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Threads", "Rounds", "Run1", "Run2", "Run3", "Min Time", "Avg Time"])

    for p in THREADS:
        r = p  # weak scaling: r = p
        print(f"Running filter with {p} threads and {r} rounds...")
        times = run_filter(p, r)
        valid_times = [t for t in times if t is not None]
        min_time = min(valid_times)
        avg_time = mean(valid_times)
        writer.writerow([p, r] + times + [min_time, avg_time])
        results.append((p, min_time))

# Plotting
x, y = zip(*results)
plt.figure(figsize=(8, 5))
plt.plot(x, y, marker='o')
plt.title("Weak Scaling Performance")
plt.xlabel("Number of Threads (Rounds = Threads)")
plt.ylabel("Min Execution Time (s)")
plt.grid(True)
plt.savefig(PLOT_FILE)
print(f"Plot saved as {PLOT_FILE}")

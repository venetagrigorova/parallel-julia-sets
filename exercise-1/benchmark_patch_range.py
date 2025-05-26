import subprocess
import statistics
import csv

size = 850
nprocs = 24
patch_range = range(1, 41)  
repeats = 3

results = []

print(f"Benchmarking patch sizes from 1 to 40 with size={size} and nprocs={nprocs}...\n")

for patch in patch_range:
    runtimes = []
    print(f"Running patch size = {patch}...")
    for i in range(repeats):
        try:
            output = subprocess.check_output([
                "python3", "julia_par.py",
                "--size", str(size),
                "--nprocs", str(nprocs),
                "--patch", str(patch)
            ]).decode().strip()
            runtime = float(output.split(";")[-1])
            runtimes.append(runtime)
            print(f"  Run {i+1}: {runtime:.4f}s")
        except Exception as e:
            print(f"   Error running patch {patch} run {i+1}: {e}")
            runtimes.append(None)
    
    if None not in runtimes:
        mean_runtime = statistics.mean(runtimes)
        results.append((patch, *runtimes, mean_runtime))
    else:
        results.append((patch, *runtimes, "ERROR"))

print("\n Benchmark complete.\n")

# Optional: save to CSV
with open("results/patch_range_850.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["patch", "run1", "run2", "run3", "mean"])
    writer.writerows(results)

print(" Results saved to results/patch_range_850.csv")

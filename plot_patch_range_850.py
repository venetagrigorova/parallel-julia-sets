import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("results/patch_range_850.csv")


patch_sizes = df["patch"]
mean_runtimes = df["mean"]


plt.figure(figsize=(10, 5))
plt.plot(patch_sizes, mean_runtimes, marker='o')
plt.title("Patch Size vs Runtime (size=850, nprocs=24)")
plt.xlabel("Patch Size")
plt.ylabel("Mean Runtime (s)")
plt.grid(True)


plt.savefig("plots/patch_vs_runtime_850.png", dpi=300)
plt.show()

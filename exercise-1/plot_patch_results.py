import matplotlib.pyplot as plt


patch_sizes = [1, 5, 10, 20, 55, 150, 400]
mean_runtimes = [112.21, 4.08, 1.68, 1.12, 1.06, 1.32, 2.07]


plt.figure(figsize=(8, 5))
plt.plot(patch_sizes, mean_runtimes, marker='o')
plt.title("Patch Size vs Runtime (size=1000, p=32)")
plt.xlabel("Patch Size")
plt.ylabel("Mean Runtime (s)")
plt.grid(True)
plt.tight_layout()


plt.savefig("plots/patch_vs_runtime.png", dpi=300)
plt.show()
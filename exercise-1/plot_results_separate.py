import pandas as pd
import matplotlib.pyplot as plt
import os

# load results
df = pd.read_csv('results.csv')

# make sure nprocs is integer
df['nprocs'] = df['nprocs'].astype(int)

# create output folders
folders = ["plots/runtime", "plots/speedup", "plots/efficiency"]
for folder in folders:
    os.makedirs(folder, exist_ok=True)


for size in df['size'].unique():
    for mode in df['mode'].unique():
        df_filtered = df[(df['size'] == size) & (df['mode'] == mode)]

        # only average the runtime column
        df_grouped = df_filtered.groupby('nprocs')[['runtime']].mean().reset_index()

        # plot runtime
        plt.figure()
        plt.plot(df_grouped['nprocs'], df_grouped['runtime'], marker='o')
        plt.xlabel('Number of Processes')
        plt.ylabel('Mean Runtime (s)')
        plt.title(f'Runtime vs Processes ({size}x{size}, {mode})')
        plt.grid(True)
        plt.savefig(f'plots/runtime/runtime_{size}_{mode}.png')
        plt.close()

        # plot speed-up
        base_time = df_grouped[df_grouped['nprocs'] == 1]['runtime'].values[0]
        speedup = base_time / df_grouped['runtime']

        plt.figure()
        plt.plot(df_grouped['nprocs'], speedup, marker='o')
        plt.xlabel('Number of Processes')
        plt.ylabel('Speed-up')
        plt.title(f'Speed-up vs Processes ({size}x{size}, {mode})')
        plt.grid(True)
        plt.savefig(f'plots/speedup/speedup_{size}_{mode}.png')
        plt.close()

        # plot efficiency
        efficiency = (speedup / df_grouped['nprocs']) * 100

        plt.figure()
        plt.plot(df_grouped['nprocs'], efficiency, marker='o')
        plt.xlabel('Number of Processes')
        plt.ylabel('Efficiency (%)')
        plt.title(f'Efficiency vs Processes ({size}x{size}, {mode})')
        plt.grid(True)
        plt.savefig(f'plots/efficiency/efficiency_{size}_{mode}.png')
        plt.close()

print("All plots finished.")

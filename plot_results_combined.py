import pandas as pd
import matplotlib.pyplot as plt
import os

# load results
df = pd.read_csv('results.csv')

# make sure nprocs is integer
df['nprocs'] = df['nprocs'].astype(int)

# create output folder
os.makedirs("plots/combined", exist_ok=True)

# loop over modes (cs and cb)
for mode in df['mode'].unique():
    df_mode = df[df['mode'] == mode]

    # --- plot 1: runtime vs processes ---
    plt.figure()
    for size in df_mode['size'].unique():
        df_size = df_mode[df_mode['size'] == size]
        df_grouped = df_size.groupby('nprocs')[['runtime']].mean().reset_index()
        plt.plot(df_grouped['nprocs'], df_grouped['runtime'], marker='o', label=f'size={size}')
    plt.xlabel('Number of Processes')
    plt.ylabel('Mean Runtime (s)')
    plt.title(f'Runtime vs Processes ({mode})')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'plots/combined/runtime_{mode}.png')
    plt.close()

    # --- plot 2: speed-up vs processes ---
    plt.figure()
    for size in df_mode['size'].unique():
        df_size = df_mode[df_mode['size'] == size]
        df_grouped = df_size.groupby('nprocs')[['runtime']].mean().reset_index()
        base_time = df_grouped[df_grouped['nprocs'] == 1]['runtime'].values[0]
        speedup = base_time / df_grouped['runtime']
        plt.plot(df_grouped['nprocs'], speedup, marker='o', label=f'size={size}')
    plt.xlabel('Number of Processes')
    plt.ylabel('Speed-up')
    plt.title(f'Speed-up vs Processes ({mode})')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'plots/combined/speedup_{mode}.png')
    plt.close()

    # --- plot 3: efficiency vs processes ---
    plt.figure()
    for size in df_mode['size'].unique():
        df_size = df_mode[df_mode['size'] == size]
        df_grouped = df_size.groupby('nprocs')[['runtime']].mean().reset_index()
        base_time = df_grouped[df_grouped['nprocs'] == 1]['runtime'].values[0]
        speedup = base_time / df_grouped['runtime']
        efficiency = (speedup / df_grouped['nprocs']) * 100
        plt.plot(df_grouped['nprocs'], efficiency, marker='o', label=f'size={size}')
    plt.xlabel('Number of Processes')
    plt.ylabel('Efficiency (%)')
    plt.title(f'Efficiency vs Processes ({mode})')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'plots/combined/efficiency_{mode}.png')
    plt.close()

print("All combined plots finished.")

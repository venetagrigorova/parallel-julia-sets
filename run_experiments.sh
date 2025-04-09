#!/bin/bash

# List of process counts
PROCS=(1 2 4 8 16 24 32)
PATCH=22
RESULT_FILE="results.csv"
OUTPUT_DIR="outputs"

# Create output directory
mkdir -p $OUTPUT_DIR

# CSV header
echo "size,patch,nprocs,runtime,mode,run" > $RESULT_FILE

run_experiments() {
    SIZE=$1
    MODE=$2
    BENCHMARK_FLAG=$3

    echo "=== Running for SIZE=$SIZE, MODE=$MODE ==="

    for P in "${PROCS[@]}"; do
        echo "Running size=$SIZE, nprocs=$P, mode=$MODE, 3 times..."
        for RUN in 1 2 3; do
            OUTPUT_FILE="${OUTPUT_DIR}/output_${SIZE}_${MODE}_p${P}_run${RUN}.png"
            echo "  Run $RUN: Saving to $OUTPUT_FILE"
            # Capture the output of the python command
            OUT=$(python3 julia_par.py --size $SIZE --nprocs $P --patch $PATCH $BENCHMARK_FLAG -o $OUTPUT_FILE)
            # Parse the output: 165;22;1;0.2884
            IFS=';' read -ra FIELDS <<< "$OUT"
            SIZE_FIELD="${FIELDS[0]}"
            PATCH_FIELD="${FIELDS[1]}"
            NPROCS_FIELD="${FIELDS[2]}"
            RUNTIME_FIELD="${FIELDS[3]}"
            echo "$SIZE_FIELD,$PATCH_FIELD,$NPROCS_FIELD,$RUNTIME_FIELD,$MODE,$RUN" >> $RESULT_FILE
            sleep 1
        done
    done
}

# --- PART 1: Run c_b (benchmark case) ---
run_experiments 165 "cb" "--benchmark"
run_experiments 1020 "cb" "--benchmark"

# --- PART 2: Run c_s (student case) ---
run_experiments 165 "cs" ""
run_experiments 1020 "cs" ""

echo "All experiments finished!"

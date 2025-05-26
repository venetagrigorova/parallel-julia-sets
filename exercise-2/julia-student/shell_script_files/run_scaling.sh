#!/bin/bash

N_VALUES=(85 1150)
P_VALUES=(1 2 4 8 16 24 32)
REPEATS=3

OUTFILE="scaling_results.csv"
echo "n,p,run,time" > $OUTFILE

for n in "${N_VALUES[@]}"; do
  for p in "${P_VALUES[@]}"; do
    export OMP_NUM_THREADS=$p
    for r in $(seq 1 $REPEATS); do
      echo "Running: n=$n, p=$p, run=$r"
      result=$(./bin/juliap_runner -n $n -p $p)
      time=$(echo $result | awk -F',' '{print $3}')
      echo "$n,$p,$r,$time" >> $OUTFILE
    done
  done
done

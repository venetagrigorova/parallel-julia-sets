#!/bin/bash

SCHEDULES=("static" "static,1" "dynamic,5" "guided,10")
REPEATS=3
N=1150
P=16

OUTFILE="schedule_results.csv"
echo "schedule,run,time" > $OUTFILE

export OMP_NUM_THREADS=$P

for sched in "${SCHEDULES[@]}"; do
  export OMP_SCHEDULE=$sched
  for r in $(seq 1 $REPEATS); do
    echo "Running: schedule=$sched, run=$r"
    result=$(./bin/juliap_runner -n $N -p $P)
    time=$(echo $result | awk -F',' '{print $3}')
    echo "\"$sched\",$r,$time" >> $OUTFILE
  done
done

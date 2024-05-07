#!/bin/bash
./lost pipeline \
  --png $1 \
  --focal-length 49 \
  --pixel-size 22.2 \
  --centroid-algo cog \
  --centroid-mag-filter 5 \
  --database my-database.dat \
  --star-id-algo py \
  --angular-tolerance 0.05 \
  --false-stars 1000 \
  --max-mismatch-prob 0.0001 \
  --attitude-algo dqm \
  --print-attitude attitude.txt \
  --plot-output annotated-$1.png 

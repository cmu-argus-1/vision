#!/bin/bash

pixel_sizes=("1.40e-6" "1.76e-6" "2.12e-6" "2.48e-6" "2.84e-6" "3.20e-6")

for pixel_size in "${pixel_sizes[@]}"; do
    echo "Generating plot for pixel_size = $pixel_size"
    python3 ops_vs_actual_frame_process_time.py "$pixel_size"
done

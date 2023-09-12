#!/bin/bash

# List of pixel_size values
pixel_sizes=("1.40e-6" "1.76e-6" "2.12e-6" "2.48e-6" "2.84e-6" "3.20e-6")

# List of ops_per_frame values
ops_per_frames=("8.8e9" "8.2e10" "2.96e11" "3.16e11" "3.86e11" "4.32e11")

for pixel_size in "${pixel_sizes[@]}"; do
    for ops_per_frame in "${ops_per_frames[@]}"; do
        echo "Generating plot for pixel_size = $pixel_size and ops_per_frame = $ops_per_frame"
        python3 ops_vs_actual_frame_process_time.py "$pixel_size" "$ops_per_frame"
    done
done

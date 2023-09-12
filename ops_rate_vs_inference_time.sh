#!/bin/bash

declare -A combinations
combinations=(
    ["1.40e-6"]="8.80e+09"
    ["1.76e-6"]="8.20e+10"
    ["2.12e-6"]="2.96e+11"
    ["2.48e-6"]="3.16e+11"
    ["2.84e-6"]="3.86e+11"
    ["3.20e-6"]="4.34e+11"
)

for pixel_size in "${!combinations[@]}"; do
    ops_per_frame=${combinations[$pixel_size]}
    echo "Generating plot for pixel_size = $pixel_size and ops_per_frame = $ops_per_frame"
    python3 ops_rate_vs_inference_time.py "$pixel_size" "$ops_per_frame"
done
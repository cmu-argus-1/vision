#!/bin/bash

# List of pixel_size values
pixel_sizes=("1.40e-6" "1.76e-6" "2.12e-6" "2.48e-6" "2.84e-6" "3.20e-6")

# Run the Python script for each pixel_size value
for pixel_size in "${pixel_sizes[@]}"; do
    echo "Generating plot for pixel_size = $pixel_size"
    python3 gsd_vs_altitude.py "$pixel_size"
done

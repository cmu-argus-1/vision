import matplotlib.pyplot as plt
import numpy as np
import sys

# Check for the correct number of command-line arguments
if len(sys.argv) < 3:
    print("Usage: python ops_vs_actual_frame_process_time.py <pixel_size> <ops_per_frame>")
    sys.exit(1)

# Parse command-line arguments
pixel_size = float(sys.argv[1])
ops_per_frame = float(sys.argv[2])

# Constants
focal_lengths = [20e-3, 5e-3]  # TODO
harvested_power = 0.5
other_power = 5.0
pixel_count = 4000
altitude = 450000
earth_radius = 6.3781e6
mass_of_earth = 5.97219e24
gravitational_constant = 6.6743e-11

# Calculate the x-axis values (ops per second)
ops_per_second = [1.6685e11*30 + i * 1.6665e11*30 for i in range(14)]
power_per_second = [1.25 + i * 1.25 for i in range(14)]

# Calculate the y-axis values (actual frame process time)
ideal_frame_process_time = [ops_per_frame / ops for ops in ops_per_second]
power_cycle_duty_cycle = [min(1, harvested_power / (other_power + pw)) for pw in power_per_second]
actual_frame_process_time = [ift / pcd for ift, pcd in zip(ideal_frame_process_time, power_cycle_duty_cycle)]

# Calculate the deadlines and intersection points
deadlines = []
intersection_points = []

for focal_length in focal_lengths:
    gsd = pixel_size * altitude / focal_length
    orbit_velocity = np.sqrt(gravitational_constant * mass_of_earth / (earth_radius + altitude))
    ground_track_velocity = (earth_radius / (earth_radius + altitude)) * orbit_velocity
    frame_distance = pixel_count * gsd
    deadline = frame_distance / ground_track_velocity
    deadlines.append(deadline)
    # Find the intersection point
    intersection = None
    for i in range(len(ops_per_second) - 1):
        if actual_frame_process_time[i] >= deadline >= actual_frame_process_time[i + 1]:
            x1, x2 = ops_per_second[i], ops_per_second[i + 1]
            y1, y2 = actual_frame_process_time[i], actual_frame_process_time[i + 1]
            slope = (y2 - y1) / (x2 - x1)
            intersection = x1 + (deadline - y1) / slope
            break
    intersection_points.append(intersection)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(ops_per_second, actual_frame_process_time, marker='o', linestyle='-')
plt.xlabel('Ops per Second (ops/sec)')
plt.ylabel('Actual Frame Process Time (s)')
plt.title(f'Ops per Second vs. Actual Frame Process Time (Pixel Size: {pixel_size:.2e} m, Ops per Frame: {ops_per_frame:.2e})')

# Add horizontal deadline lines
for i, deadline in enumerate(deadlines):
    plt.axhline(y=deadline, color=f'C{i}', linestyle='--', label=f'Ddl with focal length {focal_lengths[i]:.3f}m: {deadline:.2f} s')

# Add vertical lines at intersection points
for i, intersection in enumerate(intersection_points):
    if intersection is not None:
        plt.axvline(x=intersection, color=f'C{i}', linestyle=':', label=f'Intersection {i+1}: {intersection:.4e} ops/sec')

# Add text labels for each data point
for x, y in zip(ops_per_second, actual_frame_process_time):
    plt.annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

plt.legend()
plt.grid(True)
# Save the plot with a meaningful name
image_filename = f"Ops_vs_Actual_Frame_Process_Time_Pixel_{pixel_size:.2e}_OpsPerFrame_{ops_per_frame:.2e}.png"
plt.savefig(image_filename)
# Show the plot
# plt.show()

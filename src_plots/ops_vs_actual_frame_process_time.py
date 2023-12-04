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
focal_lengths = [16e-3] 
harvested_power = 4.46
other_power = (15.4371 -7)
pixel_count = 3120
altitude = 525000
earth_radius = 6.3781e6
mass_of_earth = 5.97219e24
gravitational_constant = 6.6743e-11

# Calculate the x-axis values (ops per second)
ops_per_second = [1.6685e11/2 + i * 1.6665e11/2 for i in range(14)]
power_per_second = [1.25/2 + i * 1.25/2 for i in range(14)]

# Calculate the y-axis values (actual frame process time)
ideal_frame_process_time = [ops_per_frame / ops for ops in ops_per_second]
power_cycle_duty_cycle = [min(1, harvested_power / (other_power + pw)) for pw in power_per_second]
actual_frame_process_time = [ift / pcd for ift, pcd in zip(ideal_frame_process_time, power_cycle_duty_cycle)]

# # the model is 0.39 GFLOPS
# model_flops = 0.39e9
# # jetson nano ops per second is 275 trillion
# jetson_ops_per_second = 275e12
# model_frame_process_time = model_flops / jetson_ops_per_second
# # calcualte the actual frame process time
# model_power_cycle_duty_cycle = min(1, harvested_power / (other_power + 5))
# model_actual_frame_process_time = model_frame_process_time / model_power_cycle_duty_cycle
# # print the actual frame process time
# print(f"Model Actual Frame Process Time: {model_actual_frame_process_time*1000:.4f} ms")

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
plt.xlabel('Ops per Second (ops/sec)', fontsize=18)
plt.ylabel('Actual Frame Process Time (s)', fontsize=18)
plt.title(f'Ops per Second vs. Actual Frame Process Time \n(Pixel Size: {pixel_size:.2e} m, Ops per Frame: {ops_per_frame:.2e})', fontsize=20)

# Add horizontal deadline lines
for i, deadline in enumerate(deadlines):
    plt.axhline(y=deadline, color=f'C{i+1}', linestyle='--', label=f'Ddl with focal length {focal_lengths[i]:.3f}m: {deadline:.2f} s')

# Add vertical lines at intersection points
for i, intersection in enumerate(intersection_points):
    if intersection is not None:
        plt.axvline(x=intersection, color=f'C{i+2}', linestyle=':', label=f'Intersection {i+1}: {intersection:.2e} ops/sec')

# Add text labels for each data point
for x, y in zip(ops_per_second, actual_frame_process_time):
    plt.annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=13)

plt.legend(fontsize='large')
plt.grid(True)
# Save the plot with a meaningful name
image_filename = f"Ops_vs_Actual_Frame_Process_Time_Pixel_{pixel_size:.2e}_OpsPerFrame_{ops_per_frame:.2e}.png"
plt.savefig(image_filename)
# Show the plot
# plt.show()

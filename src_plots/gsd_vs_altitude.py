import matplotlib.pyplot as plt
import datetime
import matplotlib.colors as colors
import sys
import os

def calculate_gsd(pixel_size, focal_lengths, altitude_values):
    gsd_values = []
    for focal_length in focal_lengths:
        gsd = [pixel_size * altitude * 1000 / focal_length for altitude in altitude_values]
        gsd_values.append(gsd)
    return gsd_values

altitude_values = list(range(400, 751, 50))
# focal_lengths = [2, 5, 8, 11, 14, 17, 20]
focal_lengths = [16]
for i in range(len(focal_lengths)):
    focal_lengths[i] /= 1000

if len(sys.argv) < 2:
    print("Usage: python script.py <pixel_size>")
    sys.exit(1)

pixel_size = float(sys.argv[1])

gsd_values = calculate_gsd(pixel_size, focal_lengths, altitude_values)

title = f'Ground Sample Distance vs. Altitude (Pixel Size: {pixel_size:.2e} m)'

plt.figure(figsize=(10, 6))
for i, focal_length in enumerate(focal_lengths):
    plt.plot(altitude_values, gsd_values[i], label=f'Focal Length = {focal_length} m', marker='x')
    # label the values
    for altitude_value_i in altitude_values:
        plt.text(altitude_value_i, gsd_values[i][altitude_values.index(altitude_value_i)], f'{gsd_values[i][altitude_values.index(altitude_value_i)]:.2f}', fontsize=15)
# plot the vertical lines
plt.axvline(x=550, color='r', linestyle='--', label='Operational Altitude (550 km)')


# plt.axhline(y=500, color='r', linestyle='--', label='Okeechobee Limit (500 m)')
plt.axhline(y=30, color='purple', linestyle='--', label='Landsat (30 m)')
plt.axhline(y=3.7, color='g', linestyle='--', label='Dove (3.7 m)')
plt.axhline(y=0.3, color='y', linestyle='--', label='WorldView (0.3 m)')

plt.title(title, fontsize=20)

plt.xlabel('Altitude (km)', fontsize=18)
plt.ylabel('Ground Sample Distance (m/px)', fontsize=18)

plt.legend(title='Focal Lengths', fontsize=18)
plt.legend(loc='upper left')
plt.legend(fontsize='large') 
plt.grid(True)

output_filename = f'plot_{pixel_size:.2e}.png'
plt.savefig(output_filename)

plt.show()
plt.close()
print(f'Plot saved as {output_filename}')

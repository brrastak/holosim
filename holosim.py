
import numpy as np
from mayavi import mlab

from pixel import PixelMatrix




# radius = np.sqrt(vox_x_pos**2 + vox_y_pos**2 + vox_z_pos**2)
# radius = np.sqrt(vox_x_pos**2 + vox_y_pos**2 + (vox_z_pos + 500)**2)
# in micrometer
wave_len = 0.5
wave_number = 2 * np.pi / wave_len
# pixel_x_size = 10
# pixel_y_size = 10

values = np.zeros((1, 1), np.uint8)
values[0, 0] = 1
matrix = PixelMatrix(values)

vox_x_pos, vox_y_pos, vox_z_pos = np.mgrid[-100:100:100j, -100:100:100j, 0:200:100j]

light_phasor = np.ndarray(shape=vox_x_pos.shape, dtype=np.complex128)
for pixel in matrix:

    dist = pixel.distance(vox_x_pos, vox_y_pos, vox_z_pos)
    light_phasor += (np.exp(1j * wave_number * dist) / dist
        * np.sinc(wave_number * matrix.PIXEL_Y_SIZE * vox_x_pos / 2 / dist)
        * np.sinc(wave_number * matrix.PIXEL_X_SIZE * vox_y_pos / 2 / dist))

# radius = np.sqrt(vox_x_pos**2 + vox_y_pos**2 + vox_z_pos**2)
# light_phasor = (np.exp(1j * wave_number * radius) / radius
#     * np.sinc(wave_number * pixel_y_size * vox_x_pos / 2 / radius)
#     * np.sinc(wave_number * pixel_x_size * vox_y_pos / 2 / radius))
# light_intensity = np.abs(light_phasor)**2

# Power 0.5 instead of 2 decrease difference between high and low peaks
# and to make low peaks visible
light_intensity = np.abs(light_phasor)**(0.5)
# Values should be in range [0; 1] for consistency with pixel plot
light_intensity /= np.max(light_intensity)

# print(light_phasor)
# print(light_intensity)

fig = mlab.figure()
contour = mlab.contour3d(vox_x_pos, vox_y_pos, vox_z_pos, light_intensity, colormap='winter')

# s = np.random.random((20, 20))

# s = np.linspace(0, 1, 100)
# s.shape = (10, 10)
# pixels = mlab.imshow(s, colormap='winter')

mlab.xlabel("X")
mlab.ylabel("Y")
mlab.zlabel("Z")
mlab.title("Hologram simulation")
mlab.show()

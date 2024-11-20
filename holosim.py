
import numpy as np
from mayavi import mlab

from pixel import PixelMatrix



# All distances are measured in micrometers
wave_len = 0.5
wave_number = 2 * np.pi / wave_len

# Plot configuration
x_start = -100
x_end = 100
y_start = -100
y_end = 100
z_start = 0
z_end = 200
step = 1



pixel_values = np.zeros((3, 3), np.uint8)
# pixel_values[0, 0] = 1
pixel_values[1, 1] = 1
matrix = PixelMatrix(pixel_values)

def number_of_points(start, end):
    return (end - start) / step * 1j

vox_x_pos, vox_y_pos, vox_z_pos = np.mgrid[
    x_start:x_end:number_of_points(x_start, x_end),
    y_start:y_end:number_of_points(y_start, y_end),
    z_start:z_end:number_of_points(z_start, z_end)
]


light_phasor = np.ndarray(shape=vox_x_pos.shape, dtype=np.complex128)
for pixel in matrix:

    if not pixel.is_turned_on():
        continue

    # Z coordinate offset is needed for correct calculation
    # but for the picture drawing still used Z coordinate without offset
    vox_z_pos_with_offset = vox_z_pos + 500

    dist = pixel.distance(vox_x_pos, vox_y_pos, vox_z_pos_with_offset)
    light_phasor += (np.exp(1j * wave_number * dist) / dist
        * np.sinc(wave_number * matrix.PIXEL_X_SIZE * vox_x_pos / 2 / dist / np.pi)
        * np.sinc(wave_number * matrix.PIXEL_Y_SIZE * vox_y_pos / 2 / dist / np.pi)
        )

# Power of 0.5 instead of 2 to decrease difference between high and low peaks
# and to make low peaks visible
light_intensity = np.abs(light_phasor)**(0.5)
# Values should be in range [0; 1] for consistency with pixel plot
light_intensity /= np.max(light_intensity)



fig = mlab.figure()
voxel_plot = mlab.contour3d(vox_x_pos, vox_y_pos, vox_z_pos, light_intensity, colormap='winter')

# s = np.random.random((20, 20))

# s = np.linspace(0, 1, 100)
# s.shape = (10, 10)

pixel_plot = np.empty((0, 0))

if step > matrix.PIXEL_X_SIZE or step > matrix.PIXEL_Y_SIZE:
    # No pixel detalization, just the whole matrix
    size_x = matrix.number_of_pixels_x() * matrix.PIXEL_X_SIZE // step
    size_y = matrix.number_of_pixels_y() * matrix.PIXEL_Y_SIZE // step
    pixel_plot = np.ones((size_x, size_y))
else:
    # Size of virtual pixel in pixels that represents it in plot
    pixel_size_x = matrix.PIXEL_X_SIZE // step
    pixel_size_y = matrix.PIXEL_Y_SIZE // step
    for row in pixel_values:
        pixel_row = np.empty((0, 0))
        for pixel in row:
            if pixel == 0:
                pixel_rectangle = np.zeros((pixel_size_x, pixel_size_y))
            else:
                pixel_rectangle = np.ones((pixel_size_x, pixel_size_y))
            if pixel_row.shape == (0, 0):
                pixel_row = pixel_rectangle
            else:
                pixel_row = np.hstack((pixel_row, pixel_rectangle))
        if pixel_plot.shape == (0, 0):
            pixel_plot = pixel_row
        else:
            pixel_plot = np.vstack((pixel_plot, pixel_row))


pixels = mlab.imshow(pixel_plot, colormap='winter')
# pixels = mlab.imshow(pixel_plot, colormap="winter", extent=[0, 10, 0, 20, 0, 0], vmax=1, vmin=0)

# size_x = matrix.number_of_pixels_x() * matrix.PIXEL_X_SIZE
# size_y = matrix.number_of_pixels_y() * matrix.PIXEL_Y_SIZE
# pixels = mlab.imshow(pixel_values.astype(dtype=np.float32), colormap="winter", extent=[0, size_x, 0, size_y, 0, 0])

# mlab.colorbar()

mlab.xlabel("X")
mlab.ylabel("Y")
mlab.zlabel("Z")
mlab.title("Hologram simulation")
mlab.show()

# from kivy.app import App
# from kivy.uix.button import Button


# class HelloWorldApp(App):
#    def build(self):
#        return Button(text="Hello Kivy World")


# HelloWorldApp().run()

	
import numpy as np
from mayavi import mlab




class Matrix:

    values = np.zeros((3, 3), np.uint8)
    pixel_x_size = 0.5
    pixel_y_size = 0.5

    def x_pos(self):
        return 0
    
    def y_pos(self):
        return 0

# def plane(x: np.ndarray):
#     res = np.zeros(x.shape)
#     for (val, arg) in zip(res.flat, x.flat):
#         # if arg > 1:
#         val = 1
#     return res

def plane(x):
    if x > 0:
        return 1
    else:
        return 0
    
plane_v = np.vectorize(plane)


vox_x_pos, vox_y_pos, vox_z_pos = np.mgrid[-100:100:100j, -100:100:100j, 0:500:100j]
# x1, y1 = np.mgrid[-5:5:500j, -5:5:500j]
# scalar = np.sin(np.sqrt(x**2 + y**2 + z**2))

# scalar = np.sinc(x)*np.sinc(y) #/(np.abs(z)+1)

# scalar = plane_v(z)
# print(scalar)

radius = np.sqrt(vox_x_pos**2 + vox_y_pos**2 + vox_z_pos**2)
# in micrometer
wave_len = 0.5
wave_number = 2 * np.pi / wave_len
pixel_x_size = 10
pixel_y_size = 10

light_phasor = np.exp(1j * wave_number * radius) / radius           \
    * np.sinc(wave_number * pixel_y_size * vox_x_pos / 2 / radius)  \
    * np.sinc(wave_number * pixel_x_size * vox_y_pos / 2 / radius)
light_intensity = np.abs(light_phasor)**2


fig = mlab.figure()
contour = mlab.contour3d(vox_x_pos, vox_y_pos, vox_z_pos, light_intensity, colormap='winter')


s = np.random.random((20, 20))
pixels = mlab.imshow(s, colormap='winter')

mlab.xlabel('X')
mlab.ylabel('Y')
mlab.zlabel('Z')
mlab.title('3D Contour Plot')
mlab.show()

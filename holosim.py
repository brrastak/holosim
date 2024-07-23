# from kivy.app import App
# from kivy.uix.button import Button


# class HelloWorldApp(App):
#    def build(self):
#        return Button(text="Hello Kivy World")


# HelloWorldApp().run()

	
import numpy as np
from mayavi import mlab


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


x, y, z = np.mgrid[-5:5:50j, -5:5:50j, 0:10:50j]
# x1, y1 = np.mgrid[-5:5:500j, -5:5:500j]
scalar = np.sin(np.sqrt(x**2 + y**2 + z**2))

# scalar = plane_v(z)
# print(scalar)

fig = mlab.figure()
contour = mlab.contour3d(x, y, z, scalar, colormap='magma')


s = np.random.random((20, 20))
pixels = mlab.imshow(s)

mlab.xlabel('X')
mlab.ylabel('Y')
mlab.zlabel('Z')
mlab.title('3D Contour Plot')
mlab.show()

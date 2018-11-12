import h5py
import math
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

"""
#%% get filename
root = Tk()
root.withdraw()
#filename = filedialog.askopenfilename(filetypes = [('h5_file',"*.h5")])
filename='../dataset/user3_gambe.h5'

#%% explore read file data

h5file = h5py.File(filename)

# print('present groups', list(h5file.keys()))
sensor_type = 'ACCELEROMETER_3D'
sensor_position = '0x0289fe5f'
t = h5file[sensor_type][sensor_position]['t'][:]
a_x = h5file[sensor_type][sensor_position]['x']['v'][:]
a_y = h5file[sensor_type][sensor_position]['y']['v'][:]
a_z = h5file[sensor_type][sensor_position]['z']['v'][:]

h5file.close()

#implement a low_pass filter
a = 0.01
b = 0.01
a_y_filtered = [a_y[0]]
a_z_filtered = [a_z[0]]

for i in range(1, a_y.shape[0]):
    a_y_filtered.append(a_y[i]*a+(1-a)*a_y_filtered[i-1])
    a_z_filtered.append(a_z[i]*b+(1-b)*a_z_filtered[i-1])

#plt.plot(a_y)
#plt.plot(a_y_filtered)
#plt.plot(a_z)
#plt.plot(a_z_filtered)
#plt.show()

#get_angles
angles = []
for i in range(len(a_y_filtered)):
    if a_z_filtered[i] > 0:
        angles.append(+a_y_filtered[i]*90/9.8)
    else:
        angles.append(((+9.8-(a_y_filtered[i])) * 90 / 9.8)+90)
#plt.plot(angles)
#plt.show()

#implement a low_pass filter
a = 0.01
angles_filtered = [angles[0]]
for i in range(1, a_y.shape[0]):
    angles_filtered.append(angles[i]*a+(1-a)*angles_filtered[i-1])

plt.plot(angles_filtered)
plt.show()
"""

a=0.5
a_y_filtered = []
a_z_filtered = []
angles = []
angles_filtered = []
def get_angles_2(data):
    global a
    global a_y_filtered
    global a_z_filtered
    global angles
    global angles_filtered
    if len(a_y_filtered) > 0:
        a_y_filtered.append((data["R_THG"])[1] * a + (1 - a) * a_y_filtered[-1])
        a_z_filtered.append((data["R_THG"])[2] * a + (1 - a) * a_z_filtered[-1])
        if len(angles) > 0:
            if a_z_filtered[-1] > 0:
                temp = a_y_filtered[-1] * 90 / 9.8
            else:
                temp = ((9.8 - (a_y_filtered[-1])) * 90 / 9.8) + 90
            angles_filtered.append(temp*a+(1-a)*angles[-1])
            angles.append(temp)
            return angles_filtered[-1]
        else:
            if a_z_filtered[-1] > 0:
                angles.append(a_y_filtered[-1] * 90 / 9.8)
            else:
                angles.append(((9.8 - (a_y_filtered[-1])) * 90 / 9.8) + 90)
            return 80
    else:
        a_y_filtered.append((data["R_THG"])[1])
        a_z_filtered.append((data["R_THG"])[2])
        return 80

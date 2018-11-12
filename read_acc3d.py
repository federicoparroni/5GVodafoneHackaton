import h5py
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

#%% get filename 
root = Tk()
root.withdraw()
filename = filedialog.askopenfilename(filetypes = [('h5_file',"*.h5")])


#%% explore read file data

h5file = h5py.File(filename)

uuid = h5file.attrs['_uuid'][0]

print (filename, ' → uuid ', uuid)
try:
	start_event_dset = h5file['EVENT']['START_SESSION']
	start_attribute_names = list(start_event_dset.attrs)
	for attribute_name in start_attribute_names:
		print(attribute_name, ' → ', start_event_dset.attrs[attribute_name][0])
except:
	pass

# print('present groups', list(h5file.keys()))
sensor_type = 'ACCELEROMETER_3D'
sensor_position = '0x026afd8f'
t = h5file[sensor_type][sensor_position]['t'][:]
acc_data = h5file[sensor_type][sensor_position]['x']['v'][:]
h5file.close()

diff_data = [0]
for i in range(1,len(acc_data)):
  diff_data.append(acc_data[i]-acc_data[i-1])

#%% plot
fig, ax = plt.subplots(2,1,sharex=True)
ax[0].plot(t, acc_data)
ax[0].set_title('accelerometer')
ax[1].plot(t, diff_data)
ax[1].set_title('difference')

plt.show()
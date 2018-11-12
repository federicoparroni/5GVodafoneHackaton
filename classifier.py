import numpy as np

# STATES:
NOT_STARTED = 0
NOT_IN_POSE = 1
CORRECT_POSE = 2
WRONG_POSE = 3

old_data = {}

sensor_type = 'ACCELEROMETER_3D'
# sens_r = ['0x0283fdaf', '0x0281fe5f', '0x0268fc8f']
# sens_l = ['0x02a3fdaf', '0x02a1fe5f', '0x0268fe8f']
sens = [ 'R_FOR', 'L_FOR', 'R_ARM', 'L_ARM', 'R_SHC', 'L_SHC']
axes = ['x', 'y', 'z']

threshold_x = 30

"""
Get player status based on sensor measures:
sum of squared differences of 6 sensors (on both arms)

< data: dictionary of accelerometer measures (key: sensor position, value: [x,y,z])

> return: status
"""
def get_status(data):
    # compute sum of squared differences
    if len(old_data.items) > 0:
        sum_sqdiff_xyz = np.array([0, 0, 0])
        for senspos, xyz in data.items():
            # filter only the wanted sensor for pose classification
            if senspos in sens:
                curr = np.array(xyz)
                prev = np.array(old_data)
                
                diff = curr - prev
                diff_square = (diff) ** 2
                sum_sqdiff_xyz += diff_square
        
    old_data = data
    if sum_sqdiff_xyz[0] < threshold_x:
        # check if correct pose
        return CORRECT_POSE if 1 else WRONG_POSE
    else:
        return NOT_IN_POSE
    

"""
#Store the new data in the buffer

#def store_in_buffer(data):
#    if len(buffer) >= buf_size:
#        buffer.pop(0)
#    buffer.append(data)

# Get the most recent sensor data from the buffer
# < key: sensor position identifier

# > return: most recent buffer item [x,y,z]

def get_prev_from_buffer(key):
    return buffer[key][-1]

"""
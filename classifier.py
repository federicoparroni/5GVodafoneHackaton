import numpy as np
from getAngles_back import get_angles
from getAngles_knees import get_angles_2
# STATES:
NOT_STARTED = 0
NOT_IN_POSE = 'PLAYING'
CORRECT_POSE = 'POSE OK'
WRONG_POSE = 'WRONG POSE'

old_data = {}

sensor_type = 'ACCELEROMETER_3D'
# sens_r = ['0x0283fdaf', '0x0281fe5f', '0x0268fc8f']
# sens_l = ['0x02a3fdaf', '0x02a1fe5f', '0x0268fe8f']
sens = ['R_FOR', 'L_FOR', 'R_ARM', 'L_ARM', 'R_SHC', 'L_SHC']
axes = ['x', 'y', 'z']

threshold_x = 35

"""
Get player status based on sensor measures:
sum of squared differences of 6 sensors (on both arms)

< data: dictionary of accelerometer measures (key: sensor position, value: [x,y,z])

> return: status
"""
def get_status(data):
    global old_data
    # compute sum of squared differences
    if len(old_data.items()) > 0:
        sum_sqdiff_xyz = np.array([0.0, 0.0, 0.0])
        for senspos, xyz in data.items():
            # filter only the wanted sensor for pose classification
            if senspos in sens:
                curr = np.array(xyz)
                prev = np.array(old_data[senspos])
                
                diff = curr - prev
                diff_square = (diff) ** 4
                sum_sqdiff_xyz += diff_square

        # print(sum_sqdiff_xyz[0])
        if sum_sqdiff_xyz[0] < threshold_x and sum_sqdiff_xyz[2] < threshold_x:
            # check if correct pose
            old_data = data
            angle_back = get_angles(data)
            angle_knees = get_angles_2(data)
            print(angle_back)
            if angle_back < 70 and angle_back > 45 and angle_knees > 30 and angle_knees < 60:
                return CORRECT_POSE
            else:
                return WRONG_POSE
        else:
            old_data = data
            return NOT_IN_POSE
    old_data = data
    

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
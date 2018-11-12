import utilities.data_cloud_messages_pb2 as protobuf
import numpy as np
from collections import deque
import threading
import matplotlib.pyplot as plt
from utilities.sensor_code_converter import sensor_code_converter

class sensor:

    def __init__(self, sensor_type, sensor_position, plot_duration_sec = None, plot_flag = False):

        # Definition of the sensor type and position (in hex and int format)
        self._type = sensor_type
        if type(sensor_position) == int:
            self._sensor_position = sensor_position
        else:
            self._sensor_position = int(sensor_position,16)

        # Definition of the sensor channels
        # DO NOT CHANGE THE channel_list VARIABLE
        if self._type == "ELECTROCARDIOGRAM_2_CH":
            channel_list = ["value_ch1_cal", "value_ch2_cal"]
            self._set_read_data(channel_list)
        elif self._type == "RESPIRATION_2_CH":
            channel_list = ["value_ch1_eng", "value_ch2_eng"]
            self._set_read_data(channel_list)
        elif self._type == "ACCELEROMETER_3D" or  self._type == "GYROSCOPE_3D" or self._type == "MAGNETOMETER_3D":
            channel_list = ["x_cal", "y_cal", "z_cal"]
            self._set_read_data(channel_list)
        elif self._type == "QUATERNIONS":
            channel_list = ["q0_eng", "q1_eng", "q2_eng", "q3_eng"]
            self._set_read_data(channel_list)

        # Other parameters
        self._sensor_enabled = False
        self._data_buffer = None
        self._sampling_freq = 0
        self._plot_size = 0
        self._start_time = 0

        # Figure initialization: graphical preferences
        if plot_flag:
            if self.get_type() == "ELECTROCARDIOGRAM_2_CH":
                self._xlabel = "time (s)"
                self._ylabel = "ECG signal (mV)"
                self._title = "Electrocardiogram, pos:" + self.get_position("hex")
                self._legend = ["ch1", "ch2"]

            if self.get_type() == "RESPIRATION_2_CH":
                self._xlabel = "time (s)"
                self._ylabel = "respiration (V)"
                self._title = "Respiration, pos:" + self.get_position("hex")
                self._legend = ["thorax", "abdomen"]

            elif self.get_type() == "ACCELEROMETER_3D":
                self._xlabel = "time (s)"
                self._ylabel = "acceleration (m/s^2)"
                self._title = "Accelerometer, pos:" + self.get_position("hex")
                self._legend = ["x-axis", "y-axis", "z-axis"]

            elif self.get_type() == "GYROSCOPE_3D":
                self._xlabel = "time (s)"
                self._ylabel = "rotation (rad/s)"
                self._title = "Gyroscope, pos:" + self.get_position("hex")
                self._legend = ["x-axis", "y-axis", "z-axis"]

            elif self.get_type() == "MAGNETOMETER_3D":
                self._xlabel = "time (s)"
                self._ylabel = "magnetic field (G)"
                self._title = "Magnetometer, pos:" + self.get_position("hex")
                self._legend = ["x-axis", "y-axis", "z-axis"]

            elif self.get_type() == "QUATERNIONS":
                self._xlabel = "time (s)"
                self._ylabel = "quaternion (a.u.)"
                self._title = "Quaternion, pos:" + self.get_position("hex")
                self._legend = ["q0", "q1", "q2", "q3"]

            self._plot_duration_sec = plot_duration_sec
            self._plot_thread = None
            self._my_figure, self._my_axis = plt.subplots()
            plt.title(self._title)
            self._my_lines = dict()
            self._draw_plot_flag = False
            self._my_axis.set_autoscaley_on(True)



    def __eq__(self, other):
        # = operator overload: the sensor are "equivalent" if they have the same type and position
        return self._sensor_position == other.get_position() and self._type == other.get_type()

    def get_position(self, format="int"):
        if format == "int":
            return self._sensor_position
        elif format == "hex":
            return "0x%08X" % self._sensor_position

    def get_type(self):
        return self._type

    def get_sampling_freq(self):
        # Return the sampling frequency in Hz
        return self._sampling_freq


    def _set_read_data(self, channel_list):
        # Lambda function used to read the sensor data according to its channel list
        string = ""
        for ch_name in channel_list:
            string += ",values." + ch_name
        self._read_data = eval("lambda values: [" + string[1:] + "]")

    def _find_freq(self,message_start_event, data_destination):
        # method which return the sampling frequency (in Hz) read back from the start event for the current sensor
        wearable = message_start_event.event.wearable
        for w in wearable:
            sens = w.sensor
            for s in sens:
                if self == sensor(sensor_code_converter(s.type),int(s.position)):
                    data_usage = s.data_usage
                    for usage in data_usage:
                        if usage.data_destination == data_destination:
                            return usage.frequency

    def start_event(self, timestamp, message_start_event):
        # Complete the sensor initialization by reading its sampling frequency
        # CLOUD_STREAMING is the real time scenario.
        self._sampling_freq = self._find_freq(message_start_event, protobuf.DataUsage.CLOUD_STREAMING)
        if self._sampling_freq is None:
            return

        self._buffer_length = self._sampling_freq
        self._plot_size = int(self._sampling_freq * self._plot_duration_sec)
        self._data_buffer = [deque(),deque()]
        self._buffer_index = 0
        self._sensor_enabled = True
        self._start_time = timestamp

        # Debug print
        print("TimeStamp Evento Start:", message_start_event.timestamp, ". La frequenza del sensore è:",
              self._sampling_freq, "Hz")

    def stop_event(self):
        # reset the sensor if a STOP SCENARIO event occurred
        self._data_buffer[0].clear()
        self._data_buffer[1].clear()
        self._data_buffer = None
        self._buffer_index = 0
        self._sampling_freq = 0
        self._sensor_enabled = False

    def set_data(self, timestamp, device_sensor_output):
        # manage the input data for the current sensor
        if not self._sensor_enabled:
            return

        # fill in new data with the last sampled data
        new_data = []
        if self._type == "ELECTROCARDIOGRAM_2_CH":
            new_data = device_sensor_output.electrocardiogram_2_ch
        elif self._type == "RESPIRATION_2_CH":
            new_data = device_sensor_output.respiration_2_ch
        elif self._type == "ACCELEROMETER_3D":
            new_data = device_sensor_output.accelerometer_3D
        elif self._type == "GYROSCOPE_3D":
            new_data = device_sensor_output.gyroscope_3D
        elif self._type == "MAGNETOMETER_3D":
            new_data = device_sensor_output.magnetometer_3D
        elif self._type == "QUATERNIONS":
            new_data = device_sensor_output.quaternions

        # decode data from the Kafka message
        data = [timestamp] + self._read_data(new_data)

        # store data in the deque
        self._data_buffer[self._buffer_index].append(data)

        # Every one second, change the deque where to store data.
        # In a different thread:
        # 1) Read data from the last used deque
        # 3) Update plot in a different thread
        # 3) Clear the last used deque so that it can store other data.
        # NB: one deque must be cleared in one second at most.
        if len(self._data_buffer[self._buffer_index]) == self._buffer_length:
            if self._buffer_index == 0:
                if not self._plot_thread is None:
                    while self._plot_thread.is_alive():
                        continue
                self._buffer_index = 1
                self._plot_thread = threading.Thread(target=self._update_plot, args=(0,))
                self._plot_thread.start()

            elif self._buffer_index == 1:
                if not self._plot_thread is None:
                    while self._plot_thread.is_alive():
                        continue
                self._buffer_index = 0
                self._plot_thread = threading.Thread(target=self._update_plot, args=(1,))
                self._plot_thread.start()


    def _update_plot(self, buffer_index):
        # Get sensor data
        data = np.array(self._data_buffer[buffer_index])

        # Set stat event timestamp as initial reference time
        data[:,0] = data[:, 0] - self._start_time

        # Comupte x axis from the data timestamps
        if len(self._my_lines.keys()) == 0:
            xdata = data[:, 0]
        else:
            xdata = np.append(self._my_lines[0].get_xdata(), data[:, 0])

        if len(xdata) >= self._plot_size:
            xdata = xdata[-self._plot_size:]

        # For each sensor channel, plot the sensor data
        color_map = ["k-", "b-", "r-", "g-"]
        if not len(self._my_lines.keys()) ==0:
            for j in range(len(self._my_axis.lines)):
                del self._my_axis.lines[0]

        # Update the plot
        for ch in range(len(self._legend)):
            if not ch in self._my_lines.keys():
                ydata = data[:, ch+1]
            else:
                ydata = np.append(self._my_lines[ch].get_ydata(), data[:, ch+1])

            if len(ydata) >= self._plot_size:
                ydata = ydata[-self._plot_size:]

            self._my_lines[ch], = self._my_axis.plot(xdata, ydata, color_map[ch])

        # Update labels and legend
        self._data_buffer[buffer_index].clear()
        self._my_axis.relim()
        self._my_axis.autoscale_view()
        self._my_axis.set_xlabel(self._xlabel)
        self._my_axis.set_ylabel(self._ylabel)
        self._my_axis.legend(self._legend)

        self._draw_plot_flag = True


    def redraw(self):
        # Return True if the plot has to be updated.
        # Return False otherwise
        if self._draw_plot_flag:
            self._draw_plot_flag = False
            return True
        else:
            return False





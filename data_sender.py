from kafka import KafkaConsumer, TopicPartition
import utilities.data_cloud_messages_pb2 as protobuf
from utilities.getUserUUID import Num2Partition
from utilities.sensor_code_converter import sensor_code_converter
import sensor
import matplotlib.pyplot as plt
import classifier

###########################################
# VIEWER PARAMETERS
###########################################
user_number = 3
kafka_topic_input_data = "hackathon"
server_address = "81.29.147.100:9094"
sensor_type = "ACCELEROMETER_3D"
sensor_position = "0x0289FE5F"
plot_range_sec = 10

count=9

###########################################
# MAIN SCRIPT
###########################################
print("Current configuration:")
print("-> User", user_number, "sensor: ", sensor_type, "position: ", sensor_position)

# Sensor constructor
my_sensor = sensor.sensor(sensor_type,sensor_position,plot_range_sec,True)

# Initialization of the protobuffer object
data_container = protobuf.DataContainer()

# Kafka consumer definition
partition_num = Num2Partition(user_number)
consumer = KafkaConsumer(bootstrap_servers=server_address,auto_offset_reset='latest',
                         enable_auto_commit=False)
partitions = [TopicPartition(kafka_topic_input_data, partition_num)]
consumer.assign(partitions)

# Wait for kafka messages: endless loop
dict =	{
    "L5": [],
    "R_THG": [],
    "L_THG": [],
    "L_FOR": [],
    "L_ARM": [],
    "L_SHC": [],
    "R_FOR": [],
    "R_ARM": [],
    "R_SHC": []
}
count = 0
for msg in consumer:
    # Parse the current protobufer message
    data_container.ParseFromString(msg.value)

    # menage the received data container
    for protobuf_message in data_container.message:

        # Start event provided
        if protobuf_message.type == protobuf.Message.EVENT and protobuf_message.event.type == protobuf.Event.START_SCENARIO:
            my_sensor.start_event(protobuf_message.timestamp, protobuf_message)

        # Stop event provided
        elif protobuf_message.type == protobuf.Message.EVENT and protobuf_message.event.type == protobuf.Event.STOP_SCENARIO:
            my_sensor.stop_event()

        # Sensor data provided
        elif protobuf_message.type == protobuf.Message.DEVICE_SENSOR_OUTPUT:
            if protobuf_message.device_sensor_output.sensor.type == 0:
                if protobuf_message.device_sensor_output.sensor.position == 0x02a3fdaf:
                    if dict["L_FOR"] == []:
                        count += 1
                    dict["L_FOR"] = [protobuf_message.device_sensor_output.accelerometer_3D.x_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.y_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.z_cal]
                if protobuf_message.device_sensor_output.sensor.position == 0x0283fdaf:
                    if dict["R_FOR"] == []:
                        count += 1
                    dict["R_FOR"] = [protobuf_message.device_sensor_output.accelerometer_3D.x_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.y_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.z_cal]
                if protobuf_message.device_sensor_output.sensor.position == 0x02a1fe5f:
                    if dict["L_ARM"] == []:
                        count += 1
                    dict["L_ARM"] = [protobuf_message.device_sensor_output.accelerometer_3D.x_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.y_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.z_cal]
                if protobuf_message.device_sensor_output.sensor.position == 0x0281fe5f:
                    if dict["R_ARM"] == []:
                        count += 1
                    dict["R_ARM"] = [protobuf_message.device_sensor_output.accelerometer_3D.x_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.y_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.z_cal]
                if protobuf_message.device_sensor_output.sensor.position == 0x0268fe8f:
                    if dict["L_SHC"] == []:
                        count += 1
                    dict["L_SHC"] = [protobuf_message.device_sensor_output.accelerometer_3D.x_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.y_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.z_cal]
                if protobuf_message.device_sensor_output.sensor.position == 0x0268fc8f:
                    if dict["R_SHC"] == []:
                        count += 1
                    dict["R_SHC"] = [protobuf_message.device_sensor_output.accelerometer_3D.x_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.y_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.z_cal]
                if protobuf_message.device_sensor_output.sensor.position == 0x0289fe5f:
                    if dict["R_THG"] == []:
                        count += 1
                    dict["R_THG"] = [protobuf_message.device_sensor_output.accelerometer_3D.x_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.y_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.z_cal]
                if protobuf_message.device_sensor_output.sensor.position == 0x02a9fe5f:
                    if dict["L_THG"] == []:
                        count += 1
                    dict["L_THG"] = [protobuf_message.device_sensor_output.accelerometer_3D.x_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.y_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.z_cal]
                if protobuf_message.device_sensor_output.sensor.position == 0x026afd8f:
                    if dict["L5"] == []:
                        count += 1
                    dict["L5"] = [protobuf_message.device_sensor_output.accelerometer_3D.x_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.y_cal,
                                     protobuf_message.device_sensor_output.accelerometer_3D.z_cal]
            if count == 9:
                print('daaiii')
                count = 0
                dict = {
                    "L5": [],
                    "R_THG": [],
                    "L_THG": [],
                    "L_FOR": [],
                    "L_ARM": [],
                    "L_SHC": [],
                    "R_FOR": [],
                    "R_ARM": [],
                    "R_SHC": []
                }
                #classifier.get_status()
                


                #if protobuf_message.device_sensor_output.sensor.position == 0x0268FE8F:
                #    dict["L_SHC"] =
                # if protobuf_message.device_sensor_output.sensor.position == 0x
                #print(protobuf_message)
                # new_data_sensor_type = sensor_code_converter(protobuf_message.device_sensor_output.sensor.type)
                # new_data_sensor_position = protobuf_message.device_sensor_output.sensor.position
                # this_sensor = sensor.sensor(new_data_sensor_type, new_data_sensor_position)
                # if this_sensor == my_sensor:
                #     my_sensor.set_data(protobuf_message.timestamp, protobuf_message.device_sensor_output)
                #     if my_sensor.redraw():  # update plot
                #         plt.draw()
                #         plt.pause(0.001)
                #a = 1

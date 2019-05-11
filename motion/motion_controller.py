#Imports.
import paho.mqtt.client as mqtt
import os
from motion_sensor import Motion_sensor

#Callback functions.

#Control the motion sensor according to message.
#The motion sensor has two mode: automation and security.
#If the message is "switchmode", the motion sensor switch to another mode.
def control_motion_sensor(client, motion_sensor, message):
    mes = str(message.payload.decode("utf-8"))
    if mes == "switchmode":
        motion_sensor.switch_mode()

#Set the motion sensor settings according to message. 
#If message is "SETLOCATION location", the motion sensor set its location. Now motion sensor can be controlled by "motion_sensor/location" topic.
#If message is "SETLIGHTTOPIC topic", the motion sensor set which bulbs switch on if the motion is detected.
#If message is "SETCAMERANAME name", the motion sensor set which camera record video if the motion is detected.
def set_settings(client, motion_sensor, message):
    mes = str(message.payload.decode("utf-8"))
    mes_list = mes.split(" ")
    if mes_list[0] == "SETLOCATION":
        client.unsubscribe(motion_sensor.get_location())
        motion_sensor.set_location(mes_list[1])
        client.subscribe(motion_sensor.get_location())
    elif mes_list[0] == "SETLIGHTTOPIC":
        motion_sensor.set_light_topic(mes_list[1])
    elif mes_list[0] == "SETCAMERANAME":
        motion_sensor.set_camera_name(mes_list[1])


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_connect(client, motion_sensor, flags, rc):
    print("connected")
    #When system is connected to network, it start subscribe settings topic and topic for control. 
    client.subscribe(motion_sensor.get_settings_topic())
    client.subscribe(motion_sensor.get_location())     
    
#Client initializing 
def initialize(id, motion_sensor, host, port=1883, username="", password=None, server_tls=False, server_cert=None):
    print("create new instance")
    #create new instance with unique id. In userdata we will create a dictionary where we save color and topic for publishing.
    client = mqtt.Client(client_id= id, userdata= motion_sensor)
    #attach function to callback
    client.message_callback_add(motion_sensor.get_settings_topic(), set_settings)
    client.on_message=control_motion_sensor
    client.on_connect=on_connect
    client.on_subscribe = on_subscribe
    client.on_unsubscribe = on_unsubscribe
    #handle authentication
    if username:
        client.username_pw_set(username, password)
    #handle certification
    if server_tls :
        client.tls_set(server_cert)
    #connect to broker
    client.connect(host, port, 60)
    return client

if __name__ == "__main__":
    #id is IP address
    id = os.popen('ip addr show wlan0').read().split("inet ")[1].split("/")[0]
    motion_sensor = Motion_sensor(7,id)
    client = initialize(motion_sensor.get_name(), motion_sensor, "192.168.1.2", 8883, "Milos", "qwerty", True, "../ca_certificates/ca.crt")
    motion_sensor.set_client(client)
    client.loop_forever()
    
#Imports.
import paho.mqtt.client as mqtt
import os
from camera import Camera
from servo import Servo_motor
from camera_web import Streaming_server, Streaming_handler


#Callback functions.

#Control camera and servo motor according to the message.
#If the message is "record", camera start recording 20 seconds long video.
#If the message is "right", servo turn right.
#If the message is "left", servo turn left.
def control_camera(client, camera, message):
    mes = str(message.payload.decode("utf-8")).strip()
    if mes == "record":
        camera.record_video()
    else:    
        with Servo_motor() as servo_motor:
            if mes == "right":
                servo_motor.right()
            elif mes == "left":
                servo_motor.left()

#Set the camera settings according to the message. 
#If the message is "SETNAME name", the camera set its nickname. It is usually location (kitchen).
def set_settings(client, camera, message):
    mes = str(message.payload.decode("utf-8"))
    mes_list = mes.split(" ")
    if mes_list[0] == "SETNAME":
        client.unsubscribe(camera.get_nickname())
        camera.set_nickname(mes_list[1])
        client.subscribe(camera.get_nickname())
    return

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_connect(client, camera, flags, rc):
    print("connected")
    #When system is connected to network, it start subscribe settings topic and topic for control.
    client.subscribe(camera.get_settings_topic())
    client.subscribe(camera.get_nickname())     
    
#Client initializing 
def initialize(id, camera, host, port=1883, username="", password=None, server_tls=False, server_cert=None):
    print("create new instance")
    #create new instance with unique id. In userdata we save the reference of camera.
    client = mqtt.Client(client_id= id, userdata= camera)
    #attach function to callback
    client.message_callback_add(camera.get_settings_topic(), set_settings)
    client.on_message=control_camera
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
    camera = Camera()
    client = initialize(camera.get_name(), camera, "192.168.1.2", 8883, "Milos", "qwerty", True, "../ca_certificates/ca.crt")
    client.loop_start()
    ip = os.popen('ip addr show wlan0').read().split("inet ")[1].split("/")[0]
    address = (ip, 8000)
    server = Streaming_server(address, Streaming_handler)
    server.serve_forever()
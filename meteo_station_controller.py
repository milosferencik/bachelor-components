#Imports.
import threading
import paho.mqtt.client as mqtt
import socket
import time
from meteo_station_show_output import Meteo_show_output
from meteo_station_sensors import Sensors
from sense_hat import SenseHat

def do(client, sensors, show_output):
    threading.Timer(measurment_interval, do).start()
    result = sensors.get_all_sensors_values()
    show_output.actual_output(result)
    client.publish(sensors.get_topic(), sensors.get_result_string())
    print(sensors.get_result_string())

#Callback functions.

#Set the bulb settings according to message. 
#If message is "SETTOPIC topic", the sensors set topic where it will publish.
def set_settings(client, sensors, message):
    mes = str(message.payload.decode("utf-8"))
    mes_list = mes.split(" ")
    if mes_list[0] == "SETTOPIC":
        sensors.set_topic(mes_list[1])
    return

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_connect(client, sensors, flags, rc):
    print("connected")
    client.subscribe(sensors.get_settings_topic())     
    
#Client initializing 
def initialize(id, sensors, host, port=1883, username="", password=None, server_tls=False, server_cert=None):
    print("create new instance")
    #create new instance with unique id. In userdata we will create a dictionary where we save color and topic for publishing.
    client = mqtt.Client(client_id= id, userdata= sensors)
    #attach function to callback
    client.message_callback_add(sensors.get_settings_topic(), set_settings)
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
    id = socket.gethostbyname(socket.gethostname())
    show_output = Meteo_show_output()
    sensors = Sensors(id)
    sense = SenseHat()
    sense.stick.direction_right = show_output.turn_to_humidity
    sense.stick.direction_up = show_output.turn_to_temperature
    sense.stick.direction_left = show_output.turn_to_pressure
    measurment_interval = 5
    client = initialize(sensors.get_name(), sensors, "192.168.1.2", 8883, "Milos", "qwerty", True, "/etc/mosquitto/ca_certificates/ca.crt")
    #loop
    client.loop_start()
    #do(client, sensors, show_output)
    while True:
        time.sleep(5)
        result = sensors.get_all_sensors_values()
        show_output.set_actual_values(result)
        show_output.actual_output()
        client.publish(sensors.get_topic(), sensors.get_result_string())
        print(sensors.get_result_string())

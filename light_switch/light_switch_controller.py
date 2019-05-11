#Imports.
import paho.mqtt.client as mqtt
import os
from light_switch import Light_switch

#Callback functions.

#Set the light switch settings according to message. 
#If the message is "SETTOPIC topic", the light switch set control topic.
#If the message is "SETCOLOR [255,255,255]", the light switch set color for bulbs which are contoled.
def set_settings(client, switch, message):
    mes = str(message.payload.decode("utf-8"))
    mes_list = mes.split(" ")
    if mes_list[0] == "SETTOPIC":
        switch.set_topic(mes_list[1])
        return

    if mes_list[0] == "SETCOLOR":
        switch.set_color(mes_list[1])
    return

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_connect(client, switch, flags, rc):
    print("connected")
    #When system is connected to network, it start subscribe settings topic.
    client.subscribe(switch.get_settings_topic())     
    
#Client initializing 
def initialize(id, switch, host, port=1883, username="", password=None, server_tls=False, server_cert=None):
    print("create new instance")
    #create new instance with unique id. In userdata we save the reference of light switch.
    client = mqtt.Client(client_id= id, userdata= switch)
    #attach function to callback
    client.message_callback_add(switch.get_settings_topic(), set_settings)
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
    switch = Light_switch(8, 10, 12, id)
    client = initialize(switch.get_name(), switch, "192.168.1.2", 8883, "Milos", "qwerty", True, "../ca_certificates/ca.crt")
    switch.set_client(client)
    client.loop_forever()
    
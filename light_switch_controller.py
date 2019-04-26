#Imports.
import paho.mqtt.client as mqtt
import socket
from light_switch import Light_switch

#pouzivam to ?
def control_lights(client, userdata, switch):
    client.publish(userdata[switch][1], str(userdata[switch][0]))
    return

#Callback functions.

#Set the bulb settings according to message. 
#If message is "SETTOPIC 1 topic", the light switch set that first switch control topic.
#If message is "SETCOLOR 1 topic", the light switch set color for bulbs which are contoled by first switch.
def set_settings(client, switches, message):
    mes = str(message.payload.decode("utf-8"))
    mes_list = mes.split(" ")
    if mes_list[0] == "SETTOPIC":
        #userdata[int(mes_list[1])] [1] = mes_list[2] 
        switches[int(mes_list[1])].set_topic(mes_list[2])
        return

    if mes_list[0] == "SETCOLOR":
        #userdata[int(mes_list[1])] [0] = mes_list[2] 
        switches[int(mes_list[1])].set_color(mes_list[2])
    return

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_connect(client, switches, flags, rc):
    print("connected")
    client.subscribe(switches[1].get_settings_topic())     
    
#Client initializing 
def initialize(id, switches, host, port=1883, username="", password=None, server_tls=False, server_cert=None):
    print("create new instance")
    #create new instance with unique id. In userdata we will create a dictionary where we save color and topic for publishing.
    client = mqtt.Client(client_id= id, userdata= switches)
    #attach function to callback
    client.message_callback_add(switches[1].get_settings_topic(), set_settings)
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
    switches = {1:Light_switch(29, id), 2:Light_switch(30, id), 3:Light_switch(31, id), 4:Light_switch(32, id)}
    client = initialize(switches[1].get_name(), switches, "192.168.1.2", 8883, "Milos", "qwerty", True, "/etc/mosquitto/ca_certificates/ca.crt")
    for number, switch in switches.items():
        switch.set_client(client)
    client.loop_forever()
    
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.add_event_detect(10, GPIO.FALLING, callback=lambda x: control_lights(client, client._userdata, 1), bouncetime=200)

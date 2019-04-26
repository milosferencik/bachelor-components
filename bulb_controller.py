#Imports.
import paho.mqtt.client as mqtt
import socket
from bulb import Bulb
from threading import Thread

#Callback functions.

#Set the bulb lighting according to message. 
#If message is "0", the bulb is turned off.
#If message is "1", the bulb is turned on.
#If message is "2", the bulb is switch to another state.
#If message is "3", the bulb is switch to another state with RGB color.
#If message is "4", the bulb light up with RGB color.
#If message is "5", the bulb has low light.
#If message is "6", the bulb has normal light.
def set_lighting(client, bulb, message):
    mes = str(message.payload.decode("utf-8"))
    mes_list = mes.split(" ")
    #switch off
    if mes_list[0] == "0" :
        bulb.switch_off()
        return
    #switch on
    if mes_list[0] == "1" :
        bulb.switch_on()
        return
    #switch
    if mes_list[0] == "2" :
        bulb.switch()
    #switch with color
    if mes_list[0] == "3" :
        color = eval(mes_list[1])
        bulb.switch_with_color(color)
    #light up with color
    if mes_list[0] == "4" :
        color = eval(mes_list[1])
        thread = Thread(target = bulb.light_up, args= (color,))
        thread.start()
        thread.join()
    #low light 
    if mes_list[0] == "5" :
        bulb.low_light()
    #normal light
    if mes_list[0] == "6" :
        bulb.normal_light()

#Set the bulb settings according to message. 
#If message is "SUBSCRIBE topic1 topic2", the bulb start subscribing topic1 and topic2. Message can contain more topics.
#If message is "UNSUBSCRIBE topic1 topic2" and the topic is subscribed by bulb, the bulb stop subscribing the topic.
#If message is "TOPICS", the bulb publish all topics, which bulb is subsribing, to topic "ovladac/client_id".
def set_settings(client, bulb, message):
    mes = str(message.payload.decode("utf-8"))
    mes_list = mes.split(" ")
    if mes_list[0] == "SUBSCRIBE":
        mes_list.pop(0)
        bulb.add_topics(mes_list)
        topics = [(topic, 1) for topic in mes_list]
        client.subscribe(topics)
        return
    if mes_list[0] == "UNSUBSCRIBE":
        mes_list.pop(0)
        for topic in mes_list:
            if bulb.remove_topics(topic):
                client.unsubscribe(topic)
        return
    if mes_list[0] == "TOPICS":
        client.publish("ovladac/" + bulb.get_name(), " ".join(bulb.get_topics()))
    return

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_connect(client, bulb, flags, rc):
    print("connected")
    client.subscribe(bulb.get_settings_topic())      
    
#Client initializing 
def initialize(id, bulb, host, port=1883, username="", password=None, server_tls=False, server_cert=None):
    print("create new instance")
    #create new instance with unique id. In userdata we will save last_color and subscribed topics.
    client = mqtt.Client(client_id= id, userdata=bulb)
    #attach function to callback
    client.message_callback_add(bulb.get_settings_topic(), set_settings)
    client.on_message=set_lighting
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
    #name is IP address
    name = socket.gethostbyname(socket.gethostname())
    bulb = Bulb(name)
    client = initialize(bulb.get_name(), bulb, "192.168.1.2", 8883, "Milos", "qwerty", True, "/etc/mosquitto/ca_certificates/ca.crt")
    client.loop_forever()
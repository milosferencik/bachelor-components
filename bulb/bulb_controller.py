#Imports.
import paho.mqtt.client as mqtt
import os
from bulb import Bulb
from threading import Thread

#Callback functions.

#Control the bulb lighting according to the message. 
#If the message is "off", the bulb is turned off.
#If the message is "on", the bulb is turned on with last set color.
#If the message is "switch", the bulb is switch to another state.
#If the message is "oncolor <color>", the bulb is turned on with RGB color.
#If the message is "switchcolor <color>", the bulb is switch to another state with RGB color.
#If the message is "lightupcolor <color>", the bulb light up with RGB color.
#If the message is "lowlight", the bulb has low light.
#If the message is "normallight", the bulb has normal light.
#If the message is "switchintensity", the bulb switch to another intensity.
#If the message is "security", the bulb switch on security light, which means 20 second white light and after that red light blinks 30 seconds.
def control_lighting(client, bulb, message):
    mes = str(message.payload.decode("utf-8"))
    mes_list = mes.split(" ")
    #switch off
    if mes_list[0] == "off" :
        bulb.switch_off()
        return
    #switch on
    if mes_list[0] == "on" :
        bulb.switch_on()
        return
    #switch
    if mes_list[0] == "switch" :
        bulb.switch()
    #switch on with color
    if mes_list[0] == "oncolor" :
        color = eval(mes_list[1])
        bulb.switch_on_with_color(color)
    #switch with color
    if mes_list[0] == "switchcolor" :
        color = eval(mes_list[1])
        bulb.switch_with_color(color)
    #light up with color
    if mes_list[0] == "lightupcolor" :
        color = eval(mes_list[1])
        thread = Thread(target = bulb.light_up, args= (color,))
        thread.start()
        thread.join()
    #low light 
    if mes_list[0] == "lowlight" :
        bulb.low_light()
    #normal light
    if mes_list[0] == "normallight" :
        bulb.normal_light()
    #switch intensity
    if mes_list[0] == "switchintensity" :
        bulb.switch_intensity()
    #security light
    if mes_list[0] == "security" :
        bulb.switch_on_security_light()

#Set the bulb settings according to message. 
#If message is "SUBSCRIBE topic1 topic2", the bulb start subscribing topic1 and topic2. Message can contain more topics.
#If message is "UNSUBSCRIBE topic1 topic2" and the topic is subscribed by bulb, the bulb stop subscribing the topic.
#If message is "TOPICS", the bulb publish all topics, which bulb is subsribing, to topic "ovladac/client_id".
#Topic should be the location where the bulb is. The bulb can subscribe topics such as "home/first_floor/kitchen", "home/first_floor", "home".
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
    #When system is connected to network, it start subscribe settings topic.
    client.subscribe(bulb.get_settings_topic())      
    
#Client initializing 
def initialize(id, bulb, host, port=1883, server_tls=False, server_cert=None):
    print("create new instance")
    #create new instance with unique id. In userdata we will save last_color and subscribed topics.
    # If clean_session=False, xsubscription information and queued messages will be retained when the client disconnects.
    client = mqtt.Client(client_id= id, clean_session=False, userdata=bulb)
    #attach function to callback
    client.message_callback_add(bulb.get_settings_topic(), set_settings)
    client.on_message=control_lighting
    client.on_connect=on_connect
    client.on_subscribe = on_subscribe
    client.on_unsubscribe = on_unsubscribe
    #handle certification
    if server_tls :
        client.tls_set(server_cert)
    #connect to broker
    client.connect(host, port, 60)
    return client

if __name__ == "__main__":
    #name is IP address
    id = os.popen('ip addr show wlan0').read().split("inet ")[1].split("/")[0]
    bulb = Bulb(id)
    client = initialize(bulb.get_name(), bulb, "192.168.1.1", 8883, True, "../ca_certificates/ca.crt")
    client.loop_forever()
#Imports.
import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import socket

sense = SenseHat()

#Create an array of 64 [R,G,B] items.
def create_array(color):
    return [color for i in range(64)]

#Set the bulb lighting according to message. 
#If message is "0", the bulb is turned off.
#If message is "1", the bulb is turned on.
#If message is "[R,G,B]", the bulb is turned on with [R,G,B] color.
def set_lighting(client, userdata, mes):
    if mes == "0" :
        sense.clear()
        return
    if mes == "1" :
        sense.set_pixels(create_array(userdata))
        return
    color = eval(mes)
    if type(color) is list:
        for x in color:
            if x < 0 or x > 255:
                return
        for i in range(3):
            userdata[0][i] = color[i]
        sense.set_pixels(create_array(userdata))

#Set the bulb settings according to message. 
#If message is "SUBSCRIBE topic1 topic2", the bulb start subscribing topic1 and topic2. Message can contain more topics.
#If message is "UNSUBSCRIBE topic1 topic2" and the topic is subscribed by bulb, the bulb stop subscribing the topic.
#If message is "TOPICS", the bulb publish all topics, which bulb is subsribing, to topic "ovladac/client_id".
def set_settings(client, userdata, mes):
    mes_list = mes.split(" ")
    if mes_list[0] == "SUBSCRIBE":
        mes_list.pop(0)
        userdata[1].extend(mes_list)
        topics = [(topic, 1) for topic in mes_list]
        client.subscribe(topics)
        return
    if mes_list[0] == "UNSUBSCRIBE":
        mes_list.pop(0)
        for topic in mes_list:
            if topic in userdata[1]:
                userdata[1].remove(topic)
                client.unsubscribe(topic)
        return
    if mes_list[0] == "TOPICS":
        client.publish("ovladac/"+client._client_id.decode('UTF-8'), " ".join(userdata[1]))
    return

#Callback functions.
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_message(client, userdata, message):
    mes = str(message.payload.decode("utf-8"))
    print("message received:" ,mes)
    if message.topic == userdata[1][0]:
        set_settings(client, userdata, mes)
    else :
        set_lighting(client, userdata, mes)

def on_connect(client, userdata, flags, rc):
    print("connected")
    #Subscribe topic settings/client_id
    if userdata[1] == []:
        topic = "settings/"+client._client_id.decode('UTF-8')
        client.subscribe(topic)
        userdata[1].append(topic)       
    
#Client initializing 
def initialize(id, host, port=1883, username="", password=None, server_tls=False, server_cert=None):
    print("create new instance")
    #create new instance with unique id. In userdata we will save last_color and subscribed topics.
    client = mqtt.Client(client_id= id, userdata=([255,255,255],[]))
    #attach function to callback
    client.on_message=on_message
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
    client = initialize(id, "192.168.1.2", 8883, "Milos", "qwerty", True, "/etc/mosquitto/ca_certificates/ca.crt")
    client.loop_forever()
    

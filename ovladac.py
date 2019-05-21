import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with rc: ", rc)
    client.subscribe("settings/#")
    client.subscribe("meteo_sensors/#")
    client.subscribe("ovladac")

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))

def initialize(name, host, port=1883, server_tls=False, server_cert=None):
    print("create new instance")
    #create new instance.
    client = mqtt.Client(client_id= name)
    #attach function to callback
    client.on_message=on_message
    client.on_connect=on_connect
    #handle certification
    if server_tls :
        client.tls_set(server_cert)
        #client.tls_insecure_set(True)
    #connect to broker
    client.connect(host, port, 60)
    return client

def fastsetup(client):
    client.publish("settings/bulb/192.168.1.1", "SUBSCRIBE room")
    client.publish("settings/light_switch/192.168.1.30", "SETTOPIC room")
    client.publish("settings/light_switch/192.168.1.30", "SETCOLOR [200,100,200]")
    client.publish("settings/camera/192.168.1.30", "SETNAME room")
    client.publish("settings/motion_sensor/192.168.1.30", "SETLOCATION room")
    client.publish("settings/motion_sensor/192.168.1.30", "SETLIGHTTOPIC room")
    client.publish("settings/motion_sensor/192.168.1.30", "SETCAMERANAME room")
    client.publish("settings/meteo_sensors/192.168.1.1", "SETLOCATION room" )

if __name__ == "__main__":
    client = initialize("ovladac" ,"192.168.1.1", 8883, True, "ca_certificates/ca.crt")
    client.loop_start()
    while True:
        time.sleep(3)
        topic = input("Topic: ")
        if topic == "fastsetup" :
            fastsetup(client)
        else :
            mes = input("Message: ")
            client.publish(topic, mes)

    

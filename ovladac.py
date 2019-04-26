import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with rc: ", rc)
    client.subscribe("settings/#")
    client.subscribe("temperature/#")

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))

def initialize(name, host, port=1883, username="", password=None, server_tls=False, server_cert=None):
    print("create new instance")
    #create new instance.
    client = mqtt.Client(client_id= name)
    #attach function to callback
    client.on_message=on_message
    client.on_connect=on_connect
    #handle authentication
    if username:
        client.username_pw_set(username, password)
    #handle certification
    if server_tls :
        client.tls_set(server_cert)
        #client.tls_insecure_set(True)
    #connect to broker
    client.connect(host, port, 60)
    return client

if __name__ == "__main__":
   client = initialize("ovladac" ,"192.168.1.2", 8883, "Milos", "qwerty", True, "/usr/local/etc/mosquitto/ca_certificates/ca.crt")
   #client = initialize("ovladac", "192.168.0.101", 1883, "Milos", "qwerty")
   client.loop_start()
   while True:
      time.sleep(3)
      topic = input("Topic: ")
      mes = input("Message: ")
      client.publish(topic, mes)

    

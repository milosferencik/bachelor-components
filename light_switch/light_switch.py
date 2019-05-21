#Imports.
import RPi.GPIO as GPIO
from sense_hat import SenseHat

class Light_switch:
    def __init__(self, channel1, channel2, channel3, id):
        self.name = "light_switch/" + id
        self.settings_topic = "settings/" + self.name
        self.last_color = "[255,255,255]"
        self.topic = ""  # topic, which bulbs subscribe, so we will controll them with this topic
        self.client = None
        # setup the buttons, and add callback functions
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(channel1, GPIO.FALLING, callback=self.switch_on, bouncetime=200)
        GPIO.setup(channel2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(channel2, GPIO.FALLING, callback=self.switch_intensity, bouncetime=200)
        GPIO.setup(channel3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(channel3, GPIO.FALLING, callback=self.switch_off, bouncetime=200)

    def get_name(self):
        return self.name

    def get_settings_topic(self):
        return self.settings_topic

    def set_client(self, client):
        self.client = client

    def get_color(self):
        return self.last_color

    def set_color(self, RGB_color):
        if is_RGB_value(eval(RGB_color)):
           self.last_color = RGB_color 
        else:
            print("RGB color was not assigned, because of incorrect type or value!")

    def set_topic(self, topic):
        self.topic = topic

    def switch_on(self, chanel):
        if self.client and self.topic != "":
            message = "oncolor " + self.last_color
            self.client.publish(self.topic, message)

    def switch_off(self, chanel):
        if self.client and self.topic != "":
            message = "off"
            self.client.publish(self.topic, message)
    
    def switch_intensity(self, chanel):
        if self.client and self.topic != "":
            message = "switchintensity"
            self.client.publish(self.topic, message)

def is_RGB_value(color):
    if type(color) is list and len(color) == 3 :
        if all(x >= 0 and x <= 255 for x in color):
            return True
    return False
#Imports.
#import RPi.GPIO as GPIO
from sense_hat import SenseHat

class Light_switch:
    def __init__(self, pin, id):
        self.name = "light_switch/" + id
        self.settings_topic = "settings/" + self.name
        self.last_color = "[255,255,255]"
        self.topic = ""
        self.client = None
        self.sense = SenseHat()
        self.sense.stick.direction_any = self.on_pressed
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.on_pressed, bouncetime=200)

    def get_name(self):
        return self.name

    def get_settings_topic(self):
        return self.settings_topic

    def set_client(self, client):
        self.client = client

    def get_color(self):
        return self.last_color

    def set_color(self, RGB_color):
        self.last_color = RGB_color
        #if is_RGB_value(RGB_color):
        #   self.last_color = RGB_color 

    def set_topic(self, topic):
        self.topic = topic

    def on_pressed(self, chanel):
        if self.client and self.topic != "":
            message = "4 " + self.last_color
            self.client.publish(self.topic, message)

def is_RGB_value(color):
    if type(color) is list:
        for x in color:
            if x < 0 or x > 255:
                return False
        return True
    return False
import RPi.GPIO as GPIO

class Motion_sensor:
    def __init__(self, channel, id):
        self.name = "motion_sensor/" + id
        self.location = "motion_sensor"
        self.settings_topic = "settings/" + self.name
        self.mode = "automation"  #actual mode of motion sensor
        self.client = None
        self.light_topic = ""
        self.camera_name = ""
        #setup PIR sensor and add callback function
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel, GPIO.IN)
        GPIO.add_event_detect(channel, GPIO.RISING, callback=self.on_motion)
    
    def set_client(self, client):
        self.client = client

    def set_location(self, location):
        self.location = "motion_sensor/" + location

    def set_light_topic(self, topic):
        self.light_topic = topic

    def set_camera_name(self, name):
        self.camera_name = "camera/" + name

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location

    def get_mode(self):
        return self.mode

    def get_settings_topic(self):
        return self.settings_topic

    def on_motion(self, channel):
        if(self.mode == "automation"):
            self.automation()
        else:
            self.security()

    def switch_mode(self):
        if(self.mode != "automation"):
            self.mode = "automation"
        else:
            self.mode = "security"
        message = self.name + " : " + self.mode + " mode!"
        self.client.publish("ovladac", message)

    # automation mode switch on the bulbs
    def automation(self):
        if self.client and self.light_topic != "":
            self.client.publish(self.light_topic, "on")

    # security mode switchs on 20 second white light and records 20 seconds video. After that red light blinks 30 seconds.
    def security(self):
        if self.client and self.camera_name != "":
            if self.light_topic != "":
                self.client.publish(self.light_topic, "security")
            self.client.publish(self.camera_name, "record")





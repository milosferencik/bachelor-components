from sense_hat import SenseHat
import time

class Bulb:
    def __init__(self, id):
        self.sense = SenseHat()
        self.name = "bulb/" + id
        self.settings_topic = "settings/" + self.name
        self.subscribe_topics = []
        self.last_color = [255, 255, 255]
        self.actual_state = False  #False when off, True when on

    def switch_on(self):
        self.sense.clear(self.last_color)
        self.actual_state = True

    def switch_off(self):
        self.sense.clear()
        self.actual_state = False

    def switch(self):
        if self.actual_state:
            self.switch_off()
        else:
            self.switch_on()

    def switch_with_color(self, RGB_color):
        if is_RGB_value(RGB_color):
            self.last_color = RGB_color
            self.switch()

    def light_up(self, RGB_color, time=0.5):
        if is_RGB_value(RGB_color):
            self.last_color = RGB_color
        self.sense.clear()
        self.sense.gamma_reset()
        copy = self.sense.gamma
        self.sense.gamma = [0 for x in copy]
        self.sense.clear(self.last_color)
        for i in range(31,0,-1):
            self.sense.gamma = [x//i for x in copy]
            print(self.sense.gamma)
            time.sleep(time)

    def low_light(self):
        self.sense.low_light = True

    def normal_light(self):
        self.sense.gamma_reset()

    def get_name(self):
        return self.name

    def get_settings_topic(self):
        return self.settings_topic

    def get_topics(self):
        return self.subscribe_topics

    def add_topics(self, topics):
        self.subscribe_topics.extend(topics)

    def remove_topics(self, topic):
        if topic in self.subscribe_topics:
            self.subscribe_topics.remove(topic)
            return True
        return False
        
def is_RGB_value(color):
    if type(color) is list and len(color) == 3 :
        if all(x >= 0 and x <= 255 for x in color):
            return True
    return False


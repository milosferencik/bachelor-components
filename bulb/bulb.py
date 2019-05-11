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
        self.actual_intensity = True #False when low, True when normal

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

    def switch_on_with_color(self, RGB_color):
        if is_RGB_value(RGB_color):
            self.last_color = RGB_color
            self.switch_on()

    def switch_off_with_color(self, RGB_color):
        if is_RGB_value(RGB_color):
            self.last_color = RGB_color
            self.switch_off()

    def switch_with_color(self, RGB_color):
        if is_RGB_value(RGB_color):
            self.last_color = RGB_color
            self.switch()

    def light_up(self, RGB_color, t=0.5):
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
            time.sleep(t)

    def low_light(self):
        self.sense.low_light = True
        self.actual_intensity = False

    def normal_light(self):
        self.sense.gamma_reset()
        self.actual_intensity = True

    def switch_intensity(self):
        if self.actual_intensity:
            self.low_light()
        else:
            self.normal_light()

    def switch_on_security_light(self):
        self.sense.clear([255,255,255])
        time.sleep(20)
        end = time.time() + 30
        change = True
        while time.time() < end:
            if change:
                self.sense.clear([255,0,0])
                time.sleep(1)
                change = False
            else:
                self.sense.clear([0,0,0])
                time.sleep(1)
                change = True    
            

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


import os
import time
from sense_hat import SenseHat
class Sensors:
    def __init__(self, id):
        self.sense = SenseHat()
        self.name = "sensors/" + id
        self.settings_topic = "settings/" + self.name
        self.topic = "temperature"

    def get_name(self):
        return self.name

    def get_settings_topic(self):
        return self.settings_topic

    def set_topic(self, topic):
        self.topic = "temperature/" + topic

    def get_topic(self):
        return self.topic

    def get_temperature(self):
        output = os.popen('vcgencmd measure_temp').readline()
        cpu_temperature = float(output.replace("temp=", "").replace("'C\n", ""))
        temperature_sensor = (self.sense.get_temperature_from_pressure() + self.sense.get_temperature_from_humidity()) / 2
        return temperature_sensor - ((cpu_temperature - temperature_sensor)/5.466)-6
    
    def get_humidity(self):
        return round(self.sense.get_humidity(), 0) 
    
    def get_pressure(self):
        pressure = round(self.sense.get_pressure(), 1)
        if (pressure < 1000) :
            return (pressure, "low")
        if (pressure > 1030) :
            return (pressure, "high")
        return (pressure, "normal")

    def get_result_string(self):
        actual_time = time.strftime("%a, %d %b %Y %H:%M:%S")
        return "%s temperature is %s'C, humidity is %s%%, pressure is %shPA, which is %s pressure." % (actual_time, self.get_temperature(), self.get_humidity(), self.get_pressure()[0], self.get_pressure()[1])

    def get_all_sensors_values(self):
        return (self.get_temperature(), self.get_humidity(), self.get_pressure())

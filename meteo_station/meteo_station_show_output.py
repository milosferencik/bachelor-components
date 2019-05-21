import time
from sense_hat import SenseHat, ACTION_RELEASED

b = [0,0,0] #background
f = [255,255,255] #foreground
BLUE = [0,0,255]
RED = [255,0,0]

zero =  [f,f,f,f,f,f,f,b,
         f,b,b,b,b,b,f,b,
         f,f,f,f,f,f,f,b,
         b,b,b,b,b,b,b,b]
one =   [b,b,b,b,f,b,b,b,
         b,b,b,b,b,f,b,b,
         f,f,f,f,f,f,f,b,
         b,b,b,b,b,b,b,b]
two =   [f,f,f,f,b,b,f,b,
         f,b,b,f,b,b,f,b,
         f,b,b,f,f,f,f,b,
         b,b,b,b,b,b,b,b]
three = [f,b,b,f,b,b,f,b,
         f,b,b,f,b,b,f,b,
         f,f,f,f,f,f,f,b,
         b,b,b,b,b,b,b,b]
four =  [b,b,b,f,f,f,f,b,
         b,b,b,f,b,b,b,b,
         f,f,f,f,f,f,b,b,
         b,b,b,b,b,b,b,b]
five =  [f,b,b,f,f,f,f,b,
         f,b,b,f,b,b,f,b,
         f,f,f,f,b,b,f,b,
         b,b,b,b,b,b,b,b]
six =   [f,f,f,f,b,b,f,b,
         f,b,b,f,b,b,f,b,
         f,f,f,f,f,f,f,b,
         b,b,b,b,b,b,b,b]
seven = [b,b,b,b,b,b,f,b,
         b,b,b,f,b,b,f,b,
         f,f,f,f,f,f,f,b,
         b,b,b,f,b,b,b,b]
eight = [f,f,f,f,f,f,f,b,
         f,b,b,f,b,b,f,b,
         f,f,f,f,f,f,f,b,
         b,b,b,b,b,b,b,b]
nine =  [f,b,b,f,f,f,f,b,
         f,b,b,f,b,b,f,b,
         f,f,f,f,f,f,f,b,
         b,b,b,b,b,b,b,b]

NUMBERS = {0 : zero,
           1 : one,
           2 : two,
           3 : three,
           4 : four,
           5 : five,
           6 : six,
           7 : seven,
           8 : eight,
           9 : nine}

SCREENS = {"temperature" : [b,b,f,f,f,b,b,b,
                            b,b,f,b,f,b,f,f,
                            b,b,f,b,f,b,b,b,
                            b,b,f,RED,f,b,f,f,
                            b,f,RED,RED,RED,f,b,b,
                            f,RED,RED,RED,RED,RED,f,b,
                            b,f,RED,RED,RED,f,b,b,
                            b,b,f,f,f,b,b,b],
           "celzius" : [f,f,f,b,b,f,b,b,
                        f,b,f,b,f,b,f,b,
                        f,f,f,f,b,b,b,f,
                        b,b,b,f,b,b,b,b,
                        b,b,b,f,b,b,b,b,
                        b,b,b,f,b,b,b,f,
                        b,b,b,b,f,b,f,b,
                        b,b,b,b,b,f,b,b],
           "humidity" : [b,b,b,BLUE,b,b,b,b,
                         b,b,BLUE,b,BLUE,b,b,b,
                         b,BLUE,b,b,b,BLUE,b,b,
                         BLUE,b,b,b,b,b,BLUE,b,
                         BLUE,b,BLUE,b,b,b,BLUE,b,
                         BLUE,b,b,BLUE,b,b,BLUE,b,
                         b,BLUE,b,b,b,BLUE,b,b,
                         b,b,BLUE,BLUE,BLUE,b,b,b],
           "percent" : [f,f,f,b,b,b,b,RED,
                        f,b,f,b,b,b,RED,b,
                        f,f,f,b,b,RED,b,b,
                        b,b,b,b,RED,b,b,b,
                        b,b,b,RED,b,b,b,b,
                        b,b,RED,b,b,f,f,f,
                        b,RED,b,b,b,f,b,f,
                        RED,b,b,b,b,f,f,f],
            "pressure" : [f,b,f,b,b,f,b,f,
                         b,f,f,b,b,f,f,b,
                         f,f,f,b,b,f,f,f,
                         b,b,b,b,b,b,b,b,
                         b,b,b,b,b,b,b,b,
                         f,f,f,b,b,f,f,f,
                         b,f,f,b,b,f,f,b,
                         f,b,f,b,b,f,b,f],
           "level" : [RED,b,b,b,b,b,b,b,
                      RED,b,b,b,b,b,b,b,
                      RED,f,f,f,b,b,b,b,
                      b,f,b,BLUE,b,b,b,BLUE,
                      b,f,f,b,BLUE,b,BLUE,b,
                      RED,f,b,b,b,BLUE,b,b,
                      RED,f,f,f,b,b,b,b,
                      RED,b,b,b,b,b,b,b],
           "low" : [b,b,f,f,f,f,b,b,
                    b,b,f,f,f,f,b,b,
                    b,b,f,f,f,f,b,b,
                    b,b,f,f,f,f,b,b,
                    f,f,f,f,f,f,f,f,
                    b,f,f,f,f,f,f,b,
                    b,b,f,f,f,f,b,b,
                    b,b,b,f,f,b,b,b],
           "high" : [b,b,b,f,f,b,b,b,
                     b,b,f,f,f,f,b,b,
                     b,f,f,f,f,f,f,b,
                     f,f,f,f,f,f,f,f,
                     b,b,f,f,f,f,b,b,
                     b,b,f,f,f,f,b,b,
                     b,b,f,f,f,f,b,b,
                     b,b,f,f,f,f,b,b],
            "normal" : [b,f,f,b,f,b,b,b,
                       f,b,b,f,f,b,b,b,
                       f,b,b,f,f,b,b,f,
                       f,b,b,f,f,b,f,b,
                       f,b,b,f,f,f,b,b,
                       f,b,b,f,f,f,b,b,
                       f,b,b,f,f,b,f,b,
                       b,f,f,b,f,b,b,f]}

def invert_matrix(pixel_list) :
    inverted = [[0,0,0] for x in range(64)]
    for i in range(64):
            n = i//8
            z = i%8
            inverted[8*(7-z)+n] = pixel_list[i]
    return inverted

# create value for show on display
def create_value(temp):
    pixels = NUMBERS[abs(temp)//10] + NUMBERS[abs(temp)%10]
    return invert_matrix(pixels)
     
def colour_value(pixel_list, temp) :
    if temp < 0 :
        pixel_list = [[0,0,255] if pixel == f else b for pixel in pixel_list]
        # if temp is negative we add minus
        for x in range(2,6) :
            pixel_list[x] = f
    elif temp < 30 :
        pixel_list = [[255,0,0] if pixel == f else [0,0,255] for pixel in pixel_list]
    else:
        pixel_list = [[255,0,0] if pixel == f else b for pixel in pixel_list]
    return pixel_list

class Meteo_show_output :
    def __init__(self):
        self.actual_values = None # last measured values by sensors
        self.actual_output = self.show_temperature  #the output currently displayed
        self.sense = SenseHat()

    def set_actual_values(self, values):
        self.actual_values = values

    def turn_to_temperature(self, event):
        if event.action != ACTION_RELEASED:
            self.actual_output = self.show_temperature
            self.show_turned_screen("temperature", "celzius")
            self.actual_output()
    
    def turn_to_humidity(self, event):
        if event.action != ACTION_RELEASED:
            self.actual_output = self.show_humidity
            self.show_turned_screen("humidity", "percent")
            self.actual_output()

    def turn_to_pressure(self, event):
        if event.action != ACTION_RELEASED:
            self.actual_output = self.show_pressure
            self.show_turned_screen("pressure", "level")
            self.actual_output()

    def show_temperature(self):
        temp = self.actual_values[0]
        self.sense.set_pixels(colour_value(create_value(round(temp, 0)), round(temp, 0)))
        
    def show_humidity(self):
        humidity = self.actual_values[1]
        self.sense.set_pixels(create_value(humidity))
    
    def show_pressure(self):
        pressure_state = self.actual_values[2][1]
        self.sense.set_pixels(SCREENS[pressure_state])

    # shows what and in which units it will be displayed
    def show_turned_screen(self, name, unit) :
        self.sense.set_pixels(SCREENS[name])
        time.sleep(1)
        self.sense.set_pixels(SCREENS[unit])
        time.sleep(1)
    
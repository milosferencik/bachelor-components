import RPi.GPIO as GPIO
import time

class Servo_motor(object):
    dc = 7
    pwm = None

    def __enter__(self):
        print("__enter__")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
        Servo_motor.pwm = GPIO.PWM(11, 50) #pin, frequency
        Servo_motor.pwm.start(Servo_motor.dc)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        print("__exit__")
        time.sleep(0.5)
        Servo_motor.pwm.stop()
        GPIO.cleanup()
        Servo_motor.pwm = None

    def move(self, value):
        newDc = Servo_motor.dc + value
        if 2.5 <= newDc and newDc <= 11.5:
            Servo_motor.dc = newDc
            Servo_motor.pwm.ChangeDutyCycle(Servo_motor.dc)
            print(Servo_motor.dc)

    def right(self):
        self.move(0.5)     

    def left(self):
        self.move(-0.5)

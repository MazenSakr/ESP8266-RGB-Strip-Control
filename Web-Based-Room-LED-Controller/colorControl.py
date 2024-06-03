import color
import time
from machine import Pin, PWM

REDPIN = 5
GREENPIN = 4
BLUEPIN = 13
FARLEDPIN = 14
NEARLEDPIN = 12

class colorControl:
    def __init__(self, message = (0, 0, 0, 0, 0, 0)):
        red, green, blue, self.nearLed, self.farLed, self.mode = message
        self.color = color.Color(red, green, blue)
        self.oldColor = color.Color(-1,-1,-1) 
        self.animationDelay = 0
        self.lastTime = time.time()
        self.brightnessFlag = 1
        self.setupPins()
        self.set_mode()

    def setupPins(self):
        # Set up RGB LED strip control using transistors connected to ESP pins
        self.red_pin = Pin(REDPIN, Pin.OUT)
        self.green_pin = Pin(GREENPIN, Pin.OUT)
        self.blue_pin = Pin(BLUEPIN, Pin.OUT)
        self.far_led_pin = Pin(FARLEDPIN, Pin.OUT)
        self.near_led_pin = Pin(NEARLEDPIN, Pin.OUT)
        self.red_pwm = PWM(self.red_pin)
        self.green_pwm = PWM(self.green_pin)
        self.blue_pwm = PWM(self.blue_pin)
        self.far_led_pwm = PWM(self.far_led_pin)
        self.near_led_pwm = PWM(self.near_led_pin)
        self.red_pwm.freq(1000)  # Set PWM frequency to 1kHz
        self.green_pwm.freq(1000)  # Set PWM frequency to 1kHz
        self.blue_pwm.freq(1000)  # Set PWM frequency to 1kHz
        self.far_led_pwm.freq(1000)
        self.near_led_pwm.freq(1000)

    def modifyColors(self, message):
        red, green, blue, nearLed, farLed, mode = message
        if self.oldColor.red != red or self.oldColor.green != green or self.oldColor.blue != blue or self.farLed != farLed or self.nearLed != nearLed or self.mode != mode :
            self.color = color.Color(red, green, blue)
            self.oldColor = color.Color(red, green, blue)
            self.animationDelay = float(101-self.color.Value)/200
            self.farLed = farLed
            self.nearLed = nearLed
            self.mode = mode
            if self.mode == 1:
                self.color.Saturation = 85
                self.color.Value = 100
                self.color.Hue = 0
                self.color.convRGB()
            elif self.mode == 2:
                self.color.Value = 0
                self.color.convRGB()
                self.animationDelay = 0.1
            self.far_led_pwm.duty(self.farLed*5)
            self.near_led_pwm.duty(self.nearLed*5)
            self.set_mode()
        else:
            self.set_mode()

    def set_rgb(self):
        # Set PWM duty cycle for each color
        self.red_pwm.duty(int(self.color.red)*5)
        self.green_pwm.duty(int(self.color.green)*5)
        self.blue_pwm.duty(int(self.color.blue)*5)

    def set_mode(self):
        # Set the mode of the strip
        if self.mode == 0:
            self.set_rgb()
        elif self.mode == 1:        
            self.rainbow_cycle()
        elif self.mode == 2:
            self.brightness_cycle()
        elif self.mode == 3:
            self.timeBasedColor()
        else:
            print("Invalid mode")

    def brightness_cycle(self):
        # Cycle between 0 and full brightness of selected color
        if time.time() - self.lastTime > self.animationDelay:
            self.lastTime = time.time()
            if self.brightnessFlag == 1:
                self.color.Value = self.color.Value + 1
                if self.color.Value == 100:
                    self.brightnessFlag = 0
            else:
                self.color.Value = self.color.Value - 1
                if self.color.Value == 0:
                    self.brightnessFlag = 1
            self.color.convRGB()
            self.set_rgb()

    def rainbow_cycle(self):
        # Cycle between colors of the rainbow
        if time.time() - self.lastTime > self.animationDelay:
            self.lastTime = time.time()
            self.color.Hue = (self.color.Hue + 1) % 360
            self.color.convRGB()
            self.set_rgb()

    def timeBasedColor(self):
        # changes the color of the strip depending on the time of day
        print("timeBasedColor")

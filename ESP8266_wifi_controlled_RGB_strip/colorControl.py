import color
import time
from machine import Pin, PWM

REDPIN = 5
GREENPIN = 12
BLUEPIN = 14

class colorControl:
    def __init__(self, red, green, blue):
        self.color = color.Color(red, green, blue)
        self.oldColor = color.Color(-1,-1,-1) 
        self.mode = 0
        self.animationDelay = 0
        self.lastTime = time.time()
        self.brightnessFlag = 1
        self.setupPins()
        self.set_mode(0)

    def setupPins(self):
        # Set up RGB LED strip control using transistors connected to ESP pins
        self.red_pin = Pin(REDPIN, Pin.OUT)
        self.green_pin = Pin(GREENPIN, Pin.OUT)
        self.blue_pin = Pin(BLUEPIN, Pin.OUT)
        self.red_pwm = PWM(self.red_pin)
        self.green_pwm = PWM(self.green_pin)
        self.blue_pwm = PWM(self.blue_pin)
        self.red_pwm.freq(1000)  # Set PWM frequency to 1kHz
        self.green_pwm.freq(1000)  # Set PWM frequency to 1kHz
        self.blue_pwm.freq(1000)  # Set PWM frequency to 1kHz

    def modifyColors(self, mode, red, green, blue):
        if self.oldColor.red != red or self.oldColor.green != green or self.oldColor.blue != blue or self.mode != mode:
            self.color = color.Color(red, green, blue)
            self.oldColor = color.Color(red, green, blue)
            self.animationDelay = float(101-self.color.Value)/200
            if mode == 1:
                self.color.Saturation = 85
                self.color.Value = 100
                self.color.Hue = 0
                self.color.convRGB()
            elif mode == 2:
                self.color.Value = 0
                self.color.convRGB()
                self.animationDelay = 0.1
            self.set_mode(mode)
        else:
            self.set_mode(mode)

    def set_rgb(self):
        # Set PWM duty cycle for each color
        self.red_pwm.duty(int(self.color.red)*5)
        self.green_pwm.duty(int(self.color.green)*5)
        self.blue_pwm.duty(int(self.color.blue)*5)

    def set_mode(self, mode):
        # Set the mode of the strip
        self.mode = mode
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


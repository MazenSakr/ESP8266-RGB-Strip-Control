import machine
import time
import usocket as socket
import network
from machine import Pin, PWM
import uasyncio
import random
import color
import sys

REDPIN = 5
GREENPIN = 14
BLUEPIN = 12

class RGBStripControl():

    def __init__(self):
        self.color = color.Color(20,20,20)
        self.mode = 0
        self.startAP()
        self.setupServer()
        self.setupPins()
        self.set_rgb()
        self.handle_request()
        #uasyncio.run(self.start_coro())


    def startAP(self):
        # Set up access point
        self.accessPoint = network.WLAN(network.AP_IF)
        self.accessPoint .active(True)
        self.accessPoint .config(essid='TeamRGB', authmode=network.AUTH_OPEN)
        self.accessPoint .ifconfig(('192.168.1.4', '255.255.255.0', '192.168.1.4', '8.8.8.8'))
        print(self.accessPoint .ifconfig())
    
    def setupServer(self):
        # Start web server
        self.websock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.websock.setblocking(False)
        self.websock.settimeout(0.1)
        self.websock.bind(('', 80))
        self.websock.listen(5)

    # async def start_coro(self):
    #     print("loop started")
    #     self.loop1 = uasyncio.get_event_loop()
    #     self.loop1.run_forever()
    #     while True:
    #         try :
    #             uasyncio.wait_for_ms(self.handle_request(), 100)
    #         except:
    #             pass
    #         await uasyncio.sleep_ms(1000)

    def setupPins(self):
        # Set up RGB LED strip control using transistors connected to ESP pins
        self.r_pin = Pin(REDPIN, Pin.OUT)
        self.g_pin = Pin(GREENPIN, Pin.OUT)
        self.b_pin = Pin(BLUEPIN, Pin.OUT)
        self.r_pwm = PWM(self.r_pin)
        self.g_pwm = PWM(self.g_pin)
        self.b_pwm = PWM(self.b_pin)
        self.r_pwm.freq(100) # Set PWM frequency to 1kHz
        self.g_pwm.freq(100) # Set PWM frequency to 1kHz
        self.b_pwm.freq(100) # Set PWM frequency to 1kHz

    def handle_request(self):
        while True:
            # Accept incoming connection
            try:
                self.connection, _ = self.websock.accept()
                request = self.connection.recv(1024)
                print(request)
                self.connection.close()
                request = str(request)
                if 'GET /rgb?' in request:
                    # Parse RGB values from request
                    start_index = request.index('GET /rgb?') + 8
                    end_index = request.index(' HTTP')
                    rgb_values = request[start_index:end_index].split('&')
                    self.color.red = int(rgb_values[0].split('=')[1],16)
                    self.color.green = int(rgb_values[1].split('=')[1],16)
                    self.color.blue = int(rgb_values[2].split('=')[1],16)
                    self.mode = int(rgb_values[3].split('=')[1])
            except:
                pass
            # Set RGB values and mode
            self.set_rgb()
            self.set_mode()
            
    def set_rgb(self):
        # Set PWM duty cycle for each color
        self.r_pwm.duty(self.color.red*5)
        self.g_pwm.duty(self.color.green*5)
        self.b_pwm.duty(self.color.blue*5)

    def set_mode(self):
        # Set mode for LED strip operation
        if self.mode == 0:
            pass
        elif self.mode == 1:
            self.brightness_cycle()
        elif self.mode == 2:
            self.rainbow_cycle()
        elif self.mode == 3:
            self.bounce()
        else:
            print("Invalid mode")

    def brightness_cycle(self):
        # Cycle between 0 and full brightness of selected color
        self.color.convHSV()
        brightness = self.color.Value
        while True :
            for i in range(brightness+1):
                self.color.Value = i
                self.color.convRGB()
                self.set_rgb()
                time.sleep(0.01)
            for i in range(brightness+1):
                self.color.Value = 255 - i
                self.color.convRGB()
                self.set_rgb()
                time.sleep(0.01)

    def rainbow_cycle(self):
        # Cycle between colors of the rainbow
        self.color.convHSV()
        delay = self.color.Value/2550
        while True:
            for i in range(360):
                self.color.Hue = i
                self.color.convRGB()
                self.set_rgb()
                time.sleep(delay)

    def bounce(self):
        # Bounce between different colors
        self.color.convHSV()
        delay = self.color.Value/2550
        while True:
            self.color.red = random.randint(0, 255)
            self.color.green = random.randint(0, 255)
            self.color.blue = random.randint(0, 255)
            time.sleep(delay)

Stripcontroller = RGBStripControl()


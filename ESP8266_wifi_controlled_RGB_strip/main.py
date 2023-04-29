import machine
import time
import usocket as socket
import network
from machine import Pin, PWM
import _thread
import random

# Set up access point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='TeamRGB', authmode=network.AUTH_OPEN)
ap.ifconfig(('192.168.1.4', '255.255.255.0', '192.168.1.4', '8.8.8.8'))
print(ap.ifconfig())

# Set up web server
def handle_request(request):
    request = str(request)
    if 'GET /rgb?' in request:
        # Parse RGB values from request
        start_index = request.index('GET /rgb?') + 8
        end_index = request.index(' HTTP')
        rgb_values = request[start_index:end_index].split('&')
        r = int(rgb_values[0].split('=')[1],16)
        g = int(rgb_values[1].split('=')[1],16)
        b = int(rgb_values[2].split('=')[1],16)
        mode = int(rgb_values[3].split('=')[1])
        
        # Set RGB values and mode
        set_rgb(r, g, b)
        set_mode(mode, r, g, b)
        
def set_rgb(r, g, b):
    # Set PWM duty cycle for each color
    global r_pwm, g_pwm, b_pwm
    r_pwm.duty(r)
    g_pwm.duty(g)
    b_pwm.duty(b)

def set_mode(mode, r, g, b):
    # Set mode for LED strip operation
    threadStatus = False
    time.sleep(0.01)
    threadStatus = True
    if mode == 0:
        pass
    elif mode == 1:
        _thread.start_new_thread(brightness_cycle, (r, g, b))
    elif mode == 2:
        _thread.start_new_thread(rainbow_cycle, (r, g, b))
    elif mode == 3:
        _thread.start_new_thread(bounce, (r, g, b))
    else:
        print("Invalid mode")

def brightness_cycle(r, g, b):
    # Cycle between 0 and full brightness of selected color
    global threadStatus
    Hue,Saturation,Value = RGBToHSV(r, g, b)
    brightness = 0
    while threadStatus :
        for i in range(Value+1):
            brightness = i
            r,g,b = HSVToRGB(Hue, Saturation, brightness)
            set_rgb(int(r),int(g),int(b))
            time.sleep(0.01)
        for i in range(Value+1):
            brightness = 255-i
            r,g,b = HSVToRGB(Hue, Saturation, brightness)
            set_rgb(int(r),int(g),int(b))
            time.sleep(0.01)


def rainbow_cycle(r, g, b):
    # Cycle between colors of the rainbow
    global threadStatus
    Hue,Saturation,Value = RGBToHSV(r, g, b)
    delay = Value/2550
    while threadStatus:
        for i in range(360):
            Hue = i
            r,g,b = HSVToRGB(Hue, Saturation, Value)
            set_rgb(int(r),int(g),int(b))
            time.sleep(delay)

def bounce(r, g, b):
    # Bounce between different colors
    global threadStatus
    Hue,Saturation,Value = RGBToHSV(r, g, b)
    delay = Value/2550
    while threadStatus:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        time.sleep(delay)

def RGBToHSV(red,green,blue):
    Value = max(red, green, blue)
    min_value = min(red, green, blue)
    Saturation = (Value - min_value) / Value
    Hue = 0 if Value == red == green == blue  else \
        60 * (green - blue) / (Value - min_value) if Value == red != green != blue else \
        60 * (blue - red) / (Value - min_value) + 120 if Value == green != red != blue else \
        60 * (red - green) / (Value - min_value) + 240 if Value == blue != red != green else \
        60 * ((green - red) / (Value - min_value) + 2) if Value != red != green != blue else None
    return Hue, Saturation, Value

def HSVToRGB(Hue, Saturation, Value):
    Chroma = Value * Saturation
    X = Chroma * (1 - abs((Hue / 60) % 2 - 1))
    m = Value - Chroma
    (Red, Green, Blue) = (Chroma, X, 0) if 0 <= Hue < 60 else \
           (X, Chroma, 0) if 60 <= Hue < 120 else \
           (0, Chroma, X) if 120 <= Hue < 180 else \
           (0, X, Chroma) if 180 <= Hue < 240 else \
           (X, 0, Chroma) if 240 <= Hue < 300 else \
           (Chroma, 0, X)
    (Red, Green, Blue) = ((Red + m) * 255, (Green + m) * 255, (Blue + m) * 255)
    return Red, Green, Blue


# Set up RGB LED strip control using transistors connected to ESP pins
r_pin = Pin(5) # Replace with actual pin number
g_pin = Pin(4) # Replace with actual pin number
b_pin = Pin(0) # Replace with actual pin number

r_pwm = PWM(r_pin)
g_pwm = PWM(g_pin)
b_pwm = PWM(b_pin)

r_pwm.freq(1000) # Set PWM frequency to 1kHz
g_pwm.freq(1000) # Set PWM frequency to 1kHz
b_pwm.freq(1000) # Set PWM frequency to 1kHz



# Start web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

threadStatus = True
set_rgb(255,255,255)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    handle_request(request)
    conn.close()

# import time
# def RGBToHSV(red,green,blue):
#     Value = max(red, green, blue)
#     min_value = min(red, green, blue)
#     Saturation = (Value - min_value) / Value
#     Hue = 0 if Value == red == green == blue  else \
#         60 * (green - blue) / (Value - min_value) if Value == red != green != blue else \
#         60 * (blue - red) / (Value - min_value) + 120 if Value == green != red != blue else \
#         120 if green == 255 and red == 0 and blue == 0 else \
#         60 * (red - green) / (Value - min_value) + 240 if Value == blue != red != green else \
#         240 if  blue == 255 and red == 0 and green == 0  else \
#         60 * ((green - red) / (Value - min_value) + 2) if Value != red != green != blue else 0
#     return Hue, Saturation, Value

# def HSVToRGB(Hue, Saturation, Value):
#     Value = Value / 255
#     Chroma = Value * Saturation
#     X = Chroma * (1 - abs((Hue / 60) % 2 - 1))
#     m = Value - Chroma
#     (Red, Green, Blue) = (Chroma, X, 0) if 0 <= Hue < 60 else \
#            (X, Chroma, 0) if 60 <= Hue < 120 else \
#            (0, Chroma, X) if 120 <= Hue < 180 else \
#            (0, X, Chroma) if 180 <= Hue < 240 else \
#            (X, 0, Chroma) if 240 <= Hue < 300 else \
#            (Chroma, 0, X)
#     (Red, Green, Blue) = ((Red + m) * 255, (Green + m) * 255, (Blue + m) * 255)
#     return Red, Green, Blue

# def brightness_cycle(r, g, b):
#     # Cycle between 0 and full brightness of selected color
#     Hue,Saturation,Value = RGBToHSV(r, g, b)
#     brightness = 0
#     for i in range(Value+1):
#         brightness = i
#         r,g,b = HSVToRGB(Hue, Saturation, brightness)
#         print(int(r),int(g),int(b))
#         time.sleep(0.01)
#     for i in range(Value+1):
#         brightness = 255-i
#         r,g,b = HSVToRGB(Hue, Saturation, brightness)
#         print(int(r),int(g),int(b))
#         time.sleep(0.01)


# def rainbow_cycle(r, g, b):
#     # Cycle between colors of the rainbow
#     Hue,Saturation,Value = RGBToHSV(r, g, b)
#     delay = Value/2550
#     for i in range(361):
#         Hue = i
#         r,g,b = HSVToRGB(Hue, Saturation, Value)
#         print(int(r),int(g),int(b))
#         time.sleep(delay)


# r = 123
# g = 213
# b = 198
# rainbow_cycle(r, g, b)



# # Hue,Saturation,Value = RGBToHSV(r, g, b)
# # brightness = 0
# # print(Hue, Saturation, Value)
# # for i in range(Value+1):
# #     brightness = i
# #     r,g,b = HSVToRGB(Hue, Saturation, brightness)
# #     print(int(r),int(g),int(b))
# #     time.sleep(0.01)
# # for i in range(Value+1):
# #     brightness = 255-i
# #     r,g,b = HSVToRGB(Hue, Saturation, brightness)
# #     print(int(r),int(g),int(b))
# #     time.sleep(0.01)
import machine
import time
import usocket as socket
import network
from machine import Pin, PWM
import random

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='TeamRGB', authmode=network.AUTH_OPEN)
ap.ifconfig(('192.168.1.4', '255.255.255.0', '192.168.1.4', '8.8.8.8'))
print(ap.ifconfig())

# Start web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("help")
    request = conn.recv(1024)
    print(request)
    conn.close()

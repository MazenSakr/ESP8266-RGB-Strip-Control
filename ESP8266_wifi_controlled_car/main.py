import network
try:
  import usocket as socket
except:
  import socket
import machine
import gc
gc.collect()
# Set up access point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='car2', authmode=network.AUTH_WPA_WPA2_PSK, password='mazenscar2')
ap.ifconfig(('192.168.1.4', '255.255.255.0', '192.168.1.4', '8.8.8.8'))
print('Access Point created successfully')
print(ap.ifconfig())


# Set up web server
html = '''<!DOCTYPE html>
<html>
    <head> <title>Car 1</title> </head>
    <body bgcolor="#808080">
        <script>
            function move(direction) {
                var xhr = new XMLHttpRequest();
                xhr.open("GET", "http://192.168.1.4/?direction="+direction, true);
                xhr.send();
            }
        </script>
        <div style="text-align:center">
            <button style="background-color:#009FF9; color:white; font-size:60px" onclick="move('forward')">UP</button>
            <br><br>
            <button style="background-color:#009FF9; color:white; font-size:60px; margin-right:10px" onclick="move('left')" >LEFT</button>
            <button style="background-color:#009FF9; color:white; font-size:60px; margin-left:10px" onclick="move('stop')" >STOP</button>
            <button style="background-color:#009FF9; color:white; font-size:60px; margin-left:10px" onclick="move('right')" >RIGHT</button>
            <br><br>
            <button style="background-color:#009FF9; color:white; font-size:60px" onclick="move('backward')" >DOWN</button>
        </div>
    </body>
</html>'''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.1.4', 80))
s.listen(5)

# Set up motor driver
motor1_pin1 = machine.Pin(14, machine.Pin.OUT)
motor1_pin2 = machine.Pin(12, machine.Pin.OUT)
motor2_pin1 = machine.Pin(5, machine.Pin.OUT)
motor2_pin2 = machine.Pin(4, machine.Pin.OUT)

def move_forward():
    motor1_pin1.value(1)
    motor1_pin2.value(0)
    motor2_pin1.value(1)
    motor2_pin2.value(0)

def move_backward():
    motor1_pin1.value(0)
    motor1_pin2.value(1)
    motor2_pin1.value(0)
    motor2_pin2.value(1)

def move_left():
    motor1_pin1.value(0)
    motor1_pin2.value(1)
    motor2_pin1.value(1)
    motor2_pin2.value(0)

def move_right():
    motor1_pin1.value(1)
    motor1_pin2.value(0)
    motor2_pin1.value(0)
    motor2_pin2.value(1)

def stop():
    motor1_pin1.value(0)
    motor1_pin2.value(0)
    motor2_pin1.value(0)
    motor2_pin2.value(0)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    response = html
    conn.send(response.encode())
    request = conn.recv(1024).decode()
    
    direction = None
    if 'direction' in request:
        direction = request.split('direction=')[1].split(' ')[0]
    
        if direction == 'forward':
            move_forward()
        elif direction == 'backward':
            move_backward()
        elif direction == 'left':
            move_left()
        elif direction == 'right':
            move_right()
        elif direction == 'stop':
            stop()

    
    
    conn.close()


import usocket as socket
import network
import colorControl

RESPONSE = '''HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {
            font-family: 'Barlow', sans-serif;
            font-weight: 400;
            font-style: normal;
            text-align: center;
            background-color: rgb(79,80,89);
            color: #FFFFFF; /* Set the text color to white */
        }
        input[type='submit'] {
            background-color: rgb(225, 90, 52); /* Set the button color to orange */
            border: none; /* Remove default border */
            padding: 10px 20px; /* Add some padding for better appearance */
            cursor: pointer; /* Change cursor on hover */
            color: #FFFFFF; /* Ensure the submit button text is also white */
        }
    </style>
    <title>Mazen's Vibe Machine</title>
</head>
<body>
    <h1>Mazen's Vibe Machine</h1>
    <form action="http://192.168.0.175" method='GET'>
        <label for='color'>Color:</label>
        <input type='color' id='color' name='color'>
        <br><br>
        <label for='mode'>Mode:</label>
        <select id='mode' name='mode'>
            <option value='0'>Normal</option>
            <option value='1'>Rainbow</option>
            <option value='2'>Dimmer</option>
            <option value='3'>Time-based</option>
        </select>
        <br><br>
        <label for = "farLED">Far LED</label>
        <input type="range" min="0" max="255" value="127" id="farLED" name="farLED">
        <br><br>
        <label for = "nearLED">Near LED</label>
        <input type="range" min="0" max="255" value="127" id="nearLED" name="nearLED">
        <br><br>
        <input type='submit' value='Submit'>
    </form>
</body>
</html>
'''

class RGBStripServer():

    def __init__(self):
        self.connectToWifi("sakr", "mwm#@537")
        self.message = (20, 20, 20, 20, 20, 0)
        self.colorControl = colorControl.colorControl(self.message)
        self.setupServer()
        self.handle_request()

    def connectToWifi(self, ssid, password):
        # Connect to WiFi
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.ifconfig(('192.168.0.175', '255.255.255.0', '192.168.0.1', '192.168.0.1'))
        self.wlan.connect(ssid, password)
        while not self.wlan.isconnected():
            print("Waiting to connect to WiFi...")
        print("IP address:", self.wlan.ifconfig())

    def setupServer(self):
        # Start web server
        self.websock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.websock.setblocking(False)
        self.websock.settimeout(0.1)
        self.websock.bind(('',  80))
        self.websock.listen(1)

    def handle_request(self):
        while True:
            self.colorControl.modifyColors(self.message)
            try: # Format Recieved : GET /color=%23000000&mode=0&farLED=127&nearLED=127
                self.connection, _ = self.websock.accept()
                print("Connected: ",self.connection,_)
                self.connection.write(RESPONSE)
                request = self.connection.recv(4096)
                self.connection.close()
                print("Request:", request)
                color = request[request.index(b'color=')+9:request.index(b'mode=')-1]
                print("Color:", color)
                red, green, blue = int(color[0:2],16), int(color[2:4],16), int(color[4:6],16)
                print("Red:", red, "Green:", green, "Blue:", blue)
                mode = int(request[request.index(b'mode=')+5:request.index(b'HTTP')-1],16)
                print("Mode:", mode)
                farLED = int(request[request.index(b'farLED=')+7:request.index(b'nearLED')-1])
                nearLED = int(request[request.index(b'nearLED=')+8:])
                print("Far LED:", farLED, "Near LED:", nearLED)
                self.message = (red, green, blue, mode, farLED, nearLED)
                [print(i) for i in self.message]
            except OSError:
                pass
            
Stripcontroller = RGBStripServer()

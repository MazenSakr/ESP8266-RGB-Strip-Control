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
    <form action="http://192.168.0.7:8080" method='GET'>
        <label for='color'>Color:</label>
        <input type='color' id='color' name='color'><br><br>
        <label for='mode'>Mode:</label>
        <select id='mode' name='mode'>
            <option value='0'>Normal</option>
            <option value='1'>Rainbow</option>
            <option value='2'>Dimmer</option>
            <option value='3'>Time-based</option>
        </select><br><br>
        <input type='submit' value='Submit'>
    </form>
</body>
</html>
'''

class RGBStripServer():

    def __init__(self):
        self.connectToWifi("YOUR SSID", "YOUR PASSWORD")
        self.message = (0, 20, 20, 20)
        self.colorControl = colorControl.colorControl(self.message)
        self.setupSendServer()
        self.setupReceiveServer()
        self.handle_request()

    def connectToWifi(self, ssid, password):
        # Connect to WiFi
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(ssid, password)
        while not self.wlan.isconnected():
            print("Waiting to connect to WiFi...")
        print("IP address:", self.wlan.ifconfig())

    def setupSendServer(self):
        # Start web server
        self.sendWebsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sendWebsock.setblocking(False)
        self.sendWebsock.settimeout(0.1)
        self.sendWebsock.bind(('192.168.0.7',  80))
        self.sendWebsock.listen(1)

    def setupReceiveServer(self):
        # Start web server
        self.recieveWebsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recieveWebsock.setblocking(False)
        self.recieveWebsock.settimeout(0.1)
        self.recieveWebsock.bind(("192.168.0.7", 8080))
        self.recieveWebsock.listen(1)

    def handle_request(self):
        while True:
            self.colorControl.update(self.message)
            # Accept incoming connection
            try:
                self.sendConnection, _ = self.sendWebsock.accept()
                print("send",self.sendConnection,_)
                self.sendConnection.write(RESPONSE)
                self.sendConnection.close()
            except OSError:
                pass

            try: # format : GET /color=%23ae3d3d&mode=2
                self.recieveConnection, _ = self.recieveWebsock.accept()
                print("recieve",self.recieveConnection,_)
                request = self.recieveConnection.recv(4096)
                self.recieveConnection.write("HTTP/1.1 200 OK\r\n")
                self.recieveConnection.close()
                mode = int(request[request.index(b'mode=')+5:request.index(b'HTTP')-1],16)
                print(mode)
                color = request[request.index(b'color=')+9:request.index(b'mode=')-1]
                print(color)
                red, green, blue = int(color[0:2],16), int(color[2:4],16), int(color[4:6],16)
                print(red, green, blue)
                self.message = (mode, red, green, blue)
                [print(i) for i in self.message]
                self.colorControl.update(self.message)
            except OSError:
                pass
            
Stripcontroller = RGBStripServer()

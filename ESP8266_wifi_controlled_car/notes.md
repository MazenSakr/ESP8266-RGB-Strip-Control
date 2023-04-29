//contains commands to manipulate code and flash esp and all notes and pitfalls

# Flashing

1. Connect ESP8266 to PC via USB
2. use command: esptool --port <your comm port for windows> erase_flash #to erase flash
3. use command: esptool --port <your comm port for windows> --baud 460800 write_flash --flash_size=detect -fm dout 0 .\esp8266-20220618-v1.19.1.bin #path to bin file #to flash esp8266 with micropython
note: for non nodemcu esp boards remove -fm dout 0, or if command is not working, to test after flash micropython should start an access point with ssid: MicroPython-xxxxxx and password: 12345678 where xxxxxx is the last 6 digits of the MAC address of the ESP8266, then connect with it using tera term to control it using built in repl(python shell)
4. use command: ampy --port <your comm port for windows> put main.py #to upload main.py to esp8266
note: main.py is run after boot.py on esp startup
5. to remove main.py from esp8266 use command: ampy --port <your comm port for windows> rm main.py
or alternatively use command: ampy --port <your comm port for windows> rmdir / #to remove all files from esp8266
or alternatively open repl and import os and use os.remove('main.py') to remove main.py and os.listdir() to list files on esp8266.

-- or you can just use pyMakr VSCode extension for easy use😅


# connections and pinouts

To flash bare esp8266 modules : <https://www.hackster.io/brian-lough/3-simple-ways-of-programming-an-esp8266-12x-module-c514ee>

nodemcu pinout: <https://www.instructables.com/id/ESP8266-NodeMCU-12E-Pinout/>

esp8266 micropython reference:  <https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html>

circuitry: power(18650 batteries) ->5v regulator -> 3.3v regulator -> esp8266 -> motor driver (control)
                                 |                                |-> led(system on indicator)
                                 |->(L298N)Motor driver -> motors (power)

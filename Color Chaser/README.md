# Color Chaser

Color Chaser is an exciting game where the player takes control of a red dot on an WS2811 addressable RGB LED strip. The objective of the game is to press the button when the red dot aligns with one of the green dots on the LED strip. Successfully pressing the button at the right time increases the player's score by one point and advances them to the next level. As the player progresses, the red dot becomes faster, adding to the challenge.

## Hardware Components

The Color Chaser project is built using the following hardware components:

- Arduino Uno: The Arduino Uno serves as the main controller for the game.
- 2N2222 NPN Transistor: This transistor is used to control a 12V buzzer, which provides audio feedback when the player wins a level or loses the game.
- 7448 7-Segment BCD Common Cathode Decoders: Two of these decoders are connected to two seven-segment displays, which are used to display the player's score.
- Button: A button is connected to ground through a 1kOhm resistor and is used by the player to interact with the game.
- WS2811 Addressable RGB LED Strip: This LED strip forms the playing field for the game, with the red and green dots representing the player and targets, respectively.
- 12V Battery Pack and 5V Regulator: The entire project is powered by a 12V battery pack, with a 5V regulator used to power the decoders.

## How to Play

To play Color Chaser, follow these steps:

1. Connect the hardware components as described in the project documentation.
2. Upload the game code to the Arduino Uno.
3. Power on the project using the 12V battery pack.
4. The red dot will start moving along the LED strip.
5. Press the button when the red dot aligns with one of the green dots.
6. If you press the button at the right time, your score will increase by one point and you will advance to the next level.
7. If you press the button at the wrong time or miss a green dot, you will lose the game.
8. The buzzer will sound to indicate whether you have won a level or lost the game.
9. The game will continue until you choose to stop or until you lose.

Enjoy playing Color Chaser and challenge yourself to achieve the highest score!

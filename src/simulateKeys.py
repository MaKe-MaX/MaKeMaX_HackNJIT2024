import serial
from pynput.keyboard import Controller, Key
import time

# Setup serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace with your port

# Setup keyboard controller
keyboard = Controller()

# Define thresholds for joystick movement (adjust based on your joystick)
THRESHOLD_LOW = -50
THRESHOLD_HIGH = 50

while True:
    # Read serial data from Arduino
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        
        try:
            # Parse the X and Y values from the serial output
            x_str, y_str = line.split(" ")
            x_value = int(x_str.split(":")[1])
            y_value = int(y_str.split(":")[1])
        except (IndexError, ValueError):
            continue  # Skip if parsing fails

        # Determine direction and send corresponding key
        if x_value < THRESHOLD_LOW:  # Left
            keyboard.press('a')
            keyboard.release('a')
        elif x_value > THRESHOLD_HIGH:  # Right
            keyboard.press('d')
            keyboard.release('d')

        if y_value < THRESHOLD_LOW:  # Up
            keyboard.press('w')
            keyboard.release('w')
        elif y_value > THRESHOLD_HIGH:  # Down
            keyboard.press('s')
            keyboard.release('s')
        
        # Small delay to avoid excessive input spamming
        time.sleep(0.1)

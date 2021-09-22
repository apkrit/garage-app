# Imports library for GPIO interface.
import RPi.GPIO as GPIO
# Prints info of GPIO device.
print(GPIO.RPI_INFO)

# Imports time library for sleep.
import time

# Sets GPI port of IR sensor.
pir_port = 4

# Setup GPIO mode to Broadcom.
# Need to look more into how this works. 
GPIO.setmode(GPIO.BCM)

# Sets input pin to the IR pin.  
GPIO.setup(pir_port,  GPIO.IN)

# Permanent loop unitil user cancels with Ctrl C.
try:
    while (True):
        # If the input is 0, sensor detects an obstacle.
        # Need to look into the reasoning behind this - 
        # Seems as though it should be the other way around.
        if GPIO.input(pir_port) == 0:
            print("Garage Door is Closed.")
        else:
            # If not 0, then sensor detects nothing. 
            print("Garage Door is Open.")
        # Waits for 1 second for sensor input. 
        time.sleep(1)
# If user presses Ctrl C, clean GPIO and exit. 
except KeyboardInterrupt:
    GPIO.cleanup()
print("Exiting")


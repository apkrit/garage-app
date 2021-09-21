# import library for GPIO
import RPi.GPIO as GPIO
# print GPIO info
print(GPIO.RPI_INFO)

# time library
import time

# Port of PIR
pir_port = 4

# Setup GPIO mode to Broadcom
GPIO.setmode(GPIO.BCM)

# configure the pin as input pin
GPIO.setup(pir_port,  GPIO.IN)

# do the loop
try:
    while (True):
        # if the input is zero, nobody is there at the sensor
        if GPIO.input(pir_port) == 0:
            print("Garage Door is Closed.")
        else:
            # found somebody at the sensor
            print("Garage Door is Open.")
        # wait for 1 sec whether you detect someone or not
        time.sleep(1)
# If user presses ^C cleanup the GPIO
except KeyboardInterrupt:
    GPIO.cleanup()
print("Exiting")


# Import os for env variabes 
import os

# Import environment variables
from dotenv import load_dotenv
load_dotenv()

# Imports Python interface for PostgreSQL database
import psycopg2

# Imports library for GPIO interface.
import RPi.GPIO as GPIO
# Prints info of GPIO device.
print(GPIO.RPI_INFO)
print()

# Imports library for displaying time..
import datetime

# Imports time library for sleep.
import time

# Twilio import for texting
from twilio.rest import Client

# Creates database connection
conn = psycopg2.connect('dbname=garagedb')
cursor = conn.cursor()

def get_all_sensor_input():
    query = """
    SELECT
        *
    FROM
        sensorlog
    """
    cursor.execute(query)
    return cursor.fetchall()

def add_sensor_record(status, time):
    query = """
    INSERT INTO
        sensorlog
    VALUES
        (%s, %s)
    """
    values = (status, time)
    cursor.execute(query, values)

def send_message():
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    twiliophone = os.environ['TWILIO_PHONENUMBER']
    userphone = os.environ['USER_PHONENUMBER']
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                              body='Garage door may have been left open.',
                              from_=twiliophone,
                              to=userphone
                          )
    # print(message.sid)

sensor_results = get_all_sensor_input()

print('---------------------------------------------')
print('Printing garagedb sensorlog table content')
for result in sensor_results:
    print(result)
print('End of garagedb sensorlog table results')
print('---------------------------------------------')
print()

# Sets GPI port of IR sensor.
pir_port = 4

# Setup GPIO mode to Broadcom.
# Need to look more into how this works. 
GPIO.setmode(GPIO.BCM)

# Sets input pin to the IR pin.  
GPIO.setup(pir_port,  GPIO.IN)

# Permanent loop unitil user cancels with Ctrl C.
lastStatus = None
print('---------------------------------------------')
print('Begining display of live sensor results:')

timeOpen = 0
try:
    while (True):
        currentTime = datetime.datetime.now()
        currentTime = currentTime.strftime("%I:%M:%S %p on %m-%d-%Y")
        garageStatus = None
        # If the input is 0, sensor detects an obstacle, so door is closed.
        # Need to look into the reasoning behind this - 
        # Seems as though it should be the other way around.
        if GPIO.input(pir_port) == 0:
            garageStatus = 'Closed'
            timeOpen = 0
        else:
            # If not 0, then sensor detects nothing, so door is open.
            garageStatus = 'Open'
        # Store initial startup value to sensorlog db
        if lastStatus == None:
            print('Initial state saved to sensorlog db.')
            add_sensor_record(garageStatus, currentTime)
            conn.commit()
        if garageStatus != lastStatus and lastStatus != None:
            print('Garage status has changed!')
            add_sensor_record(garageStatus, currentTime)
            conn.commit()
        if garageStatus == 'Open':
            timeOpen += 1
            if timeOpen > 10:
                print("Sending Text Message!")
                send_message()
                timeOpen = 0
        lastStatus = garageStatus
        garageStatusReadout = f"Garage door is {garageStatus} at {currentTime}"
        print(garageStatusReadout)
        # Waits for 1 second for sensor input. 
        time.sleep(1)
# If user presses Ctrl C, clean GPIO and exit. 
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    cursor.close()
    conn.close()
print("Exiting")
print('---------------------------------------------')

#Created by Justin Alderson
#A motion detecting program for Raspberry Pi
#Uses a PIR sensor to detect motion and records time and date of motion
#Motions are uploaded to Google firebase every hour
#Latest motion can be checked by pushing button to display on LCD

from time import sleep
from datetime import datetime
import pickle
from motion import Movement
from firebase import firebase
import json
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

#firebase
firebase = firebase.FirebaseApplication('https://your_database_name.firebaseio.com', None)
upload = []

#LCD
lcd_columns = 16
lcd_rows = 2
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)
led =  digitalio.DigitalInOut(board.D11)
pir =  digitalio.DigitalInOut(board.D7)
button =  digitalio.DigitalInOut(board.D8)
#Set directions of pins
led.direction = digitalio.Direction.OUTPUT
pir.direction = digitalio.Direction.INPUT
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, lcd_columns, lcd_rows)

#Variables
Current_State = 0
Previous_State = 0
count = 0
save_count = 0
oclock = 0
movement_detected = []
lcd_line_1 = ''
lcd_line_2 = ''

print("Home movement counter preparing to launch.")

#show last movement on button push
def show():
    print('Button pushed')
    # combine both lines into one update to the display, show last movement
    lcd.message = lcd_line_2 + lcd_line_1
    print('Button method finished')
    sleep(3)
    # wipe LCD screen
    lcd.clear()

#save method called on shutdown and at 500 saved_count variable
def save():
    data = movement_detected
    save_file = open('/home/pi/Home_Monitor/data.dat','wb')
    pickle.dump(data, save_file)
    save_file.close()

#Load data on program restart
try:

    load_file = open('/home/pi/Home_Monitor/data.dat', 'rb')
    data = pickle.load(load_file)
    movement_detected = data
    count = len(movement_detected)
    load_file.close()

except EOFError:
    pass

# wipe LCD screen before we start
lcd.clear()

try:

    sleep(2)

    print("Launching.")

    while True:
        #get datetime
        oclock = datetime.now()

        #Get the input from the PIR
        Current_State = pir.value#GPIO.input(GPIO_PIR)
        #LED off
        led.value = False

        #save at intervals of.. to prevent over saving...
        if save_count > 500 and oclock.minute == 59:
            save()
            save_count = 0

        #sense button pushed
        if button.value == False:
            show()

        #every 59th minute upload data to friebase
        if oclock.minute == 59:
            firebase.put('/Motion/',"Motion Hour: %d" %oclock.hour,upload)
            #sleep for 1 min 5 sec
            sleep(65.0)

        #If PIR detects something a one will be returned
        if Current_State == 1:
           #Create motion class object here...
           detected = Movement(count,str(oclock))
           #convert to json object dictionary
           ##work out how and what time to upload data, below code all works, then how to read data
           converted = json.dumps(detected.__dict__)
           upload.append(converted)
           upload.append(converted)

           #Append to list here for saving to pi if program shutdown
           movement_detected.append(detected)

           movement = "Motion: %d" %detected.getCount()
           print (movement)
           print(datetime.today())
           sleep(0.2)
           count += 1
           save_count += 1
           #LED on
           led.value = True

           # date and time
           lcd_line_1 = oclock.strftime('\n%b %d  %H:%M:%S')

           # current motion number
           lcd_line_2 = movement

           # combine both lines into one update to the display
           lcd.message = lcd_line_2 + lcd_line_1

           sleep(3)
           # wipe LCD screen before we start
           lcd.clear()

        sleep(0.2)

#Will accept Control C in the terminal to exit program. It will print Shutdown message.
except KeyboardInterrupt:
    #save on shutdown
    save()
    print("Home Movement Detector Shutdown")

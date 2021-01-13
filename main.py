import grove_rgb_lcd as glcd
import grovepi as gpi
import datetime as dt
from urllib.request import urlretrieve
from zipfile import ZipFile
import csv

#Put data from our data files into variables, update the data files first if there is an internet connection
def getData():
    #Download the zip file with covid data, if there is an internet connection
    try:
        urlretrieve('https://files.ssi.dk/covid19/overvagning/data/data-epidemiologisk-rapport-20112020-1rip', 'C:/Users/WaffleFlower/Desktop/Skole/Informatik/Raspberry Pi projekt/data.zip' )
    except:
        print('new data not retrieved')

    #Unzip the file we're interested in
    with ZipFile('C:/Users/WaffleFlower/Desktop/Skole/Informatik/Raspberry Pi projekt/data.zip', 'r') as zip_ref:
        zip_ref.extract('Municipality_cases_time_series.csv', 'C:/Users/WaffleFlower/Desktop/Skole/Informatik/Raspberry Pi projekt')

    #Read and save data for Copenhagen, Aarhus, Odense, Aalborg, and Esbjerg from the csv-file
    with open('C:/Users/WaffleFlower/Desktop/Skole/Informatik/Raspberry Pi projekt/Municipality_cases_time_series.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next(csv_reader)
        row = list(csv_reader)[-1]
        return row[0], row[2], row[3], row[15], row[17], row[24]
    print('done reading data')

date, copenhagen, aarhus, aalborg, esbjerg, odense = getData()

#GrovePi code
state = 0

button = 2
led = 3
led_cop = 4
led_aar = 5
led_aal = 6
led_esb = 7
led_ode = 8
leds = [4,5,6,7,8]
pressing = 0

#Retrieve current time, used to update data every hour
hour = dt.datetime.now().hour

#Set inputs and outputs
gpi.pinMode(button, 'INPUT')
for pin in range(3, 9):
    gpi.pinMode(pin, 'OUTPUT')

while 1:
    #Change state by 1 when the button is pressed
    if gpi.digitalRead(button) == 1:
        if not pressing:
            state += 1
            if state > 5:
                state = 0
            pressing = 1
    else:
        pressing = 0
    
    #State 0 gives instructions
    if state == 0:
        glcd.setText("press to\nchange city")
    
    #Copenhagen
    if state == 1:
        glcd.setText('Copenhagen ' + str(copenhagen)[0:5] + '\ndate ' + str(date))

    #Aarhus
    if state == 2:
        glcd.setText('Aarhus ' + str(aarhus)[0:5] + '\ndate ' + str(date))

    #Aalborg
    if state == 3:
        glcd.setText('Aalborg ' + str(aalborg)[0:5] + '\ndate ' + str(date))

    #Esbjerg
    if state == 4:
        glcd.setText('Esbjerg ' + str(esbjerg)[0:5] + '\ndate ' + str(date))

    #Odsense
    if state == 5:
        glcd.setText('Odense ' + str(odense)[0:5] + '\ndate ' + str(date))

    #Try to update the data every hour
    if hour != dt.datetime.now().hour:
        date, copenhagen, aarhus, aalborg, esbjerg, odense = getData()
        hour = dt.datetime.now().hour

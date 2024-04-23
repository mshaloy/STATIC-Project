#---------------------
#Main
#Created by Mallory Shaloy 3/2024
#CCofCO RockSat-X 2024
#---------------------
from sensor import Sensor
from activation import Activation
from bme280Sensor import BME280Sensor
from tmp36Sensor import TMP36Sensor
from startracker import StarTracker
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
#import adafruit_pca9685
#from adafruit_servokit import ServoKit   
import time
import multiprocessing


def runSensor_file(sensor):
    _sensor = sensor
    _sensor.takeReading()
    _sensor.recordToFile()

def runSensor_console(sensor):
    _sensor = sensor
    _sensor.takeReading()
    _sensor.printToConsole()

if __name__ == "__main__":
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)              # analog to digital converter board
        bme = BME280Sensor("BME", "Metric", 0.1)        # Set up BME280 sensor; Will take readings continuously every 0.1 seconds
        tmp = TMP36Sensor("TMP", ads, "Metric", 0.1, 0)      # Set up TMP36 sensor; Will take readings continuously every 0.1 seconds

        t1 = multiprocessing.Process(target=runSensor_file(bme))    #assigning running bme280 sensor to process 1 (number for id purposes only)
        t2 = multiprocessing.Process(target=runSensor_file(tmp))    #assigning running tmp36 sensor to proccess 2 (number for id purposes only)

        #starting individual proccesses
        t1.start()
        t2.start()

        #begin regolith sequence
        regolith = Activation()
        regolith.eventActivation(26, 5, 180)        #listening for TE-2 on GPIO 26; activating GPIO 5 for 180 seconds

        #initiate star tracker sequence
        star_tracker = StarTracker()
        angle = -30.0       #initial angle is -30 degrees
        image_number = 0    #inital image number
        star_tracker.moveCamera(angle)

        #take 4 images at each of 3 star tracker locations; repeat 3 times
        for i in range(3):
            for i in range(3):
                for i in range(4):
                    star_tracker.takePicture(image_number)
                    image_number += 1
                angle += 30
                star_tracker.moveCamera(angle)
            angle = -30
            star_tracker.moveCamera(angle)
        
        #LOST software calculations
        star_tracker.trackerCalculation()

        t1.join()
        t2.join()

    except:
        pass

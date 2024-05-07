#---------------------
#Main
#Created by Mallory Shaloy 3/2024
#CCofCO RockSat-X 2024
#---------------------
import sensor
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
    
def runExperiment():
    #begin regolith sequence
        regolith = Activation()
        regolith.eventActivation(5, 26, 180)        #listening for TE-2 on GPIO 5; activating GPIO 26 for 180 seconds

        #initiate star tracker sequence
        star_tracker = StarTracker(25)
        angle = -120.0       #initial angle is -120 degrees to account for angle adjustment interaction with looping
        image_number = 0    #inital image number

        #take 3 images at each of 3 star tracker locations; repeat 3 times
        for i in range(3):
            angle = -120
            for i in range(3):
                angle += 60		#adjust camera angle through 3 locations -60, 0, and 60 degrees
                star_tracker.moveCamera(angle)
                for i in range(3):
                    star_tracker.takePicture(image_number)
                    image_number += 1		#increment image number on captured images
            

        #LOST software calculations
        star_tracker.trackerCalculation(image_number)
        
if __name__ == "__main__":
    try:
        i2c = busio.I2C(board.SCL, board.SDA)	#setup i2c interface
        ads = ADS.ADS1115(i2c)              # setup analog to digital converter board
        bme = BME280Sensor("BME", "Metric", 0.1, 10)        # Set up BME280 sensor; Will take readings continuously every 0.1 seconds
        tmp = TMP36Sensor("TMP", ads, "Metric", 0.1, 1, 10)      # Set up TMP36 sensor; Will take readings continuously every 0.1 seconds
        t1 = multiprocessing.Process(target=runSensor_file(bme))    #assigning running bme280 sensor to process 1 (number for id purposes only)
        t2 = multiprocessing.Process(target=runSensor_file(tmp))    #assigning running tmp36 sensor to process 2 (number for id purposes only)
        t3 = multiprocessing.Process(target=runExperiment())		#assigning running experiment functions to process 3 (number for id purposes only)

        #starting individual proccesses. One sensor per process plus experiment sequence on one proccess.
        t1.start()
        t2.start()
        t3.start()

        t3.join()
        t1.join()
        t2.join()

    except Exception as e:
        print(e)
 
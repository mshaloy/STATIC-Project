#---------------------
#General Sensor Class
#Created by Mallory Shaloy 03/2024
#CCofCO RockSat-X 2024
#---------------------

import csv
import time

class Sensor:

    #initilize the sensor, default units are Imperial, default sleep time is 1 second
    def __init__(self, name, units="Imperial", sleep_t=1, repeat=0):
        self.name = name

        #unit options:
        #Imperial: fahrenheit, feet
        #Metric: celsius, meters
        #Mixed 1: celsius, feet
        #Mixed 2: fahrenheit, meters
        if units == "Imperial" or units == "Metric" or units == "Mixed 1" or units == "Mixed 2":
             self.units = units
             self._set_header()
        else:
            raise Exception("Invalid units.")
        
        self.sleep_time = sleep_t # time between readings
        self.repeat = repeat # Number of readings to take. 0 indicates continuous readings until stopped
        self.data = []

    #set header for output
    def _set_header(self):
        if self.units == "Imperial" or self.units == "Mixed 2":
            self.header = ["Temperature in F"]
        else:
            self.header = ["Temperature in C"]
        
    #take sensor reading
    def takeReading(self):
        reading_data = []
        return reading_data

    #output readings to CSV file
    def recordToFile(self):
        filename = f"{self.name}.csv"

        #create csv writer object and add the specified header
        with open(filename, 'w', newline='') as csvfile:
            sensor_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            sensor_writer.writerow(self.header)

            if self.repeat == 0:
                #continually take sensor reading, write reading to csv file, then sleep for specified interval
                while True:
                    self.data = self.takeReading()
                    sensor_writer.writerow(self.data)
                    time.sleep(self.sleep_time)
            else:
                #take specific number of sensor readings, then terminate
                for i in range(self.repeat):
                    self.data = self.takeReading()
                    sensor_writer.writerow(self.data)
                    time.sleep(self.sleep_time)

    #print readings to console
    def printToConsole(self):
        print(self.name + self.units)
        print(self.header)
        if self.repeat == 0:
            #continually take sensor readings, print to the console, then sleep for specified interval
            while True:
                self.data = self.takeReading()
                print(self.data)
                time.sleep(self.sleep_time)
        else:
            for i in range(self.repeat):
                self.data = self.takeReading()
                print(self.data)
                time.sleep(self.sleep_time)

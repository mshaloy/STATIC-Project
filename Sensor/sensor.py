#---------------------
#General Sensor Class
#Created by Mallory Shaloy 03/2024
#CCofCO RockSat-X 2024
#---------------------

import csv
import time

class Sensor:

    
    def __init__(self, name, units="Imperial", sleep_t=1.0, repeat=0):
        """
            param: string name: The name of the sensor. 
            param: string units: The units of sensor outputs. Default is Imperial.
                             Valid options:
                             Imperial: Fahrenheit, feet
                             Metric: Celsius, meters
                             Mixed 1: Celsius, feet
                             Mixed 2: Fahrenheit, meters
            param: float sleep_t: The amount of time between sequential sensor reads. 
                              Default is 1 second.
            param: int repeat: The number of times to repeat readings. 0 indicates continual readings. 
                           Default is 0.
        """
        self._name = name
        
        #input validation
        if units == "Imperial" or units == "Metric" or units == "Mixed 1" or units == "Mixed 2":
             self._units = units
             self._set_header()
        else:
            raise Exception("Invalid units."+units)
        
        if sleep_t < 0:
            raise Exception("Sleep time must be greater than or equal to 0 seconds.")
        self._sleep_time = sleep_t
        
        if repeat < 0:
            raise Exception("Number of repeats must be greater than or equal to 0.")
        self._repeat = repeat
        self._data = []

    def _set_header(self):
        """Set header for data output"""
        if self._units == "Imperial" or self._units == "Mixed 2":
            self._header = ["Temperature in F"]
        else:
            self._header = ["Temperature in C"]
        
    def takeReading(self):
        """Take sensor reading. Returns reading data as an array."""
        _reading_data = []
        return _reading_data

    def recordToFile(self):
        """Records sensor readings to csv file with single header line. Filename is the name given to the sensor."""
        filename = f"{self._name}.csv"

        #create csv writer object and add the specified header
        with open(filename, 'w', newline='') as csvfile:
            sensor_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            sensor_writer.writerow(self._header)

            if self._repeat == 0:
                #continually take sensor reading, write reading to csv file, then sleep for specified interval
                while True:
                    self._data = self.takeReading()
                    sensor_writer.writerow(self._data)
                    time.sleep(self._sleep_time)
            else:
                #take specific number of sensor readings, then terminate
                for i in range(self._repeat):
                    self._data = self.takeReading()
                    sensor_writer.writerow(self._data)
                    time.sleep(self._sleep_time)

    def printToConsole(self):
        """Prints sensor readings to console with a single header line."""
        print(self._header)
        if self._repeat == 0:
            #continually take sensor readings, print to the console, then sleep for specified interval
            while True:
                self._data = self.takeReading()
                print(self._data)
                time.sleep(self._sleep_time)
        else:
            for i in range(self._repeat):
                self._data = self.takeReading()
                print(self._data)
                time.sleep(self._sleep_time)

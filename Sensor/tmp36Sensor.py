#---------------------
#Sensor Class for TPM36 sensor using Adafruit ADS1115 analog to digital converter breakout board
#Created by Mallory Shaloy 3/2024
#CCofCO RockSat-X 2024
#---------------------

import sensor
from adafruit_ads1x15.analog_in import AnalogIn

class TMP36Sensor(sensor):
    """Class for the TMP36 temperature sensor, supported by the Adafruit ADS1115 analog to digital converter breakout board."""
    def __init__(self, name, board, units="Imperial", sleep_t=1.0, pin_number=0, repeat=0):
        """Create and initialize a TMP36 sensor object. 
        param: string name: The sensor name.
        param: ADS1115 board: The ADS1115 board interface the sensor is connected to.
        param: string units: The units of sensor outputs. Default is Imperial.
                            Valid options:
                            Imperial: Fahrenheit
                            Metric: Celsius
        param: float sleep_t: The amount of time between sequential sensor reads. 
                              Default is 1 second.
        param: int pin_number: The ADS1115 input pin to which the TMP36 sensor is connected. Default is 0.
                                0 to 3 are valid.
        param: int repeat: The number of times to repeat readings. 0 indicates continual readings. 
                           Default is 0.
        """
        #unit options: "Imperial" or "Metric"
        if units != "Imperial" and units != "Metric":
            raise Exception("Invalid units for this sensor.")
        elif pin_number < 0 or pin_number > 4:
            raise Exception("Invalid pin number.")
        else:
            super.__init__(self, name, units, sleep_t, repeat)
            self.pin_number = pin_number  # 0 to 3 are valid. Value of pin where sensor is connected

        #setup Adafruit ADS1115 analog to digital converter board with TMP36 sensor
        self.tmp = AnalogIn(board.ads, self.pin_number) 

    def takeReading(self):
        reading_data = []
        temp_in_C = (self.tmp.voltage - 0.5) * 100  # 0.5 voltage differential based on TMP36 data sheet
        if self.units == "Imperial":
            temp_in_F = (temp_in_C * (9/5)) + 32  # convert to Fahrenheit
            reading_data = [temp_in_F]
            return reading_data
        else:
            reading_data = [temp_in_C]
            return reading_data
            

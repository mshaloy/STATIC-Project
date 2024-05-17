#---------------------
#Sensor Class for Sparkfun BME280 sensor
#Created by Mallory Shaloy 3/2024
#CCofCO RockSat-X 2024
#---------------------

from sensor import Sensor
import qwiic_bme280


class BME280Sensor(Sensor):
    """Class for the Sparkfun BME280 atmospheric sensor."""

    def __init__(self, name, units="Imperial", sleep_t=1.0, repeat = 0, filter=1, standby=0, temp_oversample=1, pressure_oversample=1, humidity_oversample=1):
        """Create and initialize a BME280 sensor object. 
            param: string name: The sensor name.
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
            param: int filter: The filter coefficient which sets the level of noise reduction.
                            0 to 4 are valid values. The default is 1.
                            0 = filter off
                            1 = coefficients = 2
                            2 = coefficients = 4
                            3 = coefficients = 8
                            4 = coefficients = 16
            param: int standby: The time between readings on the sensor chip itself.
                            0 to 7 are valid inputs. Default is 0.
                            0, 0.5ms
                            1, 62.5ms
                            2, 125ms
                            3, 250ms
                            4, 500ms
                            5, 1000ms
                            6, 10ms
                            7, 20ms
            param: int temp_oversample: The temperature oversampling value. 
                                    1 to 16 are valid values. Default is 1.
            param: int pressure_oversample: The pressure oversampling value.
                                        1 to 16 are valid values. Default is 1.
            param: int humidity_oversample: The humidity oversampling value.
                                        1 to 16 are valid values. Default is 1.
            BME280 is hard coded to normal mode for continuous sensor readings.
        """
    
        super().__init__(name, units, sleep_t, repeat)
        self._set_header()

        self._bme280 = qwiic_bme280.QwiicBme280()
        self._bme280.begin()

        #setup sensor
        if filter >= 0 and filter <= 4:
            self._bme280.filter = filter  # 0 to 4 are valid. Filter coefficient. For noise reduction
        else:
            raise Exception("Invalid filter number. Valid values are 0 to 4.")
        
        if standby >= 0 and standby <= 7:
            self._bme280.standby_time = standby   # 0 to 7 are valid. Time between readings. 0 is 0.5ms
        else:
            raise Exception("Invalid standby value. Valid values are 1 to 16")
        
        if temp_oversample >= 1 and temp_oversample <= 16:
            self._bme280.over_sample = temp_oversample # 1 to 16 are valid. 0 disables temperature sensing and is not supported
        else:
            raise Exception("Invalid temperature oversampling value. Valid values are 1 to 16.")
        
        if pressure_oversample >= 1 and pressure_oversample <= 16:
            self._bme280.pressure_oversample = pressure_oversample # 1 to 16 are valid. 0 disables pressure sensing and is not supported
        else:
            raise Exception("Invalid pressure oversampling value. Valid values are 1 to 16.")
        
        if humidity_oversample >= 1 and pressure_oversample <= 16:
            self._bme280.humidity_oversample = humidity_oversample # 0 to 16 are valid. 0 disables pressure sensing and is not supported
        else:
            raise Exception("Invalid humidity oversampling value. Valid values are 1 to 16.")

        self._bme280.mode = self._bme280.MODE_NORMAL # Normal mode takes continuous readings - no other modes supported


    def _set_header(self):
        """Sets header for outputs"""
        if self._units == "Imperial" or self._units == "Mixed 2":
            self._header = ["Temperature in F"]
        else:
            self._header = ["Temperature in C"]

        if self._units == "Imperial" or self._units == "Mixed 1":
            self._header.append("Altitude in Feet")
        else:
            self._header.append("Altitude in meters")
        self._header.append("Pressure")
        self._header.append("Humidity")

    def takeReading(self):
        """Take sensor reading. Returns reading data as an array."""
        reading_data = []
        if self._units == "Imperial" or self._units == "Mixed 2":
            reading_data = [self._bme280.temperature_fahrenheit]
        else:
            reading_data = [self._bme280.temperature_celsius]


        if self._units == "Imperial" or self._units == "Mixed 1":
            reading_data.append(self._bme280.altitude_feet)
        else:
            reading_data.append(self._bme280.altitude_meters)

        reading_data.append(self._bme280.pressure)
        reading_data.append(self._bme280.humidity)

        return reading_data

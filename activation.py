#---------------------
#Class for managing Raspberry Pi GPIO pin activation and deactivations - native GPIO or with Adafruit servo/PWM hat
#Created by Mallory Shaloy 4/2024
#CCofCO RockSat-X 2024
#---------------------
from gpiozero import Button, LED
import board
import busio
import adafruit_pca9685

from time import sleep

class Activation:

    def __init__(self, board=None, channel = -1):
        """Create and initialize an activation event object.
            param: PWM board: The instance of an Adafruit servo/PWM hat being utilized if any.
                        Value of None indicates direct connection to GPIO pins.
            param: int channel: The value of the channel to which the component to be activated is connected.
                            0 to 15 are valid values. 
                            Default value of -1 indications direct connection to GPIO pins.
        """
        self._board = board
        self._channel = channel

    def eventActivation(self, listening_pin, activation_pin, activation_duration=0):
        """Event based activation. Direct GPIO connections only.
            param: int listening_pin: The pin on which the Raspberry Pi is expecting an activation input.
            param: int activation_pin: The pin which will be activated when the activation input has been recieved.
            param: float activation_duraion: How long the activated pin should remain active in seconds
        """
        _listening_pin = Button(listening_pin, pull_up = False)
        _activated_pin = LED(activation_pin)

        _listening_pin.wait_for_press()
        _activated_pin.on()             # turns component on
        if activation_duration >= 0:
            sleep(activation_duration)  # wait time between activation and deactivation
            _activated_pin.off()        # turns component off
        else:
            raise Exception("Invalid duration. Values must be 0 or greater.")
    
    def boardEvent(self, listening_pin, activation_duration=0):
        """Event based activation. For use with PWM board only.
            param: int listening_pin: The pin on which the Raspberry Pi is expecting an activation input.
            param: float activation_duraion: How long the activated channel should remain active in seconds
        """
        if self._board == None:
            raise Exception("This function requires the use of a compatible PWM board")
        elif self._channel < 0 or self._channel > 15:
            raise Exception("Invalid channel number. Value must be 0 to 15")
        elif activation_duration < 0:
            raise Exception("Invalid duration. Values must be 0 or greater.")
        else:
            _listening_pin = Button(listening_pin, pull_up = False)
            _activation_channel = self._board.channels[self._channel]
            _activation_channel.duty_cycle = 0xffff     # maximum activation value on PWM hat channel - turns component on
            sleep(activation_duration)
            _activation_channel.duty_cycle = 0          # minimum activation value on PWM hat - turns component off
            
    def pinActivation(self, activation_pin, activation_duration=0):
        """Direct pin activation and deactivation. Direct GPIO connections only.
            param: int activation_pin: The pin which will be activated.
            param: float activation_duraion: How long the activated pin should remain active in seconds
        """
        _activated_pin = LED(activation_pin)
        _activated_pin.on()             # turns component on
        if activation_duration >= 0:
            sleep(activation_duration)  # wait time between activation and deactivation
            _activated_pin.off()        # turns component off
        else:
            raise Exception("Invalid duration. Values must be 0 or greater.")

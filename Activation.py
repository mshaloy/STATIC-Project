#---------------------
#Class for managing Raspberry Pi GPIO pin activation and deactivations
#Created by Mallory Shaloy 4/2024
#CCofCO RockSat-X 2024
#---------------------
from gpiozero import Button, LED
from time import sleep

class Activation:

    def __init__(self):
        pass

    def event_activation(self, listening_pin, activation_pin, activation_duration=0):
        _listening_pin = Button(listening_pin, pull_up = False)
        _activated_pin = LED(activation_pin)

        _listening_pin.wait_for_press()
        _activated_pin.on()
        if activation_duration >= 0:
            sleep(activation_duration)
            _activated_pin.off()
        else:
            raise Exception("Invalid duration. Values must be 0 or greater.")
    


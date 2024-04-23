#---------------------
#Star Tracker Class using Raspberry Pi HD camera and 5V servo motor for imaging and LOST software for image proccessing
#Created by Mallory Shaloy 4/2024
#CCofCO RockSat-X 2024
#---------------------

from picamera2 import Picamera2
from time import sleep
from gpiozero import AngularServo

class StarTracker():
    """Class for controlling Star Tracker using a Raspberry Pi HD camera and servo motor, optionally controlled by Adafruit servo/PWM hat. 
        Also controls computational software for star tracking."""
    def __init__(self, board=None, channel=-1):
        """
            param: PWM board: The instance of an Adafruit servo/PWM hat being utilized if any.
                            Value of None indicates direct connection to GPIO pins.
            param: int channel: The value of the channel to which the component to be activated is connected.
                            0 to 15 are valid values. 
                            Default value of -1 indications direct connection to GPIO pins.
        """
        self.board = board
        self.channel = channel
        self.camera = Picamera2()

    def moveCamera(self, pin_number, angle=0):          # moves servo to specified angle. For use with direct GPIO connection only
        _tracker_servo = AngularServo(pin_number)
        _tracker_servo.angle = angle

    def boardMoveCamera(self, angle=0):         # moves the servo to a specified angle. For use with PWM board only
        if self.board == None:
            raise Exception("This function requires the use of a compatible PWM board")
        elif self.channel < 0 or self.channel > 15:
            raise Exception("Invalid channel number. Value must be 0 to 15")
        else:
            self.board.servo[self.channel].angle = [angle]

    def takePicture(self, image_number):    # Takes a single camera image, saved as a png
        self.camera.start()
        sleep(1)
        self.camera.capture_file(f"image{image_number}.png")

    def trackerCalculation():       # TODO
        sleep(30)

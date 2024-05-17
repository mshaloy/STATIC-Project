#---------------------
#Star Tracker Class using Raspberry Pi HD camera and 5V servo motor for imaging and LOST software for image proccessing
#Servo motion controls using native Raspberry Pi GPIO pins or Adafruit servo/PWM hat. Camera controls using Picamera
#Created by Mallory Shaloy 4/2024
#CCofCO RockSat-X 2024
#---------------------

from picamera2 import Picamera2
from time import sleep
from gpiozero import AngularServo, Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import subprocess

class StarTracker():
    """Class for controlling Star Tracker using a Raspberry Pi HD camera and servo motor, optionally controlled by Adafruit servo/PWM hat. 
        Also controls computational software for star tracking."""
    def __init__(self, pin_number, board=None, channel=-1):
        """Create and initialize a Star Tracker object.
            param: pin_number: The value of the pin to which the servo to be controlled is attached.
            param: PWM board: The instance of an Adafruit servo/PWM hat being utilized if any.
                            Value of None indicates direct connection to GPIO pins.
            param: int channel: The value of the channel to which the servo to be controlled is connected.
                            0 to 15 are valid values. 
                            Default value of -1 indications direct connection to GPIO pins.
        """
        self._board = board
        self._channel = channel
        self._camera = Picamera2()
        self._my_factory = PiGPIOFactory()
        self._tracker_servo = AngularServo(pin_number, min_pulse_width=.0005, max_pulse_width=.0025, pin_factory=self._my_factory)

    def moveCamera(self, angle=0):
        """Moves servo and attached camera to specified angle in degrees. For use with direct GPIO connection only."""
        self._tracker_servo.angle = angle

    def boardMoveCamera(self, angle=0):
        """Moves servo and attached camera to specified angle in degrees. For use with PWM board only."""
        if self._board == None:
            raise Exception("This function requires the use of a compatible PWM board")
        elif self._channel < 0 or self.channel > 15:
            raise Exception("Invalid channel number. Value must be 0 to 15")
        else:
            self._board.servo[self._channel].angle = [angle]

    def takePicture(self, image_number):
        """Begins camera object, captures a single image, and saves it as a png file with the naming schema 'image[image_number].png'."""
        self._camera.start_and_capture_files(f"/home/static/static_project/lost/image{image_number}.png", initial_delay=0, delay=0, num_files=1)

    def trackerCalculation(self, num_images):       # TODO
        """Runs the LOST star tracker software calculations on the specified number of images with the naming schema 'image[image_number].png'"""
        for i in range(num_images):
            subprocess.run(['/home/static/static_project/trackerSoftware.sh', f'{i}'])

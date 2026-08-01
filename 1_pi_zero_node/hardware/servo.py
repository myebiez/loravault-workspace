import RPi.GPIO as GPIO
import time
from config import Pinout

class VaultLatch:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Pinout.SERVO_DATA, GPIO.OUT)
        self.pwm = GPIO.PWM(Pinout.SERVO_DATA, 50) # 50Hz for SG90/MG90S
        self.pwm.start(0)
        self.lock()

    def _set_angle(self, angle):
        # CLRS: Constant time physical actuation -> \mathcal{O}(1)
        duty = (angle / 18) + 2
        GPIO.output(Pinout.SERVO_DATA, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        GPIO.output(Pinout.SERVO_DATA, False)
        self.pwm.ChangeDutyCycle(0)

    def unlock(self):
        self._set_angle(90) # Open position

    def lock(self):
        self._set_angle(0)  # Closed position
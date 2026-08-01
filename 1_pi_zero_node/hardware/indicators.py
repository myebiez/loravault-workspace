import RPi.GPIO as GPIO
import time
from config import Pinout

# DOET: Feedback & Mapping. Immediate physical responses to system state.
class Indicator:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pins = [Pinout.LED_GREEN, Pinout.LED_RED, Pinout.BUZZER]
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def success(self):
        # DOET: Clear, positive feedback (Green + short beep)
        GPIO.output(Pinout.LED_GREEN, GPIO.HIGH)
        GPIO.output(Pinout.BUZZER, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(Pinout.BUZZER, GPIO.LOW)
        time.sleep(1.8)
        GPIO.output(Pinout.LED_GREEN, GPIO.LOW)

    def error(self):
        # DOET: Error Signifier (Red + long/harsh beep)
        GPIO.output(Pinout.LED_RED, GPIO.HIGH)
        GPIO.output(Pinout.BUZZER, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(Pinout.BUZZER, GPIO.LOW)
        GPIO.output(Pinout.LED_RED, GPIO.LOW)
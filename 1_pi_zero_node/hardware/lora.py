import serial
import RPi.GPIO as GPIO
import time
from config import Pinout, Settings

class LoRaTransceiver:
    def __init__(self):
        self.serial = serial.Serial(Settings.LORA_PORT, Settings.LORA_BAUDRATE, timeout=1)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Pinout.LORA_M0, GPIO.OUT)
        GPIO.setup(Pinout.LORA_M1, GPIO.OUT)
        self.set_mode_transmit()

    def _set_pins(self, m0, m1):
        GPIO.output(Pinout.LORA_M0, m0)
        GPIO.output(Pinout.LORA_M1, m1)
        # Pragmatic: Hardware timing constraint. M0/M1 switches require delay.
        time.sleep(0.15) 

    def set_mode_transmit(self):
        # Mode 0,0: Normal Transmission
        self._set_pins(GPIO.LOW, GPIO.LOW)

    def set_mode_config(self):
        # Mode 1,0: Configuration (Waveshare specific)
        self._set_pins(GPIO.HIGH, GPIO.LOW)

    def send_packet(self, rfid_uid, weight_delta):
        # SICP: Pure string formatting abstraction for our private protocol
        # Format: <UID>|<DELTA>
        payload = f"{rfid_uid}|{weight_delta:.2f}\n"
        self.serial.flushOutput()
        self.serial.write(payload.encode('utf-8'))
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
        time.sleep(0.15) 

    def set_mode_transmit(self):
        self._set_pins(GPIO.LOW, GPIO.LOW)

    def set_mode_config(self):
        self._set_pins(GPIO.HIGH, GPIO.LOW)

    def send_telemetry(self, rfid_uid: str, weight_delta: float):
        # Format Multiplexing: Telemetri Fisik (Pengambilan/Pengembalian Aset)
        payload = f"TLM|{rfid_uid}|{weight_delta:.2f}\n"
        self.serial.flushOutput()
        self.serial.write(payload.encode('utf-8'))

    def send_registration(self, rfid_uid: str, nik: str):
        # Format Multiplexing: Registrasi Cloud (Air-Gapped Sync berbasis NIK)
        payload = f"REG|{rfid_uid}|{nik}\n"
        self.serial.flushOutput()
        self.serial.write(payload.encode('utf-8'))
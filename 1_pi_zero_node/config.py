import os
from dotenv import load_dotenv

load_dotenv()

# SICP: Data Abstraction - centralizing hardware mappings.
# Semua penomoran di sini menggunakan standar BCM (GPIO) yang selaras dengan Pin Fisik di README.
class Pinout:
    # LoRa SX1262 (M0/M1 Logic Pins)
    LORA_M0 = 22  # Selaras dengan Pin Fisik 15
    LORA_M1 = 27  # Selaras dengan Pin Fisik 13
    
    # HX711 Load Cell
    SCALE_DT = 5  # Selaras dengan Pin Fisik 29
    SCALE_SCK = 6 # Selaras dengan Pin Fisik 31
    
    # Servo
    SERVO_DATA = 12 # Selaras dengan Pin Fisik 32
    
    # Indicators (DOET Signifiers)
    LED_GREEN = 18 # Selaras dengan Pin Fisik 12
    LED_RED = 24   # Selaras dengan Pin Fisik 18
    BUZZER = 23    # Selaras dengan Pin Fisik 16
    
    # Catatan: Pin SPI (SDA, SCK, MOSI, MISO) dan UART (TX, RX) 
    # ditangani langsung oleh interface raspi-config OS.

class Settings:
    LORA_PORT = os.getenv("LORA_PORT", "/dev/serial0")
    LORA_BAUDRATE = int(os.getenv("LORA_BAUDRATE", 9600))
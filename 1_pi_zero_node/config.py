import os
from dotenv import load_dotenv

load_dotenv()

# SICP: Data Abstraction - centralizing hardware mappings.
# Physical pin numbers mapped to BCM (GPIO) for RPi.GPIO
class Pinout:
    # LoRa SX1262
    LORA_TX = 15
    LORA_RX = 14
    LORA_M0 = 22
    LORA_M1 = 27
    
    # HX711 Load Cell
    SCALE_DT = 5
    SCALE_SCK = 6
    
    # Servo
    SERVO_DATA = 12
    
    # Indicators (DOET Signifiers)
    LED_GREEN = 18
    LED_RED = 24
    BUZZER = 23
    
    # RFID (SPI pins handled natively by spidev, only RST defined here)
    RFID_RST = 25

class Settings:
    LORA_PORT = os.getenv("LORA_PORT", "/dev/serial0")
    LORA_BAUDRATE = int(os.getenv("LORA_BAUDRATE", 9600))
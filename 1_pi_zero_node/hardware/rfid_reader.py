from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

# SICP: Data and Procedural Abstraction.
# We hide the complexity of the SPI interface (MOSI/MISO/SCK/SDA) behind this class.
# The main loop now only cares about "waiting for a tap" and "getting a UID".
class RFIDScanner:
    def __init__(self):
        # SimpleMFRC522 natively handles the SPI setup on physical pins 19, 21, 23, 24, 22.
        # We wrap it here to enforce a strict boundary between hardware and business logic.
        self.reader = SimpleMFRC522()

    def wait_for_tap(self):
        """
        Blocks execution until an RFID tag is detected.
        Returns the sanitized UID as a string.
        """
        try:
            # CLRS: I/O bound blocking operation. 
            uid, text = self.reader.read()
            
            # Pragmatic Programmer: Design by Contract. 
            # We guarantee the upper layers receive a clean, uniform string, not raw hardware bytes.
            return str(uid).strip()
        except Exception as e:
            # Fail gracefully, pass error up the chain if SPI crashes
            print(f"[Hardware Error] RFID read failed: {e}")
            return None
        finally:
            # Note: We do NOT call GPIO.cleanup() here because other 
            # hardware components (servo, LEDs) are still actively using GPIO.
            pass
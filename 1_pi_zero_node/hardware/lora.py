import serial
import RPi.GPIO as GPIO
import time
from config import Pinout, Settings

class LoRaTransceiver:
    def __init__(self):
        # Pragmatic Programmer: Bounded blocking. 
        # Kita tambahkan timeout=3 agar sistem tidak hang selamanya jika ESP32 mati/ACK hilang.
        self.serial = serial.Serial(Settings.LORA_PORT, Settings.LORA_BAUDRATE, timeout=3)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Pinout.LORA_M0, GPIO.OUT)
        GPIO.setup(Pinout.LORA_M1, GPIO.OUT)
        self.set_mode_transmit()

    def _set_pins(self, m0, m1):
        GPIO.output(Pinout.LORA_M0, m0)
        GPIO.output(Pinout.LORA_M1, m1)
        # Delay perangkat keras untuk memastikan modul SX1262 selesai berpindah state
        time.sleep(0.15) 

    def set_mode_transmit(self):
        # Mode Normal Transmisi & Receive (M0=0, M1=0)
        self._set_pins(GPIO.LOW, GPIO.LOW)

    def set_mode_config(self):
        self._set_pins(GPIO.HIGH, GPIO.LOW)

    def send_telemetry(self, rfid_uid: str, weight_delta: float):
        # Format Multiplexing: Telemetri Fisik (Pengambilan/Pengembalian Aset)
        # Tetap fire-and-forget karena paket telemetri redundan secara alamiah
        payload = f"TLM|{rfid_uid}|{weight_delta:.2f}\n"
        self.serial.flushOutput()
        self.serial.write(payload.encode('utf-8'))

    def send_registration_with_ack(self, rfid_uid: str, nik: str) -> bool:
        # SICP: Sinkronisasi Transaksional.
        # Menembakkan payload ke ESP32
        payload = f"REG|{rfid_uid}|{nik}\n"
        
        # Bersihkan buffer masuk sebelum mengirim untuk membuang noise/pantulan sisa
        self.serial.flushInput() 
        self.serial.write(payload.encode('utf-8'))
        
        # Memblokir thread untuk menunggu ACK balik dari ESP32 (Maksimal 3 detik dari init)
        try:
            response = self.serial.readline().decode('utf-8').strip()
            if response == f"ACK|{rfid_uid}":
                return True # Gateway mengkonfirmasi Supabase mengembalikan HTTP 200/201
        except Exception as e:
            print(f"[LoRa] Kegagalan IO saat menunggu ACK: {e}")
            pass
            
        return False # Timeout atau balasan korup, sync dianggap gagal
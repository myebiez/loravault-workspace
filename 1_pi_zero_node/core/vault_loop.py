import time
import RPi.GPIO as GPIO
from hardware.rfid_reader import RFIDScanner
from hardware.indicators import Indicator
from hardware.servo import VaultLatch
from hardware.scale import WeightSensor
from hardware.lora import LoRaTransceiver
from core.local_db import LocalAuthDB

class VaultSystem:
    def __init__(self):
        self.rfid = RFIDScanner()
        self.indicator = Indicator()
        self.latch = VaultLatch()
        self.scale = WeightSensor()
        self.lora = LoRaTransceiver()
        self.auth_db = LocalAuthDB()

    def _write_last_tap_for_web(self, uid: str):
        """IPC Sederhana: Menyimpan UID terakhir di SQLite agar UI Web Flask dapat melakukan Auto-Fill."""
        try:
            self.auth_db.set_last_rfid(uid)
        except Exception as e:
            print(f"[IPC Error] Gagal mencatat last tap ke database: {e}")

    def _check_tare_flag(self):
        """IPC Sederhana: Membaca flag atomik dari SQLite untuk melakukan kalibrasi hardware."""
        try:
            # check_and_clear_tare_flag() melakukan DELETE atomik dan mengembalikan True jika berhasil
            if self.auth_db.check_and_clear_tare_flag():
                print("[Hardware] Perintah Tare (Kalibrasi) dari Web UI dieksekusi...")
                self.scale.hx.tare()
                self.indicator.success()
        except Exception as e:
            print(f"[IPC Error] Gagal mengecek tare flag: {e}")

    def _sync_offline_registrations(self):
        """Memancarkan data user baru ke gateway saat sedang idle dan menunggu ACK."""
        unsynced = self.auth_db.get_unsynced_users()
        for uid, nik in unsynced:
            print(f"Air-Gapped Sync: Mencoba mendaftarkan NIK {nik}...")
            # Hanya tandai sukses jika ESP32 mengirim balasan ACK secara eksplisit
            if self.lora.send_registration_with_ack(uid, nik):
                print(f"ACK Diterima! {nik} tersinkronisasi secara persisten.")
                self.auth_db.mark_synced(uid)
            else:
                print(f"Gagal Sync {nik}. Menunggu siklus berikutnya.")
            time.sleep(1) # Jeda antar pancaran agar buffer LoRa aman

    def run(self):
        print("LoRaVault Core Active. Awaiting RFID...")
        try:
            while True:
                # 1. Cek perintah kalibrasi dari UI (Atomic DB Check)
                self._check_tare_flag()
                
                # 2. Background Sync Protocol dengan Guaranteed Delivery (ACK)
                self._sync_offline_registrations()
                
                # 3. Wait for tap
                uid = self.rfid.wait_for_tap()
                if not uid:
                    time.sleep(0.5)
                    continue
                    
                print(f"RFID Terdeteksi: {uid}")
                self._write_last_tap_for_web(uid) # Trigger auto-fill UI
                
                # 4. ZERO-TRUST SECURITY: Validasi Lokal Terketat
                if not self.auth_db.is_valid_uid(uid):
                    print("Akses Ditolak: Kartu Tidak Dikenal.")
                    self.indicator.error() # Tembakkan alarm penolakan fisik
                    time.sleep(1.5)
                    continue
                
                # 5. Akses Sah -> Operasional Standar
                self.indicator.success()
                self.latch.unlock()
                
                weight_before = self.scale.get_stable_weight()
                time.sleep(5.0) # Waktu bagi pengguna untuk mengambil aset
                
                self.latch.lock()
                weight_after = self.scale.get_stable_weight()
                
                delta = weight_after - weight_before
                print(f"Weight Delta: {delta}g")
                
                # 6. Kirim Telemetri ke Gateway (Fire-and-forget, data fisik bersifat redundant)
                self.lora.send_telemetry(uid, delta)
                time.sleep(2)
                        
        except KeyboardInterrupt:
            print("System halted by user.")
        finally:
            # Pragmatic Programmer: Safe shutdown to prevent hardware damage or open locks
            self.latch.lock()
            GPIO.cleanup()
            print("GPIO Cleaned up. Vault Locked.")
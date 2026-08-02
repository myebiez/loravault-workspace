import time
import os
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
        """IPC Sederhana: Menyimpan UID terakhir agar UI Web Flask dapat melakukan Auto-Fill."""
        try:
            with open("/tmp/last_rfid.txt", "w") as f:
                f.write(str(uid))
        except Exception:
            pass

    def _sync_offline_registrations(self):
        """Memancarkan data user baru ke gateway saat sedang idle."""
        unsynced = self.auth_db.get_unsynced_users()
        for uid, nik in unsynced:
            print(f"Air-Gapped Sync: Mendaftarkan NIK {nik}...")
            self.lora.send_registration(uid, nik)
            self.auth_db.mark_synced(uid)
            time.sleep(1) # Jeda antar pancaran agar buffer LoRa aman

    def run(self):
        print("LoRaVault Core Active. Awaiting RFID...")
        try:
            while True:
                # 1. Background Sync Protocol
                self._sync_offline_registrations()
                
                # 2. Wait for tap
                uid = self.rfid.wait_for_tap()
                if not uid:
                    time.sleep(0.5)
                    continue
                    
                print(f"RFID Terdeteksi: {uid}")
                self._write_last_tap_for_web(uid) # Trigger auto-fill UI
                
                # 3. ZERO-TRUST SECURITY: Validasi Lokal Terketat
                if not self.auth_db.is_valid_uid(uid):
                    print("Akses Ditolak: Kartu Tidak Dikenal.")
                    self.indicator.error() # Tembakkan alarm penolakan fisik
                    time.sleep(1.5)
                    continue
                
                # 4. Akses Sah -> Operasional Standar
                self.indicator.success()
                self.latch.unlock()
                
                weight_before = self.scale.get_stable_weight()
                time.sleep(5.0) # Waktu bagi pengguna untuk mengambil aset
                
                self.latch.lock()
                weight_after = self.scale.get_stable_weight()
                
                delta = weight_after - weight_before
                print(f"Weight Delta: {delta}g")
                
                # 5. Kirim Telemetri ke Gateway
                self.lora.send_telemetry(uid, delta)
                time.sleep(2)
                        
        except KeyboardInterrupt:
            self.latch.lock()
            print("System halted.")
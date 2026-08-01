import time
from hardware.rfid_reader import RFIDScanner
from hardware.indicators import Indicator
from hardware.servo import VaultLatch
from hardware.scale import WeightSensor
from hardware.lora import LoRaTransceiver

# SICP: The procedural controller mapping the physical state machine.
class VaultSystem:
    def __init__(self):
        self.rfid = RFIDScanner() # Encapsulated behind Abstraction Barrier
        self.indicator = Indicator()
        self.latch = VaultLatch()
        self.scale = WeightSensor()
        self.lora = LoRaTransceiver()

    def run(self):
        print("LoRaVault Core Active. Awaiting RFID...")
        try:
            while True:
                # Step 1: Wait for tap (DOET: System readiness is implicit)
                uid = self.rfid.wait_for_tap()
                if not uid:
                    continue
                    
                print(f"Auth tap: {uid}")
                
                # Step 2: Immediate DOET Feedback & Unlock
                self.indicator.success()
                self.latch.unlock()
                
                # Baseline weight
                weight_before = self.scale.get_stable_weight()
                
                # Step 3: Wait for physical interaction (User opens, takes/returns, closes)
                # Pragmatic: Giving the user 5 seconds to actuate the door. 
                time.sleep(5.0) 
                
                # Step 4: Lock and audit
                self.latch.lock()
                weight_after = self.scale.get_stable_weight()
                
                delta = weight_after - weight_before
                print(f"Weight Delta: {delta}g")
                
                # Step 5: Fire-and-forget transmission to ESP32 Gateway
                self.lora.send_packet(uid, delta)
                
                # Prevent double-reads
                time.sleep(2)
                        
        except KeyboardInterrupt:
            self.latch.lock()
            print("System halted.")
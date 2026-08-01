import subprocess
import os

class CameraService:
    def __init__(self, output_dir="captures"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def capture_image(self, transaction_id):
        # SICP: Procedural Abstraction mapping to the OS shell layer.
        # Uses standard libcamera-jpeg for modern Raspberry Pi OS compatibility (CSI port).
        # CLRS: \mathcal{O}(1) system call bounded by physical shutter speed constraints (1000ms).
        filepath = f"{self.output_dir}/audit_{transaction_id}.jpg"
        try:
            subprocess.run([
                "libcamera-jpeg", 
                "-o", filepath, 
                "-t", "1000",          # 1 second warmup
                "--width", "1280", 
                "--height", "720",
                "--nopreview"
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return filepath
        except subprocess.CalledProcessError:
            print("[Hardware Error] Camera capture failed. Is Arducam connected?")
            return None
import tkinter as tk
from queue import Empty
from PIL import Image, ImageTk
from src.config import Config
from src.camera_service import CameraService
from src.telegram_service import TelegramNotifier

class AuditDashboard:
    def __init__(self, root, event_queue):
        self.root = root
        self.event_queue = event_queue
        self.camera = CameraService()
        self.telegram = TelegramNotifier()
        
        self.root.title("LoRaVault Audit Desktop")
        self.root.geometry("800x480")
        self.root.configure(bg=Config.COLOR_BG)
        self.root.attributes("-fullscreen", True) # Intended for Pi 3 Touch Display
        
        self._build_ui()
        self._process_queue()

    def _build_ui(self):
        # Krug's Law: Design for Scanning, Not Reading. Omit needless words.
        # Massive headers. Obvious visual hierarchy.
        
        self.lbl_status = tk.Label(self.root, text="SYSTEM ARMED", 
                                   font=("Helvetica", 36, "bold"), 
                                   bg=Config.COLOR_BG, fg=Config.COLOR_SUCCESS)
        self.lbl_status.pack(pady=20)
        
        self.lbl_details = tk.Label(self.root, text="Awaiting next transaction...", 
                                    font=("Helvetica", 18), 
                                    bg=Config.COLOR_BG, fg=Config.COLOR_TEXT)
        self.lbl_details.pack(pady=10)

        # Image canvas placeholder
        self.lbl_image = tk.Label(self.root, bg=Config.COLOR_BG)
        self.lbl_image.pack(expand=True)

        # Escape route for development
        btn_exit = tk.Button(self.root, text="EXIT UI", font=("Helvetica", 12),
                             command=self.root.quit, bg="#3f3f46", fg="white", borderwidth=0)
        btn_exit.pack(side=tk.BOTTOM, fill=tk.X)

    def _process_queue(self):
        # CLRS: \mathcal{O}(1) polling of the event queue on the main GUI thread.
        try:
            event = self.event_queue.get_nowait()
            self._handle_event(event)
        except Empty:
            pass
        finally:
            # Recursive Tkinter loop scheduling (approx 100ms)
            self.root.after(100, self._process_queue)

    def _handle_event(self, transaction):
        uid = transaction.get("rfid_uid")
        delta = transaction.get("weight_delta")
        t_id = transaction.get("id")

        # Basic anomaly check based on weight delta (e.g., if highly irregular)
        # For DOET feedback, we visually highlight the UI.
        is_anomaly = abs(delta) > 500 # Example threshold logic

        # 1. Update UI (DOET: Feedback)
        bg_color = Config.COLOR_ALERT if is_anomaly else Config.COLOR_SUCCESS
        status_text = "⚠️ ANOMALY DETECTED" if is_anomaly else "✅ ASSET SECURED"
        
        self.lbl_status.config(text=status_text, fg=bg_color)
        self.lbl_details.config(text=f"UID: {uid} | Delta: {delta}g")

        # 2. Trigger Hardware (Camera)
        img_path = self.camera.capture_image(t_id)
        
        # 3. Update UI Image & Send Telegram
        if img_path:
            self._display_image(img_path)
            msg = f"{status_text}\nUID: {uid}\nWeight Delta: {delta}g"
            self.telegram.send_audit(msg, img_path)

    def _display_image(self, path):
        # Image resizing abstraction for Tkinter
        img = Image.open(path)
        img = img.resize((400, 225), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        self.lbl_image.config(image=tk_img)
        self.lbl_image.image = tk_img # Keep garbage collector away
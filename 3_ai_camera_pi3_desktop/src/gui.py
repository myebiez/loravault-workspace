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
        
        self.root.title("LoRaVault Executive Audit")
        self.root.geometry("800x480")
        self.root.configure(bg=Config.COLOR_BG)
        self.root.attributes("-fullscreen", True) # Intended for Pi 3 Touch Display
        
        self._build_ui()
        self._process_queue()

    def _build_ui(self):
        # UI/UX Goal: Create a zero-cognitive-load dashboard. 
        # Norman's DOET: Immediate Feedback and Clear Conceptual Model.
        # Krug's Law: Design for Scanning. Massive semantic headers.
        
        # Header Status
        self.lbl_status = tk.Label(self.root, text="VAULT SECURED", 
                                   font=("Helvetica", 38, "bold"), 
                                   bg=Config.COLOR_BG, fg=Config.COLOR_SUCCESS)
        self.lbl_status.pack(pady=(30, 5))
        
        # Identity Details (Who did what)
        self.lbl_identity = tk.Label(self.root, text="Monitoring Active...", 
                                    font=("Helvetica", 22, "bold"), 
                                    bg=Config.COLOR_BG, fg=Config.COLOR_TEXT_MAIN)
        self.lbl_identity.pack(pady=(0, 2))

        # Technical Details (Subtext for auditing)
        self.lbl_technical = tk.Label(self.root, text="System standing by for telemetry events.", 
                                    font=("Helvetica", 14), 
                                    bg=Config.COLOR_BG, fg=Config.COLOR_TEXT_MUTED)
        self.lbl_technical.pack(pady=(0, 15))

        # Image canvas placeholder (Visual Evidence)
        self.lbl_image = tk.Label(self.root, bg=Config.COLOR_BG)
        self.lbl_image.pack(expand=True)

        # Escape route for development (DOET: Exit constraint)
        btn_exit = tk.Button(self.root, text="EXIT SECURE VIEW", font=("Helvetica", 10, "bold"),
                             command=self.root.quit, bg="#1e293b", fg=Config.COLOR_TEXT_MUTED, 
                             activebackground="#334155", activeforeground="white", borderwidth=0, pady=10)
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

        # SSOT: Extract Full Name and Department safely (Handling Nulls / Unregistered)
        users_data = transaction.get("users") or {}
        hr_data = users_data.get("hr_employees") or {}
        full_name = hr_data.get("full_name", "UNKNOWN (UNREGISTERED CARD)")
        dept = hr_data.get("department", "No Dept")

        # Logic Filter: Is it taken, returned, or noise?
        is_taken = delta < -15
        is_returned = delta > 15
        
        # Norman's DOET: Clear Signifiers mapped to physical state.
        if is_taken:
            bg_color = Config.COLOR_ALERT
            status_text = "ASSET TAKEN"
            delta_str = f"{delta}g"
        elif is_returned:
            bg_color = Config.COLOR_SUCCESS
            status_text = "ASSET RETURNED"
            delta_str = f"+{delta}g"
        else:
            bg_color = Config.COLOR_TEXT_MUTED
            status_text = "DOOR ACCESSED (NO CHANGE)"
            delta_str = f"{delta}g"

        # 1. Update UI (Krug's Law: Don't make me think. Tell me WHO and WHAT instantly)
        self.lbl_status.config(text=status_text, fg=bg_color)
        self.lbl_identity.config(text=f"{full_name}")
        self.lbl_technical.config(text=f"UID: {uid}  |  Dept: {dept}  |  Weight: {delta_str}")

        # 2. Trigger Hardware (Camera Snapshot - O(1) specific event targeting)
        img_path = self.camera.capture_image(t_id)
        
        # 3. Update UI Image & Send Executive Telegram Notification
        if img_path:
            self._display_image(img_path)
            
            # Format the Telegram alert to be highly readable for executives
            telegram_msg = (
                f"🚨 *LORA VAULT ALERT*\n\n"
                f"*{status_text}*\n"
                f"👤 *Name:* {full_name}\n"
                f"🏢 *Dept:* {dept}\n"
                f"⚖️ *Delta:* {delta_str}\n"
                f"🪪 *UID:* `{uid}`"
            )
            self.telegram.send_audit(telegram_msg, img_path)

    def _display_image(self, path):
        # Image resizing abstraction for Tkinter GUI
        img = Image.open(path)
        img = img.resize((400, 225), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        self.lbl_image.config(image=tk_img)
        self.lbl_image.image = tk_img # Keep garbage collector away
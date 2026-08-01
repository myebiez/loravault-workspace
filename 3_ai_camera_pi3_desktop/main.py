import tkinter as tk
import queue
from src.cloud_listener import CloudListener
from src.gui import AuditDashboard

# SICP: The system entrypoint merely instantiates independent modules 
# and provides the data channel (Queue) to link them without tight coupling.
if __name__ == "__main__":
    # Create thread-safe queue for inter-thread communication
    event_queue = queue.Queue()

    # Initialize and start Cloud Listener (Background Thread)
    listener = CloudListener(event_queue)
    listener.start()

    # Initialize and start Tkinter GUI (Main Thread)
    root = tk.Tk()
    app = AuditDashboard(root, event_queue)
    
    # Block and run UI
    root.mainloop()
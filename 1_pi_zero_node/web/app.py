from flask import Flask, render_template, request, jsonify
import os
import sys

# Memastikan Flask dapat membaca modul dari folder utama (core)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.local_db import LocalAuthDB

app = Flask(__name__)
auth_db = LocalAuthDB()

# Krug's Law: Routing yang absolut dan jelas.
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/last_tap', methods=['GET'])
def last_tap():
    """Mengambil UID terakhir dari sensor fisik secara aman."""
    try:
        if os.path.exists("/tmp/last_rfid.txt"):
            with open("/tmp/last_rfid.txt", "r") as f:
                uid = f.read().strip()
                return jsonify({"uid": uid})
    except Exception:
        pass
    return jsonify({"uid": ""})

@app.route('/api/register', methods=['POST'])
def register():
    """Mendaftarkan NIK ke DB lokal dan menandainya untuk Sinkronisasi LoRa."""
    data = request.json
    uid = data.get("uid")
    nik = data.get("nik")
    
    if not uid or not nik:
        return jsonify({"status": "error", "message": "UID dan NIM/NIK wajib diisi!"}), 400
        
    try:
        auth_db.register_user(uid, nik)
        # Menghapus cache temporary agar tidak tersubmit dua kali
        if os.path.exists("/tmp/last_rfid.txt"):
            os.remove("/tmp/last_rfid.txt")
        return jsonify({"status": "success", "message": f"Karyawan ID {nik} masuk antrean Sync!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/tare', methods=['POST'])
def tare_scale():
    """
    IPC (Inter-Process Communication) Sederhana.
    Menulis flag file untuk dibaca oleh vault_loop.py tanpa memblokir thread web.
    """
    try:
        with open("/tmp/tare_flag", "w") as f:
            f.write("1")
        return jsonify({"status": "success", "message": "Perintah kalibrasi dikirim ke hardware."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Gagal mengirim perintah: {e}"}), 500

if __name__ == '__main__':
    # Security by Default: Menurunkan privilege dengan tidak menggunakan port 80 (Root).
    port = int(os.getenv("FLASK_PORT", 8080))
    app.run(host='0.0.0.0', port=port)
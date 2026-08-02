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
    """Mengambil UID terakhir dari database SQLite IPC secara atomik."""
    try:
        uid = auth_db.get_last_rfid()
        return jsonify({"uid": uid})
    except Exception as e:
        print(f"[Web API Error] Gagal membaca last tap: {e}")
        return jsonify({"uid": ""})

@app.route('/api/register', methods=['POST'])
def register():
    """Mendaftarkan NIK ke DB lokal, menandainya untuk Sync LoRa, dan membersihkan cache UI."""
    data = request.json
    uid = data.get("uid")
    nik = data.get("nik")
    
    if not uid or not nik:
        return jsonify({"status": "error", "message": "UID dan NIM/NIK wajib diisi!"}), 400
        
    try:
        auth_db.register_user(uid, nik)
        # Membersihkan cache UID terakhir di SQLite agar UI tidak terisi otomatis dengan UID yang sama
        auth_db.clear_last_rfid()
        return jsonify({"status": "success", "message": f"Karyawan ID {nik} masuk antrean Sync!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/tare', methods=['POST'])
def tare_scale():
    """
    IPC (Inter-Process Communication) Atomik via SQLite.
    Menulis tare_flag ke tabel ipc_state tanpa memblokir thread HTTP response.
    """
    try:
        auth_db.set_tare_flag()
        return jsonify({"status": "success", "message": "Perintah kalibrasi dikirim ke hardware."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Gagal mengirim perintah: {e}"}), 500

if __name__ == '__main__':
    # Security by Default: Menurunkan privilege dengan tidak menggunakan port 80 (Root).
    port = int(os.getenv("FLASK_PORT", 8080))
    app.run(host='0.0.0.0', port=port)
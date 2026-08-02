import sqlite3
import os

# SICP: Enkapsulasi penyimpanan state secara lokal. 
# Database disimpan di root folder 1_pi_zero_node/
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'access_control.db')

class LocalAuthDB:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(DB_PATH) as conn:
            # The Pragmatic Programmer: Mengatasi "database is locked" saat Flask dan Core Loop mengakses bersamaan
            conn.execute('PRAGMA journal_mode=WAL;')
            
            # 1. Tabel Utama: Autentikasi Zero-Trust
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    uid TEXT PRIMARY KEY,
                    nik TEXT NOT NULL,
                    sync_status INTEGER DEFAULT 0
                )
            """)
            
            # 2. Tabel IPC (Inter-Process Communication): Pengganti /tmp yang tahan banting
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ipc_state (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)

    # =========================================================================
    # FUNGSI AUTENTIKASI (Zero-Trust & Air-Gapped Sync)
    # =========================================================================
    
    def is_valid_uid(self, uid: str) -> bool:
        """CLRS: Pencarian O(log N) menggunakan Primary Key index bawaan SQLite."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("SELECT 1 FROM users WHERE uid = ?", (uid,))
            return cursor.fetchone() is not None

    def register_user(self, uid: str, nik: str):
        """Simpan secara lokal dan tandai sebagai belum tersinkronisasi (0)."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO users (uid, nik, sync_status) VALUES (?, ?, 0)",
                (uid, nik)
            )

    def get_unsynced_users(self):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("SELECT uid, nik FROM users WHERE sync_status = 0")
            return cursor.fetchall()

    def mark_synced(self, uid: str):
        """Ubah status menjadi 1 setelah LoRa/Gateway berhasil mengembalikan ACK."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("UPDATE users SET sync_status = 1 WHERE uid = ?", (uid,))

    # =========================================================================
    # FUNGSI IPC (Inter-Process Communication untuk Flask Web <-> Core Loop)
    # =========================================================================
    
    def set_last_rfid(self, uid: str):
        """Menyimpan UID terakhir agar UI Web Flask dapat melakukan Auto-Fill."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT OR REPLACE INTO ipc_state (key, value) VALUES ('last_rfid', ?)", (uid,))

    def get_last_rfid(self) -> str:
        """Mengambil UID terakhir dari database untuk Web UI."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("SELECT value FROM ipc_state WHERE key = 'last_rfid'")
            row = cursor.fetchone()
            return row[0] if row else ""

    def clear_last_rfid(self):
        """Membersihkan cache UI setelah pendaftaran berhasil."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("DELETE FROM ipc_state WHERE key = 'last_rfid'")

    def set_tare_flag(self):
        """Web UI menitipkan pesan kalibrasi ke dalam database (Tidak memblokir web request)."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT OR REPLACE INTO ipc_state (key, value) VALUES ('tare_flag', '1')")

    def check_and_clear_tare_flag(self) -> bool:
        """
        Core Loop mengecek pesan kalibrasi. 
        Eksekusi atomik mutlak: Langsung DELETE dan cek rowcount, menghindari Race Condition.
        """
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("DELETE FROM ipc_state WHERE key = 'tare_flag'")
            return cursor.rowcount > 0
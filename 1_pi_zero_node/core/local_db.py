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
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    uid TEXT PRIMARY KEY,
                    nik TEXT NOT NULL,
                    sync_status INTEGER DEFAULT 0
                )
            """)

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
        """Ubah status menjadi 1 setelah LoRa berhasil mengirimkannya ke Cloud."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("UPDATE users SET sync_status = 1 WHERE uid = ?", (uid,))
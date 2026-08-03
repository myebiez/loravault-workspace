import os
from supabase import create_client, Client
from src.config import Config

class StorageService:
    def __init__(self):
        self.supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        self.bucket_name = "audit_snapshots"

    def upload_evidence(self, transaction_id: str, file_path: str) -> str:
        """
        Mengunggah foto ke Supabase Storage, mengambil Public URL, 
        dan memperbarui baris transaksi di SQL secara atomik menggunakan Secure RPC.
        """
        if not os.path.exists(file_path):
            print(f"[Storage Error] File {file_path} tidak ditemukan.")
            return None

        file_name = f"audit_{transaction_id}.jpg"

        try:
            # 1. Unggah File ke Bucket (O(1) Network I/O)
            with open(file_path, "rb") as f:
                file_bytes = f.read()
                
            self.supabase.storage.from_(self.bucket_name).upload(
                path=file_name,
                file=file_bytes,
                file_options={"content-type": "image/jpeg", "x-upsert": "true"}
            )

            # ZERO-TRUST: Kita TIDAK mengambil public_url. 
            # Kita hanya melempar file_name ke DB agar Dashboard membuat Signed URL.
            self.supabase.rpc("secure_attach_evidence", {
                "p_transaction_id": transaction_id,
                "p_url": file_name, 
                "p_token": Config.GATEWAY_TOKEN # Membaca dari environment
            }).execute()

            print(f"[Storage Success] Bukti forensik diamankan: {file_name}")
            return file_name # Mengembalikan path untuk Telegram (opsional)

        except Exception as e:
            print(f"[Storage Error] Gagal mengamankan bukti visual: {e}")
            return None
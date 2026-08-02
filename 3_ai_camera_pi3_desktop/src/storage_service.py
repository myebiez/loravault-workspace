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

            # 2. Dapatkan Tautan Resolusi Publik
            public_url = self.supabase.storage.from_(self.bucket_name).get_public_url(file_name)

            # 3. Update Database (Zero-Trust RPC)
            # Mengeliminasi blokade RLS yang membatasi hak akses 'anon'
            self.supabase.rpc("secure_attach_evidence", {
                "p_transaction_id": transaction_id,
                "p_url": public_url,
                "p_token": "secret_esp32_hmac_token" # Sesuai dengan Token Arsitektur kita
            }).execute()

            print(f"[Storage Success] Bukti forensik diamankan: {public_url}")
            return public_url

        except Exception as e:
            print(f"[Storage Error] Gagal mengamankan bukti visual: {e}")
            return None
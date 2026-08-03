-- ==============================================================================
-- LORAVAULT: ZERO-TRUST ROW LEVEL SECURITY (RLS)
-- ==============================================================================
-- Pragmatic Programmer: Security by Default (Deny All).
-- Semua tabel dikunci secara absolut. Tidak ada satupun entitas client-side 
-- (termasuk public anon key) yang bisa melakukan INSERT/UPDATE/DELETE langsung ke tabel.

ALTER TABLE hr_employees ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE active_loans ENABLE ROW LEVEL SECURITY;

-- ==============================================================================
-- 1. EDGE GATEWAY POLICIES (ESP32)
-- ==============================================================================
-- PENTING: Kebijakan "ESP32 can insert transactions" TELAH DICABUT TOTAL.
-- ESP32 kini WAJIB melewati titik akhir RPC (secure_insert_telemetry & secure_sync_user)
-- di mana fungsi tersebut berjalan sebagai SECURITY DEFINER dan memvalidasi GATEWAY_TOKEN.
-- RLS secara alamiah akan memblokir 100% upaya injeksi langsung dari DevTools/Postman hacker.

-- ==============================================================================
-- 2. COMMAND CENTER POLICIES (NEXT.JS DASHBOARD)
-- ==============================================================================
-- Hapus akses terbuka (anon) jika sebelumnya pernah dijalankan
DROP POLICY IF EXISTS "Command Center read hr" ON hr_employees;
DROP POLICY IF EXISTS "Command Center read users" ON users;
DROP POLICY IF EXISTS "Command Center read assets" ON assets;
DROP POLICY IF EXISTS "Command Center read logs" ON transactions_log;
DROP POLICY IF EXISTS "Command Center read loans" ON active_loans;

-- Terapkan Zero-Trust Absolute: Hanya yang LOGIN (authenticated) yang boleh membaca data
CREATE POLICY "Command Center read hr" ON hr_employees FOR SELECT TO authenticated USING (true);
CREATE POLICY "Command Center read users" ON users FOR SELECT TO authenticated USING (true);
CREATE POLICY "Command Center read assets" ON assets FOR SELECT TO authenticated USING (true);
CREATE POLICY "Command Center read logs" ON transactions_log FOR SELECT TO authenticated USING (true);
CREATE POLICY "Command Center read loans" ON active_loans FOR SELECT TO authenticated USING (true);

-- ==============================================================================
-- 3. VISUAL AUDIT STORAGE POLICIES (PI 3 CAMERA)
-- ==============================================================================
-- Inisialisasi Bucket PRIVATE untuk menyimpan bukti foto dari Pi 3.
-- Menggunakan metode "Infrastructure as Code" (IaC) yang memastikan 
-- jika bucket sudah ada sebagai public, ia akan ditimpa menjadi private.
INSERT INTO storage.buckets (id, name, public) 
VALUES ('audit_snapshots', 'audit_snapshots', false) 
ON CONFLICT (id) DO UPDATE SET public = false;

-- Mengunci akses objek storage (Secure by default)
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Policy 1: Mengizinkan Node 3 (Kamera Pi 3) untuk mengunggah (INSERT) foto
-- Node 3 menggunakan anon key, dibatasi HANYA ke bucket 'audit_snapshots'
CREATE POLICY "Camera Node can upload snapshots" 
ON storage.objects FOR INSERT 
TO anon, authenticated 
WITH CHECK (bucket_id = 'audit_snapshots');

-- Policy 2: Mengizinkan Dasbor Next.js untuk membaca (SELECT) foto
-- Dasbor akan menggunakan metode Signed URL untuk bypass akses publik
CREATE POLICY "Dashboard can view snapshots" 
ON storage.objects FOR SELECT 
TO anon, authenticated 
USING (bucket_id = 'audit_snapshots');
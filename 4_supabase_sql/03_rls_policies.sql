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
-- Mengizinkan Dasbor Eksekutif (client-side) untuk MEMBACA (SELECT) data secara real-time.
-- Karena ini dasbor monitoring, akses READ diberikan untuk memastikan Websocket berjalan.
-- Operasi tulis (Admin Panel) di masa depan WAJIB menggunakan Service Role Key (Server-Side).

CREATE POLICY "Command Center read hr" ON hr_employees FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Command Center read users" ON users FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Command Center read assets" ON assets FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Command Center read logs" ON transactions_log FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Command Center read loans" ON active_loans FOR SELECT TO anon, authenticated USING (true);
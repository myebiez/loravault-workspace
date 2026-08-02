-- Pragmatic Programmer: Security by Default.
-- We do not trust the client. The ESP32 is only granted exact, minimal privileges.

ALTER TABLE hr_employees ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE active_loans ENABLE ROW LEVEL SECURITY;

-- 1. KEBIJAKAN ESP32 (Murni Edge Client)
-- Anon/ESP32 HANYA boleh mencatat log transaksi dan menyinkronkan kartu RFID.
CREATE POLICY "ESP32 can insert transactions" ON transactions_log FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "ESP32 can insert/sync users" ON users FOR INSERT TO anon WITH CHECK (true);

-- 2. KEBIJAKAN COMMAND CENTER (Manajer Dashboard)
-- Harus Authenticated (atau menggunakan Service_Role) untuk membaca data
CREATE POLICY "Command Center read hr" ON hr_employees FOR SELECT TO authenticated USING (true);
CREATE POLICY "Command Center read users" ON users FOR SELECT TO authenticated USING (true);
CREATE POLICY "Command Center read assets" ON assets FOR SELECT TO authenticated USING (true);
CREATE POLICY "Command Center read logs" ON transactions_log FOR SELECT TO authenticated USING (true);
CREATE POLICY "Command Center read loans" ON active_loans FOR SELECT TO authenticated USING (true);
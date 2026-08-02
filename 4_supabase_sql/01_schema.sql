-- ==============================================================================
-- LORAVAULT: ENTERPRISE DATABASE SCHEMA (SINGLE SOURCE OF TRUTH)
-- ==============================================================================
-- Pragmatic Programmer: Design by Contract. 
-- We enforce data integrity at the lowest level. No nulls, strict types, and clear relationships.

-- 1. TABEL HRD (Kebenaran Tunggal Data Pegawai)
-- Tabel ini idealnya disinkronisasi dari sistem HR perusahaan (misal: SAP/Oracle).
CREATE TABLE hr_employees (
    nik TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    department TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 2. TABEL PENGGUNA RFID (Jembatan antara Kartu Fisik dan Identitas HRD)
-- Diisi otomatis oleh ESP32 Gateway via LoRa Multiplexing (Paket REG)
CREATE TABLE users (
    rfid_uid TEXT PRIMARY KEY,
    nik TEXT NOT NULL REFERENCES hr_employees(nik) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 3. TABEL ASET (Katalog Inventaris Brankas)
CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    baseline_weight_g NUMERIC NOT NULL,
    tolerance_g NUMERIC NOT NULL DEFAULT 15, -- DOET: Error Recovery. Toleransi drift LoadCell
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 4. TABEL LOG TRANSAKSI (Immutable Ledger - Paket TLM dari ESP32)
CREATE TABLE transactions_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rfid_uid TEXT NOT NULL,
    weight_delta NUMERIC NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    -- Relasi FK: Gunakan RESTRICT agar data log audit/finansial tidak cacat jika user dihapus
    CONSTRAINT fk_user FOREIGN KEY (rfid_uid) REFERENCES users(rfid_uid) ON DELETE RESTRICT
);

-- 5. TABEL PEMINJAMAN AKTIF (State Aset Berjalan)
CREATE TABLE active_loans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rfid_uid TEXT NOT NULL REFERENCES users(rfid_uid) ON DELETE CASCADE,
    asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    borrowed_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    UNIQUE(asset_id) -- Sebuah aset fisik hanya bisa dipinjam oleh satu orang pada satu waktu
);

-- CLRS: Asymptotic Efficiency. 
-- B-Tree indexes ensure O(log N) time complexity for range scans and exact matches.
CREATE INDEX idx_users_rfid ON users USING btree(rfid_uid);
CREATE INDEX idx_transactions_created ON transactions_log USING btree(created_at DESC);
CREATE INDEX idx_assets_weight ON assets USING btree(baseline_weight_g);

-- ==============================================================================
-- SEED DATA (MOCK HR DATABASE)
-- Masukkan data dummy ini agar Dasbor Next.js bisa mem-parsing NIK.
-- ==============================================================================
INSERT INTO hr_employees (nik, full_name, department) VALUES 
('EMP-2026-001', 'Fadhil Muhammad Habibie', 'Systems Architecture'),
('EMP-2026-002', 'Yudha Prasetya', 'Maintenance & Engineering');

-- Mock Asset (Ganti baseline_weight_g dengan berat benda yang kamu uji coba di rumah)
INSERT INTO assets (name, baseline_weight_g, tolerance_g) VALUES 
('Mesin Bor Bosch', 1500, 20),
('Tang Ampere', 350, 10);

-- ==============================================================================
-- SUPABASE 2026 EXPLICIT GRANTS
-- ==============================================================================
-- Mencegah akses default yang ditiadakan di versi terbaru Supabase PostgreSQL.
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT SELECT ON hr_employees, users, assets, transactions_log, active_loans TO anon, authenticated;
-- (Hak INSERT dicabut dari 'anon' publik. Semua operasi penulisan kini WAJIB 
-- melewati fungsi RPC SECURITY DEFINER dengan injeksi token HMAC).
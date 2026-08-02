<div align="center">
  <img src="https://img.shields.io/badge/NODE-04_THE_BRAIN-059669?style=for-the-badge" alt="Node 4">
  <img src="https://img.shields.io/badge/DATABASE-POSTGRESQL-blue?style=for-the-badge" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/PLATFORM-SUPABASE-green?style=for-the-badge" alt="Supabase">
  
  <h1>🧠 Node 4: The Mathematical Brain (Supabase)</h1>
  <p><b>State Machine, B-Tree Indexes, & Single Source of Truth DB</b></p>
</div>

---

## 💼 The Executive Summary (Business Value)

Jika Node *Hardware* (Pi Zero & ESP32) adalah otot dan saraf, maka **Node 4 adalah Otaknya**. 

Di sistem konvensional, data HRD sering tumpang tindih (*Silo Data*). Arsitektur LoRaVault terbaru menerapkan **Single Source of Truth (SSOT)**. Sistem Keamanan (Tabel `users`) tidak lagi menyimpan Nama dan Departemen secara berulang, melainkan hanya berpegang pada NIK (Nomor Induk Karyawan). Ini menghemat *bandwidth* transmisi LoRa hingga 60% dan mencegah data menjadi basi jika ada mutasi karyawan.

Selain itu, seluruh logika bisnis (menerjemahkan fluktuasi Gram menjadi Peminjaman/Pengembalian) diproses 100% di level *Database* melalui *PostgreSQL Triggers*, membunuh *"Human Error"* hingga 0%.

---

## 🏛️ Filosofi Arsitektur (Engineering Rigor)

- **Database Normalization (SSOT):** Tabel `users` hanya berisi `rfid_uid` dan `nik`. Jika nama Budi diganti di tabel HRD (`hr_employees`), Dasbor LoRaVault secara otomatis menampilkan nama yang baru berkat relasi *Foreign Key*.
- **SICP (Data & Procedural Abstraction):** Node Edge dibuat sangat bodoh. Mereka hanya mengirim *"UID X, berat berubah Y gram"*. Seluruh logika bisnis (*State Machine*) dienkapsulasi di *PostgreSQL Triggers*. 
- **CLRS (Efisiensi Asimtotik):** Seiring berjalannya waktu, tabel transaksi akan membengkak hingga jutaan baris. Pencarian data beroperasi dalam **$\mathcal{O}(\log N)$ time complexity** melalui *B-Tree Indexing* yang ketat.
- **Security by Default (Row Level Security):** ESP32 secara kriptografis hanya diizinkan untuk `INSERT` data telemetri dan pendaftaran, tanpa bisa membaca atau menghapus riwayat apa pun.

---

## 🗄️ Skema Topologi (Data Structures)

1. **`hr_employees`**: Kebenaran tunggal untuk data manusia (Nama, Departemen).
2. **`users`**: Jembatan LoRaVault. Memetakan UID kartu RFID fisik ke NIK.
3. **`assets`**: Katalog inventaris brankas (Berat absolut dan toleransi penyusutan).
4. **`transactions_log`**: Buku besar yang tidak bisa diubah (*Immutable Ledger*).
5. **`active_loans`**: Tabel *Real-Time State* barang di tangan karyawan.

---

## 🚀 Setup & Deployment

1. Buka [Supabase](https://supabase.com) dan masuk ke menu **SQL Editor**.
2. *Copy* dan *Paste* ketiga file secara berurutan, lalu klik **Run**:
   - `01_schema.sql` (Fondasi tabel, SSOT, dan indeks B-Tree).
   - `02_functions_triggers.sql` (Menanamkan otak matematika dan pencegahan Indiana Jones Vulnerability).
   - `03_rls_policies.sql` (Mengunci gerbang akses *Zero-Trust*).
3. Tabel `hr_employees` secara otomatis akan diisi dengan data *Mock* (Fadhil dan Yudha) agar dasbor siap diuji coba.
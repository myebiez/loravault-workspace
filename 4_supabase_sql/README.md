<div align="center">
  <img src="https://img.shields.io/badge/NODE-04_THE_BRAIN-059669?style=for-the-badge" alt="Node 4">
  <img src="https://img.shields.io/badge/DATABASE-POSTGRESQL-blue?style=for-the-badge" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/PLATFORM-SUPABASE-green?style=for-the-badge" alt="Supabase">
  
  <h1>🧠 Node 4: The Mathematical Brain (Supabase)</h1>
  <p><b>State Machine, B-Tree Indexes, & Zero-Trust RLS Policies</b></p>
</div>

---

## 💼 The Executive Summary (Business Value)

Jika Node *Hardware* (Pi Zero & ESP32) adalah otot dan saraf, maka **Node 4 adalah Otaknya**. 

Di sistem manajemen inventaris konvensional, manusia harus menginput data: *"Budi meminjam Bor."* Di **LoRaVault**, manusia tidak menyentuh *software* sama sekali. Sistem ini menerjemahkan hukum fisika (perubahan berat dalam gram) menjadi sebuah entitas bisnis (Peminjaman atau Pengembalian) secara otomatis. 

Hal ini membunuh *"Human Error"* hingga 0% dan mengotomatisasi pencatatan inventaris (Admin Gudang Robotik), menghemat ratusan juta rupiah dari potensi kehilangan aset dan inefisiensi jam kerja operasional.

---

## 🏛️ Filosofi Arsitektur (Engineering Rigor)

- **SICP (Data & Procedural Abstraction):** Node Edge (ESP32/Pi Zero) dibuat **sangat bodoh**. Mereka tidak tahu apa itu "Peminjaman" atau "Pengembalian". Mereka hanya tahu: *"Ada UID X, dan berat berubah Y gram"*. Seluruh logika bisnis (*State Machine*) dienkapsulasi murni di dalam level *Database* melalui *PostgreSQL Triggers*. 
- **CLRS (Efisiensi Asimtotik):** Seiring berjalannya waktu, tabel transaksi akan membengkak hingga jutaan baris. Pencarian UID pengguna dan validasi berat aset dijamin berjalan dalam **$\mathcal{O}(\log N)$ time complexity** melalui implementasi **B-Tree Indexing** yang ketat. Sistem tidak akan pernah *ngelag*.
- **The Pragmatic Programmer (Design by Contract & Fail-Fast):** Data tidak valid dilarang keras masuk. Jika ada fluktuasi berat di bawah *margin of error* (15 gram), sistem akan mengabaikannya (Filter Noise).
- **Security by Default (Row Level Security):** ESP32 secara kriptografis hanya diizinkan melakukan perintah `INSERT` ke tabel transaksi. Jika kredensial ESP32 dibajak oleh *hacker*, mereka **TIDAK BISA** membaca data (*SELECT*), menghapus log (*DELETE*), atau memanipulasi peminjaman.

---

## 🗄️ Skema Topologi (Data Structures)

Sistem ini terdiri dari 4 tabel utama dengan relasi *Foreign Key* yang ketat:

1. **`users`**: Memetakan UID kartu RFID fisik ke identitas manusia (Nama, Departemen).
2. **`assets`**: Katalog inventaris brankas. Menyimpan nama alat, berat absolut (*baseline weight*), dan toleransi penyusutan (*tolerance*).
3. **`transactions_log`**: Buku besar yang tidak bisa diubah (*Immutable Ledger*). Menyimpan aliran data mentah dari ESP32.
4. **`active_loans`**: Tabel *Real-Time State*. Otomatis terisi saat ada barang keluar, dan otomatis terhapus saat barang masuk. Inilah yang ditampilkan di layar manajer.

---

## ⚙️ The Trigger: Menangkal "Indiana Jones Vulnerability"

Fungsi `process_vault_transaction()` adalah mahakarya algoritma sistem ini. Setiap kali ESP32 mengirim data baru:
1. **Identifikasi:** Sistem mencari siapa pemilik RFID secara $\mathcal{O}(\log N)$.
2. **Filter Fisika:** Jika fluktuasi berat $< 15g$, abaikan (dianggap guncangan pintu).
3. **Pencocokan Aset:** Sistem membandingkan delta berat dengan katalog aset. Jika seseorang mengambil barang 1.500g, lalu mengembalikan **batu** seberat 1.200g, sistem **TIDAK AKAN** mencoret peminjamannya karena berada di luar batas toleransi (*Indiana Jones rock-swap failed*).
4. **Mutasi State:** Mengotomatisasi perpindahan barang ke dalam atau keluar dari `active_loans`.

---

## 🚀 Setup & Deployment

Sistem ini didesain agar sangat mudah diimplementasikan (Krug's Law: *Don't Make Me Think*).

1. Buat proyek baru di [Supabase](https://supabase.com).
2. Masuk ke menu **SQL Editor**.
3. *Copy* dan *Paste* ketiga file secara berurutan, lalu klik **Run**:
   - `01_schema.sql` (Membangun fondasi tabel dan indeks).
   - `02_functions_triggers.sql` (Menanamkan otak matematika dan *State Machine*).
   - `03_rls_policies.sql` (Mengunci gerbang keamanan *Zero-Trust*).
4. (Opsional) Masukkan data awal (*seed data*) untuk tabel `users` (daftarkan kartu RFID Anda) dan `assets` (daftarkan barang uji coba Anda beserta berat aslinya).

---
*Dokumen ini dikompilasi berdasarkan filosofi engineering tingkat lanjut (SICP, CLRS, Pragmatic Programmer, DOET, & Krug's Laws).*
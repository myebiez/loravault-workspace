<div align="center">
  <img src="https://img.shields.io/badge/NODE-05_COMMAND_CENTER-4f46e5?style=for-the-badge" alt="Node 5">
  <img src="https://img.shields.io/badge/FRAMEWORK-NEXT.JS_14-black?style=for-the-badge" alt="Next.js">
  <img src="https://img.shields.io/badge/UI-TAILWIND_CSS-38bdf8?style=for-the-badge" alt="Tailwind CSS">
  
  <h1>📊 Node 5: The Command Center</h1>
  <p><b>Executive Real-Time Security Dashboard & Audit Interface</b></p>
</div>

---

## 💼 The Executive Summary (Business Value)

Sebuah sistem keamanan industri bernilai miliaran rupiah tidak ada artinya jika manajer membutuhkan waktu 20 menit hanya untuk memahami cara kerja aplikasinya. 

**Node 5 (Command Center)** adalah puncak dari arsitektur LoRaVault. Dibangun di atas Next.js, ini bukan sekadar dasbor; ini adalah **Viewport Eksekutif**. Sistem ini mengeliminasi *Refresh Button*—setiap perubahan fisik (gramasi) pada brankas di ruang bawah tanah akan terefleksi di layar eksekutif dalam hitungan milidetik secara *real-time*.

---

## 🎨 Filosofi UI/UX (Krug's "Don't Make Me Think" & Norman's DOET)

Antarmuka ini dirancang secara brutal untuk **Pemindaian Visual (Scannability)**, ditargetkan langsung untuk level eksekutif (CEO/CTO).
1. **Single Source of Truth (SSOT):** Dashboard secara otomatis melakukan *JOIN Query* ke tabel SDM (`hr_employees`) menggunakan NIK. Ini memastikan identitas peminjam selalu 100% akurat sesuai database kantor.
2. **Zero Cognitive Load (Krug):** Tidak ada ambiguitas angka mentah. Fluktuasi `-500g` diterjemahkan secara semantik menjadi lencana **"Aset Keluar"** (Merah), dan `+500g` menjadi **"Aset Masuk"** (Hijau).
3. **High-Contrast Corporate Aesthetic:** Menggunakan palet `slate` minimalis untuk memastikan tingkat keterbacaan instan tertinggi di layar *mobile* satpam maupun presentasi dewan direksi, menghindari desain *dark-mode* berlebihan yang memperlambat mata.
4. **Immediate Feedback (DOET):** Dilengkapi dengan indikator kesehatan *Websocket* (Live Beacon) bergaya *pulsing radar* yang memberikan umpan balik psikologis bahwa sistem aktif melindungi aset.

---

## 🚀 Panduan Pengembangan Lokal (Localhost)

Sebelum menyentuh *Cloud*, sistem harus divalidasi di mesin lokal (CachyOS/Windows/macOS).

### 1. Instalasi Dependensi
Pastikan Node.js terinstal, lalu jalankan di terminal:
```bash
cd 5_dashboard_nextjs
npm install
```
### 2. Injeksi Kredensial (Design by Contract)
Buat file .env.local di root folder 5_dashboard_nextjs/ dan masukkan kunci dari Supabase:
```bash
NEXT_PUBLIC_SUPABASE_URL="https://[PROJECT_ID].supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJh..."
```
(Catatan: Tanpa kredensial ini, aplikasi akan menolak untuk me-render data).
### 3. Eksekusi Dev Server
```bash
npm run dev
```
Buka http://localhost:3000 di browser.
### 4. Uji Coba Real-Time (Simulasi)
Buka Supabase SQL Editor di tab sebelahnya dan eksekusi perintah ini:
```bash
SQLINSERT INTO transactions_log (rfid_uid, weight_delta) VALUES ('SIMULASI_LOKAL', -500);
```
Lihat ke layar localhost:3000 Anda. Data peminjaman akan muncul dalam $\sim 200$ milidetik tanpa perlu refresh halaman.

## ☁️ Production Deployment (Vercel)
Sistem ini didesain 100% native untuk Vercel (kreator Next.js) untuk menjamin zero-downtime dan maintenance-free scaling.
### Fase 1: Sinkronisasi GitHubBashgit init
```bash
git add .
git commit -m "Initial commit: LoRaVault Command Center"
git branch -M main
git remote add origin [https://github.com/](https://github.com/)[username_kamu]/loravault-dashboard.git
git push -u origin main
```
### Fase 2: Vercel Integration
1. Login ke Vercel dengan akun GitHub Anda.
2. Klik Add New... $\rightarrow$ Project.
3. Import repositori loravault-dashboard.
4. ⚠️ KRUSIAL: Buka bagian Environment Variables di layar konfigurasi Vercel, lalu tambahkan:
  - NEXT_PUBLIC_SUPABASE_URL = https://[proyek_kamu].supabase.co
  - NEXT_PUBLIC_SUPABASE_ANON_KEY = eyJh...
5. Klik Deploy.
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

## 🎨 Filosofi UI/UX (Krug's "Don't Make Me Think")

Antarmuka ini dirancang secara brutal untuk **Pemindaian Visual (Scannability)**, bukan untuk dibaca seperti buku.
1. **Zero Cognitive Load:** Tidak ada ambiguitas. Kami mengganti angka mentah (misal: `-500g`) dengan status semantik yang eksplisit (**"Taken"** berwarna merah, atau **"Returned"** berwarna hijau).
2. **High-Contrast Visual Hierarchy:** Menggunakan latar belakang *light-gray* dengan teks gelap untuk memastikan keterbacaan instan di bawah sinar matahari atau layar *mobile* satpam, meninggalkan estetika *dark-mode* yang justru memperlambat pemindaian (*scanning*).
3. **DOET Feedback Loop:** Dilengkapi dengan indikator kesehatan *Websocket* (Live Connection) yang memberikan umpan balik psikologis bahwa sistem sedang mengawasi aset tanpa henti.

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

Buat file `.env.local` di root folder `5_dashboard_nextjs/` dan masukkan kunci dari Supabase:

```env
NEXT_PUBLIC_SUPABASE_URL="https://[PROJECT_ID].supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJh..."
```

*(Catatan: Tanpa kredensial ini, aplikasi akan menolak untuk me-render data).*

### 3. Eksekusi Dev Server

```bash
npm run dev
```

Buka `http://localhost:3000` di *browser*.

### 4. Uji Coba Real-Time (Simulasi)

Buka [Supabase SQL Editor](https://www.google.com/search?q=https://supabase.com) di *tab* sebelahnya dan eksekusi perintah ini:

```sql
INSERT INTO transactions_log (rfid_uid, weight_delta) VALUES ('SIMULASI_LOKAL', -500);
```

Lihat ke layar `localhost:3000` Anda. Data peminjaman akan muncul dalam $\sim 200$ milidetik tanpa perlu *refresh* halaman.

---

## ☁️ Production Deployment (Vercel)

Sistem ini didesain 100% *native* untuk Vercel (kreator Next.js) untuk menjamin *zero-downtime* dan *maintenance-free scaling*.

### Fase 1: Sinkronisasi GitHub

```bash
git init
git add .
git commit -m "Initial commit: LoRaVault Command Center"
git branch -M main
git remote add origin [https://github.com/](https://github.com/)[username_kamu]/loravault-dashboard.git
git push -u origin main
```

### Fase 2: Vercel Integration

1. Login ke [Vercel](https://www.google.com/search?q=https://vercel.com) dengan akun GitHub Anda.
2. Klik **Add New...** $\rightarrow$ **Project**.
3. Import repositori `loravault-dashboard`.
4. ⚠️ **KRUSIAL:** Buka bagian **Environment Variables** di layar konfigurasi Vercel, lalu tambahkan:
* `NEXT_PUBLIC_SUPABASE_URL` = `https://[proyek_kamu].supabase.co`
* `NEXT_PUBLIC_SUPABASE_ANON_KEY` = `eyJh...`


5. Klik **Deploy**.

Dalam 2 menit, Command Center LoRaVault Anda akan *Live* secara global dan siap dipresentasikan di hadapan dewan direksi atau juri kompetisi.

---

*Dokumen ini dikompilasi berdasarkan filosofi engineering tingkat lanjut (SICP, CLRS, Pragmatic Programmer, DOET, & Krug's Laws).*

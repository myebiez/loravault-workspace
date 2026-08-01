<div align="center">
  <img src="https://img.shields.io/badge/NODE-03_THE_EYE-b91c1c?style=for-the-badge" alt="Node 3">
  <img src="https://img.shields.io/badge/UI-TKINTER-yellow?style=for-the-badge" alt="Tkinter">
  <img src="https://img.shields.io/badge/VISION-ARDUCAM_CSI-blue?style=for-the-badge" alt="CSI Camera">
  
  <h1>👁️ Node 3: The Eye (Pi 3 Audit Desktop)</h1>
  <p><b>Event-Driven Visual Audit & Notification Matrix</b></p>
</div>

---

## 💼 The Executive Summary (Business Value)

CCTV konvensional merekam video 24/7, memaksa manajemen untuk membuang waktu berjam-jam memutar ulang rekaman untuk mencari bukti pencurian. 

**Node 3 (The Eye)** mendisrupsi pendekatan tersebut. Modul ini beroperasi sebagai *Event-Driven Audit Trail*. Ia tidak merekam video, melainkan berdiri pasif mendengarkan database (Supabase). Ketika sensor fisik di dalam brankas mendeteksi perubahan berat, sistem ini akan bereaksi dalam hitungan milidetik: memotret wajah pengguna dan mengirimkannya ke Telegram Manajer. Ini adalah solusi absolut untuk memitigasi **"Indiana Jones Vulnerability"** (percobaan menipu sensor berat menggunakan batu/benda lain).

---

## 🏛️ Filosofi Arsitektur (Engineering Rigor)

- **CLRS (Efisiensi Asimtotik):** Pencarian bukti kejahatan diubah dari $\mathcal{O}(N)$ (mencari dalam durasi video yang panjang) menjadi $\mathcal{O}(1)$ (satu foto presisi yang terikat langsung dengan satu ID Transaksi dan Waktu).
- **The Pragmatic Programmer (Orthogonality & Concurrency):** Proses mendengarkan Cloud (I/O Bound) dan proses me-render GUI (Main Thread) dipisahkan secara absolut. Mereka hanya berkomunikasi melalui *Thread-Safe Queue* (`queue.Queue()`). Jika koneksi internet putus, GUI tidak akan *freeze* atau *crash*.
- **Steve Krug's 1st Law (Don't Make Me Think):** Antarmuka Tkinter dirancang brutalist dan masif. Satpam atau operator tidak perlu membaca teks kecil. Warna layar merah (Anomali) atau hijau (Aman) memberikan umpan balik seketika.
- **SICP (Procedural Abstraction):** Akses ke *hardware* kamera diabstraksikan melalui OS Shell (`subprocess.run`), memisahkan kompleksitas *driver* kamera dari logika Python murni.

---

## 🛠️ Persyaratan Perangkat Keras

1. **Raspberry Pi 3 (atau varian yang lebih tinggi)** dengan koneksi Wi-Fi ke jaringan gedung.
2. **Kamera Arducam / Pi Camera Module** (Dihubungkan melalui port pita CSI bawaan motherboard, BUKAN USB).
3. **Layar LCD** (Disarankan layar sentuh 5" atau 7" yang terhubung via HDMI/DSI untuk *dashboard display*).

---

## 🚀 Setup & Deployment

### Langkah 1: Aktivasi Kamera CSI
Kamera pita Raspberry Pi memerlukan aktivasi pada tingkat sistem operasi (Raspberry Pi OS versi Bullseye/Bookworm).
```bash
sudo raspi-config
```

Pilih `3 Interface Options` $\rightarrow$ `I1 Legacy Camera` (atau sesuaikan dengan konfigurasi `libcamera` pada OS terbaru Anda) $\rightarrow$ **Enable**. Kemudian `reboot`.

### Langkah 2: Instalasi Dependensi Terisolasi

Gunakan Virtual Environment untuk mematuhi prinsip *Sandboxing*:

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv libjpeg-dev zlib1g-dev -y

# Buat dan aktifkan virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependensi Python
pip install -r requirements.txt
```

### Langkah 3: Injeksi Kredensial (Design by Contract)

Buat file `.env` di *root* direktori `3_ai_camera_pi3_desktop/`. Sistem dirancang untuk *Fail-Fast* dan akan *crash* saat *booting* jika file ini tidak lengkap.

```env
SUPABASE_URL="https://[PROJECT_ID].supabase.co"
SUPABASE_KEY="eyJh...[ANON_KEY]..."
TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrSTUvwxYZ"
TELEGRAM_CHAT_ID="-1001234567890"
```

### Langkah 4: Eksekusi GUI

```bash
# Pastikan berada di dalam virtual environment
python3 main.py
```

Aplikasi akan mengambil alih layar penuh (*fullscreen*). Untuk keluar dari mode kiosk selama pengembangan, klik tombol **"EXIT UI"** di bagian bawah layar.

---

## 📡 Mekanisme Notifikasi Telegram

Ketika anomali terdeteksi (contoh: berat yang dikembalikan tidak sesuai dengan batas toleransi aset), kelas `TelegramNotifier` akan menyatukan ID RFID, $\Delta$ Berat, dan foto *snapshot* ke dalam satu muatan HTTP POST.

Notifikasi akan masuk ke grup Telegram manajemen secara *real-time*, memberikan visibilitas instan kepada eksekutif yang sedang berada di luar area fasilitas.

---

*Dokumen ini dikompilasi berdasarkan filosofi engineering tingkat lanjut (SICP, CLRS, Pragmatic Programmer, DOET, & Krug's Laws).*
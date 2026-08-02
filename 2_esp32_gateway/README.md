<div align="center">
  <img src="https://img.shields.io/badge/NODE-02_THE_BRIDGE-2563eb?style=for-the-badge" alt="Node 2">
  <img src="https://img.shields.io/badge/FRAMEWORK-PLATFORMIO-orange?style=for-the-badge" alt="PlatformIO">
  <img src="https://img.shields.io/badge/LANG-C++-blue?style=for-the-badge" alt="C++">
  
  <h1>🌉 Node 2: The Bridge (ESP32 Gateway)</h1>
  <p><b>Stateless LoRa-to-HTTP Telemetry Courier</b></p>
</div>

---

## 💼 The Executive Summary (Business Value)

Jika **Node 1 (Pi Zero)** adalah otak yang terkunci di dalam brankas baja (Sangkar Faraday), maka **Node 2 (ESP32 Gateway)** adalah telinga yang berada di dunia luar (Pos Satpam/Ruang Server). 

Tugas Node 2 sangat spesifik dan murni: **Mendengarkan frekuensi radio LoRa dari brankas, dan menembakkannya langsung ke Cloud (Supabase) menggunakan jaringan Wi-Fi gedung.** 

Dengan memisahkan fungsi ini (*Orthogonality*), matinya router Wi-Fi gudang atau sabotase kabel di area brankas **TIDAK AKAN** melumpuhkan kemampuan brankas untuk berteriak meminta tolong via gelombang radio. Ini adalah jaminan *Uptime 99.9%* untuk keamanan aset Anda.

---

## 🏛️ Filosofi Arsitektur (Engineering Rigor)

- **The Pragmatic Programmer (Decoupling & Security):** Kredensial Wi-Fi dan API Key Supabase **TIDAK PERNAH** di- *hardcode* di dalam source code `.cpp`. Semua rahasia disuntikkan secara dinamis saat proses kompilasi (*compile-time*) melalui `platformio.ini` (`build_flags`). 
- **SICP (Procedural Abstraction):** File `main.cpp` tidak memiliki logika bisnis. Ia hanya bertindak sebagai konduktor yang memanggil modul `wifi_manager`, `lora_receiver`, dan `supabase_client` secara berurutan.
- **CLRS (Asymptotic Efficiency):** Parsing string UART dilakukan dalam kompleksitas waktu $\mathcal{O}(N)$ (linear terhadap panjang *buffer*), memastikan tidak ada hambatan prosesor saat paket data masuk. Manajemen memori menggunakan alokasi statis (`StaticJsonDocument<200>`) untuk mencegah *Heap Fragmentation* yang sering membunuh ESP32.
- **DOET (Constraints & Mapping):** Modul LoRa pada node ini dikunci secara fisik pada state $\mathcal{O}(1)$ (Mode Transmisi konstan) dengan menyolder pin M0 dan M1 langsung ke Ground (GND). Menghilangkan kerumitan penggantian *state* pada perangkat lunak.

---

## 🛠️ Cetak Biru Perangkat Keras (Perfboard Wiring)

ESP32 beroperasi pada logika 3.3V. Pastikan tidak memberikan tegangan 5V pada jalur komunikasi.

### 1. Sistem Daya (Power Bus)
*   **VCC LoRa HAT:** Dihubungkan ke pin **3V3** (atau 5V/VIN, karena HAT Waveshare memiliki *regulator step-down* bawaan, namun jalur data tetap 3.3V).
*   **GND LoRa HAT:** Dihubungkan ke pin **GND** ESP32.

### 2. Jalur Komunikasi (Cross-UART)
Menggunakan Hardware Serial 2 pada ESP32 untuk menghindari konflik dengan Serial Monitor USB (Serial 0).
*   **TX LoRa** $\rightarrow$ Dihubungkan ke pin **RX2 (GPIO 16)** ESP32.
*   **RX LoRa** $\rightarrow$ Dihubungkan ke pin **TX2 (GPIO 17)** ESP32.

### 3. Penguncian Mode (Hardware Constraint)
Gateway hanya bertugas mendengar. Tidak ada mode *sleep* atau *config*.
*   **M0 LoRa** $\rightarrow$ Solder permanen ke **GND**.
*   **M1 LoRa** $\rightarrow$ Solder permanen ke **GND**.

---

## 🚀 Setup & Deployment (PlatformIO)

Jangan menggunakan Arduino IDE konvensional. Proyek ini menggunakan **PlatformIO** untuk manajemen *dependency* yang terisolasi dan injeksi variabel lingkungan yang aman.

### Langkah 1: Konfigurasi Keamanan (Wajib!)
Buka file `platformio.ini` dan ganti nilai `build_flags` dengan kredensial asli Anda. **Jangan hapus tanda kutip miring (`\"`)!**

```ini
build_flags =
    -D WIFI_SSID=\"Gudang_WiFi_2.4G\"
    -D WIFI_PASS=\"SuperSecretPassword\"
    -D SUPABASE_URL=\"https://[PROJECT_ID].supabase.co\"
    -D SUPABASE_KEY=\"eyJh...[ANON_KEY]...\"
```

### Langkah 2: Build & Flash

1. Buka folder `2_esp32_gateway` di VS Code (sebagai *root workspace* agar PlatformIO aktif).
2. Klik ikon **Tanda Centang (✓)** di bilah bawah untuk mengkompilasi (*Build*). PlatformIO akan mengunduh `ArduinoJson` secara otomatis.
3. Hubungkan ESP32 ke PC via USB.
4. Klik ikon **Tanda Panah Kanan (→)** untuk melakukan proses *Upload / Flash*. (Tahan tombol `BOOT` pada ESP32 jika muncul pesan *Connecting...*).


### Langkah 3: Verifikasi Log (Serial Monitor)

Klik ikon **Steker (🔌)** di bilah bawah untuk membuka Serial Monitor (Baudrate 115200). 

Ketika ada pendaftaran pegawai baru (Air-Gapped Sync), log akan menampilkan:
```text
[LoRa] REG Diterima -> UID: 9876543210 | NIK: EMP-2026-001
[Supabase] Executing POST to: [https://xxx.supabase.co/rest/v1/users](https://xxx.supabase.co/rest/v1/users)
[Supabase] Success! Payload accepted. HTTP 201
```

Ketika ada aksi peminjaman/pengembalian aset fisik, log akan menampilkan:

```text
[LoRa] TLM Diterima -> UID: 9876543210 | Delta: -1532.00g
[Supabase] Executing POST to: [https://xxx.supabase.co/rest/v1/transactions_log](https://xxx.supabase.co/rest/v1/transactions_log)
[Supabase] Success! Payload accepted. HTTP 201
```
---

*Dokumen ini dikompilasi berdasarkan filosofi engineering tingkat lanjut (SICP, CLRS, Pragmatic Programmer, DOET, & Krug's Laws).*
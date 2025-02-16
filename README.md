# Telegram - Journal Search

## 📌 Deskripsi Proyek
Telegram - Journal Search adalah bot otomatis yang memungkinkan pengguna mencari jurnal akademis langsung dari Google Scholar melalui Telegram. Bot ini menggunakan Selenium untuk scraping data dan menampilkan hasil pencarian dalam format yang mudah dibaca di Telegram.

## 🚀 Fitur Utama
- 🔍 **Pencarian Jurnal**: Gunakan perintah `/search` untuk mencari jurnal akademis berdasarkan kata kunci.
- 📚 **Hasil Detail**: Menampilkan judul, penulis, tahun publikasi, dan tautan ke jurnal yang ditemukan.
- 🤖 **Simulasi Perilaku Manusia**: Menambahkan jeda acak untuk menghindari deteksi bot oleh Google.
- 🔄 **Rotasi User-Agent**: Menggunakan berbagai User-Agent untuk meningkatkan anonimitas.
- 🍪 **Pengelolaan Cookies**: Menyimpan dan memuat cookies untuk sesi pencarian yang lebih stabil.
- 🛠 **Logging**: Mencatat aktivitas bot untuk pemantauan dan debugging.

## ⚙️ Instalasi
### 1️⃣ Persyaratan
- Python 3.x
- `pip` package manager
- Driver Web Selenium (Firefox Geckodriver)
- Akun Telegram Bot API

### 2️⃣ Instalasi Dependensi
Jalankan perintah berikut untuk menginstal dependensi yang diperlukan:
```bash
pip install selenium python-telegram-bot
```

### 3️⃣ Menjalankan Bot
1. Pastikan `geckodriver` sudah terinstal dan berada dalam PATH.
2. Ganti token bot di file `main.py` dengan token Anda.
3. Jalankan bot dengan perintah:
```bash
python main.py
```

## 🔧 Konfigurasi
### Mengatur Token Bot Telegram
Gantilah baris berikut di `main.py` dengan token bot Anda:
```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

## 📝 Cara Penggunaan
1. Jalankan bot.
2. Kirimkan perintah `/start` untuk memulai interaksi.
3. Gunakan `/search` diikuti dengan kata kunci untuk mencari jurnal.
4. Bot akan memberikan daftar hasil pencarian beserta tautan untuk membaca lebih lanjut.

## 💡 Catatan Penting
- Pastikan jaringan internet stabil untuk menghindari error saat scraping.
- Jangan melakukan pencarian berlebihan dalam waktu singkat agar tidak diblokir oleh Google.

## 🤝 Kontribusi
Kontribusi selalu diterima! Jika Anda menemukan bug atau memiliki fitur baru yang ingin ditambahkan, silakan buat pull request atau buka issue.

## 📜 Lisensi
Proyek ini dirilis di bawah lisensi MIT. Silakan gunakan dan kembangkan sesuai kebutuhan Anda! 🚀


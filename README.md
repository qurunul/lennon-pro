# Proyek Steganografi Audio dengan Enkripsi AES-128
Proyek ini mengimplementasikan steganografi audio menggunakan metode Least Significant Bit (LSB) yang dikombinasikan dengan enkripsi AES-128 dalam mode CBC. Tujuannya adalah menyembunyikan pesan rahasia dalam file audio (MP3, WAV, FLAC) dan mengevaluasi kualitas serta ketahanan sistem terhadap gangguan seperti kompresi dan noise. Proyek ini digunakan untuk penelitian skripsi, dengan pengujian pada 4 file audio (3 MP3, 1 WAV) dan panjang pesan 100, 300, dan 500 karakter.

## Fitur Utama
- **Steganografi LSB**: Menyisipkan dan mengekstrak pesan dalam file audio.
- **Enkripsi AES-128**: Mengamankan pesan sebelum penyisipan.
- **Analisis Kualitas**: Menghitung MSE, PSNR, SNR, spectral distortion, dan THD.
- **Pengujian Ketahanan**: Menguji ketahanan terhadap kompresi MP3 (128k, 320k) dan noise (rendah, sedang, tinggi).
- **Pengujian MOS**: Evaluasi subjektif kualitas audio.
- **Otomatisasi**: Skrip untuk pengujian batch dan pembuatan tabel hasil.

## Struktur Proyek
```
steganografi_audio/
├── .venv/                          # Virtual environment
├── .vscode/                        # Konfigurasi VS Code (settings.json, launch.json, tasks.json)
├── src/                            # Kode sumber
│   ├── enkripsi.py                 # Modul enkripsi AES-128
│   ├── audio_steganografi.py       # Modul steganografi LSB
│   ├── utils.py                    # Fungsi utilitas (konversi, validasi)
│   └── quality_analyzer.py         # Analisis kualitas audio
├── samples/                        # File audio sampel (sample1.mp3, sample2.mp3, sample3.mp3, sample4.wav)
├── output/                         # File output (audio stego, laporan, grafik)
├── temp/                           # File sementara untuk pengujian
├── tests/                          # Folder untuk pengujian unit (opsional)
├── backup_proyek_28juli2025/       # Folder backup proyek
├── main.py                         # Skrip utama untuk perintah CLI
├── setup_vscode.py                 # Skrip untuk mengatur VS Code
├── requirements.txt                # Dependensi proyek
├── batch_test.py                   # Batch embedding dan extraction
├── batch_quality.py                # Batch analisis kualitas
├── batch_robustness.py             # Batch pengujian ketahanan
├── mos_test.py                     # Pengujian MOS
├── generate_results_table.py       # Pembuatan tabel hasil
├── .env.example                    # Contoh variabel lingkungan
├── .gitignore                      # File untuk mengabaikan file sementara
└── README.md                       # Dokumentasi ini
```
## Prasyarat
- Python 3.8 atau lebih baru
- FFmpeg terinstal (unduh di sini)
- Sistem operasi: Windows (juga kompatibel dengan macOS/Linux)

## Instalasi

### Buat dan aktifkan virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
atau: source .venv/bin/activate  # macOS/Linux
```

### Instal dependensi:
```bash
pip install -r requirements.txt
```

### Instal FFmpeg:
- Unduh dari https://www.gyan.dev/ffmpeg/builds/.
- Tambahkan ffmpeg\bin ke PATH sistem.
- Verifikasi: ffmpeg -version dan ffprobe -version.


### Siapkan file audio:
- Tempatkan file audio (MP3, WAV, FLAC) di folder `samples/`.
- Contoh: sample1.mp3, sample2.mp3, sample3.mp3, sample4.wav (durasi minimal 30 detik, sampling rate 44.1 kHz).


### Konfigurasi VS Code (opsional):
```bash
python setup_vscode.py
```
- Pastikan settings.json menggunakan .venv\Scripts\python.exe (Windows) atau .venv/bin/python (macOS/Linux).


## Penggunaan
Gunakan `main.py` untuk menjalankan perintah steganografi dan analisis:

### Cek informasi file audio:
```bash
python main.py info samples/sample1.mp3
```

### Embedding pesan:
```bash
python main.py embed samples/sample1.mp3 "Pesan rahasia" password123 --format mp3
```
- Output: `output/sample1_stego.mp3`


### Extraction pesan:
```bash
python main.py extract output/sample1_stego.mp3 password123
```

### Analisis kualitas:
```bash
python main.py quality samples/sample1.mp3 output/sample1_stego.mp3
```
- Hasil disimpan di `output/quality_report.txt`.


### Pengujian ketahanan:
```bash
python main.py robustness output/sample1_stego.mp3 password123 "Pesan rahasia"
```

### Pengujian batch:
- Embedding dan extraction:
```bash
python batch_test.py
```
- Analisis kualitas:
```bash
python batch_quality.py
```
- Pengujian ketahanan:
```bash
python batch_robustness.py
```

### Pengujian MOS:
- Putar audio untuk responden:
```bash
python mos_test.py
```

### Buat tabel hasil:
```bash
python generate_results_table.py
```
- Hasil disimpan di `output/results_table.md`.


## Contoh Hasil Pengujian
Berikut adalah contoh tabel hasil untuk BAB IV skripsi:

| File Audio    | Format | Panjang Pesan | MSE  | PSNR (dB) | SNR (dB) | Gangguan       | BER (%) | Status Ekstraksi | MOS |
| ------------- |--------|----------------|------|-----------|----------|----------------|---------|-------------------|-----|
| sample1.mp3   | MP3    | 100 karakter   | 0.02 | 65.23     | 62.15    | Kompresi 128k  | 0.12    | Berhasil          | 4.5 |
| sample4.wav   | WAV    | 300 karakter   | 0.03 | 63.88     | 60.47    | Noise Sedang   | 5.67    | Gagal             | 4.2 |

- Grafik: Lihat `output/waveform_comparison.png dan output/spectrum_comparison.png`.
- Laporan Kualitas: Lihat `output/quality_report.txt`.

## Catatan

- Pastikan file audio di `samples/` memiliki durasi cukup untuk pesan panjang (100, 300, 500 karakter).
- Untuk pengujian MOS, gunakan 10–20 responden untuk skor 1–5.
- Backup proyek setiap hari.

## Kontribusi
Proyek ini dikembangkan untuk penelitian skripsi. Untuk pertanyaan atau saran, hubungi qurunul.

## Lisensi
MIT License
import os
from quality_analyzer import QualityAnalyzer
from audio_steganografi import AudioSteganography

audio_files = ["sample1.mp3", "sample2.mp3", "sample3.mp3", "sample4.wav"]
messages = [
    "Ini adalah pesan rahasia untuk pengujian steganografi audio dengan panjang 100 karakter, aman dan terenkripsi dengan AES-128.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
]
password = "password123"
analyzer = QualityAnalyzer()
stego = AudioSteganography()

table = "| File Audio | Format | Panjang Pesan | MSE | PSNR (dB) | SNR (dB) | Gangguan | BER (%) | Status Ekstraksi | MOS |\n"
table += "|------------|--------|---------------|-----|-----------|----------|----------|---------|------------------|-----|\n"

for audio in audio_files:
    original = f"samples/{audio}"
    stego_file = f"output/{audio.split('.')[0]}_stego.{audio.split('.')[-1]}"
    if os.path.exists(stego_file):
        metrics = analyzer.calculate_metrics(original, stego_file)
        for msg in messages:
            robustness = stego.test_robustness(*stego._load_audio(stego_file), password, msg)
            for condition, result in robustness.items():
                table += (f"| {audio} | {audio.split('.')[-1].upper()} | {len(msg)} karakter | "
                        f"{metrics['mse']:.2f} | {metrics['psnr']:.2f} | {metrics['snr']:.2f} | "
                        f"{condition} | {result['ber']:.2f} | {'Berhasil' if result['success'] else 'Gagal'} | - |\n")

with open("output/results_table.md", "w") as f:
    f.write(table)
print("Tabel hasil disimpan di output/results_table.md")
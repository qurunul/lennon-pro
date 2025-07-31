import numpy as np
import soundfile as sf
import librosa
import matplotlib.pyplot as plt
import os
from src.utils import convert_to_wav

class QualityAnalyzer:
    """Kelas untuk menganalisis kualitas audio."""
    
    def calculate_metrics(self, original_file: str, stego_file: str) -> dict:
        """Menghitung metrik kualitas (MSE, PSNR, SNR, dll.)."""
        original, sr = sf.read(convert_to_wav(original_file))
        stego, _ = sf.read(convert_to_wav(stego_file))
        if len(original.shape) > 1:
            original = original[:, 0]
        if len(stego.shape) > 1:
            stego = stego[:, 0]
        
        # MSE
        mse = np.mean((original - stego) ** 2)
        
        # PSNR
        max_value = np.max(np.abs(original))
        psnr = 20 * np.log10(max_value / np.sqrt(mse)) if mse > 0 else float('inf')
        
        # SNR
        signal_power = np.mean(original ** 2)
        noise_power = mse
        snr = 10 * np.log10(signal_power / noise_power) if noise_power > 0 else float('inf')
        
        # Spectral Distortion
        spec_orig = np.abs(librosa.stft(original))
        spec_stego = np.abs(librosa.stft(stego))
        spectral_distortion = np.mean((spec_orig - spec_stego) ** 2)
        
        # THD (Total Harmonic Distortion)
        thd = np.sum(np.abs(spec_stego - spec_orig)) / np.sum(np.abs(spec_orig)) * 100
        
        return {
            "mse": mse,
            "psnr": psnr,
            "snr": snr,
            "spectral_distortion": spectral_distortion,
            "thd": thd
        }

    def generate_quality_report(self, original_file: str, stego_file: str) -> str:
        """Menghasilkan laporan kualitas dalam file teks."""
        metrics = self.calculate_metrics(original_file, stego_file)
        report_file = f"output/quality_report_{os.path.basename(original_file).split('.')[0]}.txt"
        with open(report_file, "w") as f:
            f.write(f"Quality Report: {original_file} vs {stego_file}\n")
            f.write(f"MSE: {metrics['mse']:.2f}\n")
            f.write(f"PSNR: {metrics['psnr']:.2f} dB\n")
            f.write(f"SNR: {metrics['snr']:.2f} dB\n")
            f.write(f"Spectral Distortion: {metrics['spectral_distortion']:.2f}\n")
            f.write(f"THD: {metrics['thd']:.2f}%\n")
        return report_file

    def plot_waveform_comparison(self, original_file: str, stego_file: str):
        """Membuat grafik perbandingan waveform."""
        original, sr = sf.read(convert_to_wav(original_file))
        stego, _ = sf.read(convert_to_wav(stego_file))
        time = np.arange(len(original)) / sr
        plt.figure(figsize=(10, 4))
        plt.plot(time, original, label="Original", alpha=0.7)
        plt.plot(time, stego, label="Stego", alpha=0.7)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.title("Waveform Comparison")
        plt.legend()
        plt.savefig(f"output/waveform_comparison_{os.path.basename(original_file).split('.')[0]}.png")
        plt.close()

    def plot_spectrum_comparison(self, original_file: str, stego_file: str):
        """Membuat grafik perbandingan spektrum."""
        original, sr = sf.read(convert_to_wav(original_file))
        stego, _ = sf.read(convert_to_wav(stego_file))
        spec_orig = np.abs(librosa.stft(original))
        spec_stego = np.abs(librosa.stft(stego))
        freqs = librosa.fft_frequencies(sr=sr)
        plt.figure(figsize=(10, 4))
        plt.semilogx(freqs, np.mean(spec_orig, axis=1), label="Original", alpha=0.7)
        plt.semilogx(freqs, np.mean(spec_stego, axis=1), label="Stego", alpha=0.7)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.title("Spectrum Comparison")
        plt.legend()
        plt.savefig(f"output/spectrum_comparison_{os.path.basename(original_file).split('.')[0]}.png")
        plt.close()
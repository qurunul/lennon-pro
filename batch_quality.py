from quality_analyzer import QualityAnalyzer
import os

audio_files = ["sample1.mp3", "sample2.mp3", "sample3.mp3", "sample4.wav"]
analyzer = QualityAnalyzer()

for audio in audio_files:
    original = f"samples/{audio}"
    stego = f"output/{audio.split('.')[0]}_stego.{audio.split('.')[-1]}"
    if os.path.exists(stego):
        report_file = analyzer.generate_quality_report(original, stego)
        print(f"Laporan untuk {audio}: {report_file}")
        analyzer.plot_waveform_comparison(original, stego)
        analyzer.plot_spectrum_comparison(original, stego)
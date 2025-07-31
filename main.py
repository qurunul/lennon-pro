import argparse
import os
from src.audio_steganografi import AudioSteganography
from src.quality_analyzer import QualityAnalyzer
from src.utils import validate_file, get_audio_info

def main(args=None):
    """Fungsi utama untuk menjalankan perintah CLI."""
    parser = argparse.ArgumentParser(description="Steganografi Audio dengan Enkripsi AES-128")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser untuk info
    info_parser = subparsers.add_parser("info", help="Menampilkan informasi audio")
    info_parser.add_argument("input_file", type=str, help="Path ke file audio")

    # Subparser untuk embed
    embed_parser = subparsers.add_parser("embed", help="Menyisipkan pesan ke audio")
    embed_parser.add_argument("input_file", type=str, help="Path ke file audio")
    embed_parser.add_argument("message", type=str, help="Pesan untuk disisipkan")
    embed_parser.add_argument("password", type=str, help="Kata sandi untuk enkripsi")
    embed_parser.add_argument("--format", type=str, default="wav", choices=["wav", "mp3", "flac"], 
                            help="Format file output")

    # Subparser untuk extract
    extract_parser = subparsers.add_parser("extract", help="Mengekstrak pesan dari audio")
    extract_parser.add_argument("input_file", type=str, help="Path ke file audio stego")
    extract_parser.add_argument("password", type=str, help="Kata sandi untuk dekripsi")

    # Subparser untuk quality
    quality_parser = subparsers.add_parser("quality", help="Menganalisis kualitas audio")
    quality_parser.add_argument("original_file", type=str, help="Path ke file audio asli")
    quality_parser.add_argument("stego_file", type=str, help="Path ke file audio stego")

    # Subparser untuk robustness
    robustness_parser = subparsers.add_parser("robustness", help="Menguji ketahanan steganografi")
    robustness_parser.add_argument("stego_file", type=str, help="Path ke file audio stego")
    robustness_parser.add_argument("password", type=str, help="Kata sandi untuk dekripsi")
    robustness_parser.add_argument("original_message", type=str, help="Pesan asli untuk perbandingan")

    args = parser.parse_args(args)

    stego = AudioSteganography()
    analyzer = QualityAnalyzer()

    if args.command == "info":
        if validate_file(args.input_file):
            info = get_audio_info(args.input_file)
            print(f"Info Audio: {args.input_file}")
            print(f"Sample Rate: {info['sample_rate']} Hz")
            print(f"Channels: {info['channels']}")
            print(f"Duration: {info['duration']:.2f} seconds")
            print(f"Max Message Length: {info['max_message_length']} characters")
        else:
            print(f"❌ File tidak valid: {args.input_file}")

    elif args.command == "embed":
        if validate_file(args.input_file):
            output_file = f"output/{os.path.basename(args.input_file).split('.')[0]}_stego.{args.format}"
            try:
                result = stego.embed_message(args.input_file, args.message, args.password, output_file, args.format)
                print(f"✅ Pesan disisipkan ke: {result['output_file']}")
                metrics = analyzer.calculate_metrics(args.input_file, output_file)
                print(f"MSE: {metrics['mse']:.2f}, PSNR: {metrics['psnr']:.2f} dB, SNR: {metrics['snr']:.2f} dB")
            except Exception as e:
                print(f"❌ Error dalam penyisipan pesan: {str(e)}")
        else:
            print(f"❌ File tidak valid: {args.input_file}")

    elif args.command == "extract":
        if validate_file(args.input_file):
            try:
                message = stego.extract_message(args.input_file, args.password)
                print(f"✅ Pesan diekstrak: {message}")
            except Exception as e:
                print(f"❌ Error dalam ekstraksi pesan: {str(e)}")
        else:
            print(f"❌ File tidak valid: {args.input_file}")

    elif args.command == "quality":
        if validate_file(args.original_file) and validate_file(args.stego_file):
            try:
                metrics = analyzer.calculate_metrics(args.original_file, args.stego_file)
                print(f"MSE: {metrics['mse']:.2f}")
                print(f"PSNR: {metrics['psnr']:.2f} dB")
                print(f"SNR: {metrics['snr']:.2f} dB")
                print(f"Spectral Distortion: {metrics['spectral_distortion']:.2f}")
                print(f"THD: {metrics['thd']:.2f}%")
                report_file = analyzer.generate_quality_report(args.original_file, args.stego_file)
                print(f"Laporan disimpan di: {report_file}")
            except Exception as e:
                print(f"❌ Error dalam analisis kualitas: {str(e)}")
        else:
            print(f"❌ File tidak valid: {args.original_file} atau {args.stego_file}")

    elif args.command == "robustness":
        if validate_file(args.stego_file):
            try:
                audio_array, sample_rate = stego._load_audio(args.stego_file)
                results = stego.test_robustness(audio_array, sample_rate, args.password, args.original_message)
                for condition, result in results.items():
                    print(f"Kondisi: {condition}")
                    print(f"Status: {'Berhasil' if result['success'] else 'Gagal'}")
                    print(f"BER: {result['ber']:.2f}%")
                    print(f"Pesan: {result['message']}")
                    if result['error']:
                        print(f"Error: {result['error']}")
                    print("-" * 50)
            except Exception as e:
                print(f"❌ Error dalam pengujian ketahanan: {str(e)}")
        else:
            print(f"❌ File tidak valid: {args.stego_file}")

if __name__ == "__main__":
    main()
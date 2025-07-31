import numpy as np
import soundfile as sf
from pydub import AudioSegment
from src.enkripsi import Encryption
from src.utils import convert_to_wav
import os

class AudioSteganography:
    """Kelas untuk steganografi audio menggunakan metode LSB."""
    
    def __init__(self, delimiter: str = "11111111"):
        self.delimiter = ''.join(format(ord(c), '08b') for c in delimiter)
        self.encryption = Encryption()

    def _load_audio(self, file_path: str) -> tuple:
        """Memuat file audio dan mengembalikan array serta sample rate."""
        audio_array, sample_rate = sf.read(convert_to_wav(file_path))
        if len(audio_array.shape) > 1:
            audio_array = audio_array[:, 0]  # Ambil channel pertama jika stereo
        return audio_array, sample_rate

    def text_to_binary(self, text: str) -> bytes:
        """Mengonversi teks ke bytes."""
        return bytearray(text.encode('utf-8'))

    def binary_to_text(self, binary: bytes) -> str:
        """Mengonversi bytes ke teks."""
        return binary.decode('utf-8')

    def embed_lsb(self, audio_array: np.ndarray, message: str, password: str) -> np.ndarray:
        """Menyisipkan pesan terenkripsi ke audio menggunakan LSB."""
        try:
            # Enkripsi pesan
            encrypted_data = self.encryption.encrypt(message.encode('utf-8'), password)
            binary_data = ''.join(format(byte, '08b') for byte in encrypted_data) + self.delimiter
            
            if len(binary_data) > len(audio_array):
                raise ValueError("Pesan terlalu panjang untuk audio ini")
            
            # Salin array audio
            stego_audio = audio_array.copy()
            
            # Sisipkan bit menggunakan NumPy
            for i, bit in enumerate(binary_data):
                stego_audio[i] = (stego_audio[i] & ~1) | int(bit)
            
            return stego_audio
        except Exception as e:
            raise ValueError(f"Gagal menyisipkan pesan: {str(e)}")

    def extract_lsb(self, audio_array: np.ndarray, password: str) -> str:
        """Mengekstrak pesan dari audio menggunakan LSB."""
        try:
            # Ekstrak bit menggunakan NumPy
            binary_data = np.array(audio_array.flatten() & 1, dtype=np.uint8).tobytes().decode('latin1')
            
            # Cari delimiter
            delimiter_pos = binary_data.find(self.delimiter)
            if delimiter_pos == -1:
                raise ValueError("Delimiter tidak ditemukan dalam audio")
            
            # Ambil data sebelum delimiter
            binary_data = binary_data[:delimiter_pos]
            encrypted_data = int(binary_data, 2).to_bytes(len(binary_data) // 8, byteorder='big')
            
            # Dekripsi data
            decrypted_data = self.encryption.decrypt(encrypted_data, password)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Gagal mengekstrak pesan: {str(e)}")

    def _extract_from_array(self, audio_array: np.ndarray, password: str) -> str:
        """Mengekstrak pesan dari array audio (digunakan dalam pengujian)."""
        return self.extract_lsb(audio_array, password)

    def add_noise(self, audio_array: np.ndarray, noise_level: float) -> np.ndarray:
        """Menambahkan Gaussian noise ke audio."""
        noise = np.random.normal(0, noise_level, audio_array.shape)
        noisy_audio = audio_array + noise
        return np.clip(noisy_audio, -1.0, 1.0)

    def test_robustness(self, stego_audio: np.ndarray, sample_rate: int, password: str, 
                        original_message: str) -> dict:
        """Menguji ketahanan steganografi terhadap gangguan."""
        from pydub import AudioSegment
        import soundfile as sf
        results = {}

        # Fungsi untuk menghitung BER
        def calculate_ber(original: str, extracted: str) -> float:
            original_bits = ''.join(format(ord(c), '08b') for c in original)
            extracted_bits = ''.join(format(ord(c), '08b') for c in extracted[:len(original)])
            errors = sum(1 for a, b in zip(original_bits, extracted_bits) if a != b)
            return (errors / len(original_bits)) * 100 if original_bits else 0.0

        # Test asli
        try:
            message = self._extract_from_array(stego_audio, password)
            results['original'] = {
                'success': message == original_message,
                'message': message,
                'ber': calculate_ber(original_message, message),
                'error': ''
            }
        except Exception as e:
            results['original'] = {
                'success': False,
                'message': '',
                'ber': 100.0,
                'error': str(e)
            }

        # Test kompresi MP3
        for bitrate in ['128k', '320k']:
            temp_wav = 'temp/temp_stego.wav'
            temp_mp3 = f'temp/temp_stego_{bitrate}.mp3'
            sf.write(temp_wav, stego_audio, sample_rate)
            audio_segment = AudioSegment.from_wav(temp_wav)
            audio_segment.export(temp_mp3, format='mp3', bitrate=bitrate)
            compressed_audio, _ = sf.read(convert_to_wav(temp_mp3))
            try:
                message = self._extract_from_array(compressed_audio, password)
                results[f'compression_{bitrate}'] = {
                    'success': message == original_message,
                    'message': message,
                    'ber': calculate_ber(original_message, message),
                    'error': ''
                }
            except Exception as e:
                results[f'compression_{bitrate}'] = {
                    'success': False,
                    'message': '',
                    'ber': 100.0,
                    'error': str(e)
                }
            os.remove(temp_wav)
            os.remove(temp_mp3)

        # Test noise
        for noise_level, name in [(0.005, 'noise_low'), (0.01, 'noise_medium'), (0.02, 'noise_high')]:
            try:
                noisy_audio = self.add_noise(stego_audio, noise_level)
                message = self._extract_from_array(noisy_audio, password)
                results[name] = {
                    'success': message == original_message,
                    'message': message,
                    'ber': calculate_ber(original_message, message),
                    'error': ''
                }
            except Exception as e:
                results[name] = {
                    'success': False,
                    'message': '',
                    'ber': 100.0,
                    'error': str(e)
                }

        return results

    def embed_message(self, input_file: str, message: str, password: str, output_file: str, 
                        output_format: str = 'wav') -> dict:
        """Menyisipkan pesan ke file audio dan menyimpan hasil."""
        audio_array, sample_rate = self._load_audio(input_file)
        stego_audio = self.embed_lsb(audio_array, message, password)
        sf.write(output_file, stego_audio, sample_rate)
        if output_format != 'wav':
            audio_segment = AudioSegment.from_wav(output_file)
            audio_segment.export(output_file, format=output_format)
        return {'success': True, 'output_file': output_file}

    def extract_message(self, input_file: str, password: str) -> str:
        """Mengekstrak pesan dari file audio."""
        audio_array, _ = self._load_audio(input_file)
        return self.extract_lsb(audio_array, password)
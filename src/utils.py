import os
import soundfile as sf
from pydub import AudioSegment

def validate_file(file_path: str) -> bool:
    """Memvalidasi apakah file audio ada dan valid."""
    if not os.path.exists(file_path):
        return False
    try:
        sf.read(file_path)
        return True
    except:
        return False

def convert_to_wav(input_file: str) -> str:
    """Mengonversi file audio ke format WAV."""
    output_file = f"temp/{os.path.basename(input_file).split('.')[0]}_temp.wav"
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="wav")
    return output_file

def get_audio_info(file_path: str) -> dict:
    """Mengambil informasi audio."""
    try:
        audio, sample_rate = sf.read(file_path)
        duration = len(audio) / sample_rate
        channels = audio.shape[1] if len(audio.shape) > 1 else 1
        max_message_length = len(audio) // 8  # 1 byte = 8 bit
        return {
            "sample_rate": sample_rate,
            "channels": channels,
            "duration": duration,
            "max_message_length": max_message_length
        }
    except Exception as e:
        raise ValueError(f"Gagal membaca info audio: {str(e)}")
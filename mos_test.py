import pygame
import time

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

audio_files = ["sample1.mp3", "sample2.mp3", "sample3.mp3", "sample4.wav"]
for audio in audio_files:
    original = f"samples/{audio}"
    stego = f"output/{audio.split('.')[0]}_stego.{audio.split('.')[-1]}"
    print(f"Memutar asli: {original}")
    play_audio(original)
    input("Tekan Enter untuk memutar stego...")
    print(f"Memutar stego: {stego}")
    play_audio(stego)
    score = input("Masukkan skor MOS (1-5): ")
    print(f"Skor MOS untuk {audio}: {score}")
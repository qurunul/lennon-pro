import os
from main import main

audio_files = ["sample1.mp3", "sample2.mp3", "sample3.mp3", "sample4.wav"]
messages = [
    "Ini adalah pesan rahasia untuk pengujian steganografi audio dengan panjang 100 karakter, aman dan terenkripsi dengan AES-128.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
]
password = "password123"

for audio in audio_files:
    stego = f"output/{audio.split('.')[0]}_stego.{audio.split('.')[-1]}"
    for msg in messages:
        if os.path.exists(stego):
            print(f"Testing robustness: {stego}, Pesan: {msg[:20]}...")
            main(["robustness", stego, password, msg])
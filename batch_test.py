import os
from main import main

audio_files = ["samples/sample1.mp3", "samples/sample2.mp3", "samples/sample3.mp3", "samples/sample4.wav"]
messages = [
    "Ini adalah pesan rahasia untuk pengujian steganografi audio dengan panjang 100 karakter, aman dan terenkripsi dengan AES-128.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
]
password = "password123"

for audio in audio_files:
    for msg in messages:
        output_file = f"output/{os.path.basename(audio).split('.')[0]}_stego.{audio.split('.')[-1]}"
        print(f"Embedding: {audio}, Pesan: {msg[:20]}...")
        main(["embed", audio, msg, password, "--format", audio.split('.')[-1]])
        print(f"Extracting: {output_file}")
        main(["extract", output_file, password])
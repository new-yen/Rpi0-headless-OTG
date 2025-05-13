import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess
import time
import os

# --- Configuration ---
AUDIO_DIR = "/home/pi/audio/"
# RFID_TO_MP3 = {  #  Not needed anymore
#     "488504499188": "ape.mp3",
#     "YOUR_UID_2_HERE": "another_song.mp3",
# }

# --- Setup ---
GPIO.setwarnings(False)
reader = SimpleMFRC522()
current_playing = None
vlc_process = None

def play_audio(filepath):
    """Plays the audio file specified by the filepath."""
    global current_playing, vlc_process
    if os.path.exists(filepath):
        print(f"Playing: {filepath}")
        # Kill any existing VLC process before starting a new one
        if vlc_process:
            vlc_process.terminate()
            vlc_process.wait()
        vlc_process = subprocess.Popen(["cvlc", "--play-and-exit", filepath],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        current_playing = filepath
    else:
        print(f"Error: Audio file not found: {filepath}")
        current_playing = None
        if vlc_process:
            vlc_process.terminate()
            vlc_process.wait()
        vlc_process = None

def main():
    global current_playing, vlc_process
    print("Ready to read RFID tags...")
    try:
        GPIO.setmode(GPIO.BOARD) # Initialize GPIO
        while True:
            print("Scanning for tag...")
            id, text = reader.read()  # Read RFID data

            if id is not None:
                print(f"UID: {id}")
                print(f"Text: {text}")
                if text:  # Check if text is not empty
                    audio_file = text.strip() + ".mp3"  # Use the text as filename
                    audio_path = os.path.join(AUDIO_DIR, audio_file)
                    play_audio(audio_path)
                else:
                    print("No text found on the RFID tag.")
            else:
                print("No tag detected.")

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting.")
    finally:  # Ensure cleanup happens even after normal execution
        GPIO.cleanup()
        if vlc_process:
            vlc_process.terminate()
            vlc_process.wait()

if __name__ == "__main__":
    main()

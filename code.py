import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess
import time
import os

# --- Configuration ---
AUDIO_DIR = "/home/pi/audio/"
RFID_TO_MP3 = {
    "488504499188": "ape.mp3",
    "486519217122": "slow.mp3",  # Add more mappings here
    # "ANOTHER_UID": "another_song.wav", # You can use other formats
}

# --- Setup ---
GPIO.setwarnings(False)
reader = SimpleMFRC522()
current_playing = None
vlc_process = None
last_card_id = None
NO_CARD_TIMEOUT = 5  # seconds

def play_audio(filename):
    """Plays the audio file specified by the filename."""
    global current_playing, vlc_process
    filepath = os.path.join(AUDIO_DIR, filename)
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
    global current_playing, vlc_process, last_card_id
    print("Ready to read RFID tags...")
    try:
        GPIO.setmode(GPIO.BOARD)  # Initialize GPIO
        last_card_time = time.time()  # Initialize with current time

        while True:
            print("Scanning for tag...")
            id, text = reader.read_no_block()  # Use non-blocking read

            if id is not None:
                print(f"UID: {id}")
                print(f"Text: {text}")
                last_card_time = time.time()  # Update last_card_time
                if id != last_card_id:  # Check if it's a new card
                    last_card_id = id  # Update the last read card ID
                    uid_str = str(id)
                    if uid_str in RFID_TO_MP3:
                        audio_file = RFID_TO_MP3[uid_str]
                        play_audio(audio_file)
                    else:
                        print(f"No audio file associated with UID: {id}")
                else:
                    print("Same card detected, not playing again.")
            else:
                # No card detected
                if time.time() - last_card_time > NO_CARD_TIMEOUT:
                    print("No card detected for too long. Resetting.")
                    last_card_id = None  # Reset last_card_id
                    last_card_time = time.time() # Reset timer
            time.sleep(0.1)  # Short delay to prevent excessive CPU usage

    except KeyboardInterrupt:
        print("\nExiting.")
    finally:  # Ensure cleanup happens even after normal execution
        GPIO.cleanup()
        if vlc_process:
            vlc_process.terminate()
            vlc_process.wait()

if __name__ == "__main__":
    main()

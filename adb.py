import subprocess
import os
import time

# --- Configuration ---
LDPLAYER_ADB_PATH = "F:\\LDPlayer\\LDPlayer9\\adb.exe" 
SCREENSHOT_OUTPUT_DIR = "D:\\kelp\\images"

# --- Functions ---
def connect_to_emulator():
    subprocess.call([LDPLAYER_ADB_PATH, "connect", "127.0.0.1:5555"])  # Standard LDPlayer connection

def take_screenshot():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    output_path = os.path.join(SCREENSHOT_OUTPUT_DIR, filename)

    # Capture screen
    subprocess.call([LDPLAYER_ADB_PATH, "-s", "emulator-5554", "shell", "screencap", "-p", "/sdcard/screenshot.png"])

    # Pull screenshot - modify the output path
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    output_path = os.path.join(SCREENSHOT_OUTPUT_DIR, filename)   
    subprocess.call([LDPLAYER_ADB_PATH, "-s", "emulator-5554", "pull", "/sdcard/screenshot.png", output_path])

    # Optional: Delete screenshot from emulator
    subprocess.call([LDPLAYER_ADB_PATH, "shell", "rm", "/sdcard/screenshot.png"])

# --- Main Script ---
if __name__ == "__main__":
    connect_to_emulator()
    take_screenshot()

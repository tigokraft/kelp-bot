import subprocess
import os
import time
import cv2  
from PIL import Image

# --- Configuration ---
LDPLAYER_ADB_PATH = "F:\\LDPlayer\\LDPlayer9\\adb.exe"  
SCREENSHOT_OUTPUT_DIR = "D:\\kelp"  
REFERENCE_IMAGE_PATH = "D:\\kelp\\images\\setupW.png"  

# --- Functions ---
def connect_to_emulator():
    subprocess.call([LDPLAYER_ADB_PATH, "connect", "127.0.0.1:5555"]) 

def take_screenshot():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    output_path = os.path.join(SCREENSHOT_OUTPUT_DIR, filename)
    subprocess.call([LDPLAYER_ADB_PATH, "-s", "emulator-5554", "shell", "screencap", "-p", "/sdcard/screenshot.png"])
    subprocess.call([LDPLAYER_ADB_PATH, "-s", "emulator-5554", "pull", "/sdcard/screenshot.png", output_path]) 
    return filename 

def click_on_screen(x, y):
    subprocess.call([LDPLAYER_ADB_PATH, "-s", "emulator-5554", "shell", "input", "tap", str(x), str(y)])

def compare_screenshot(screenshot_path, reference_image_path):
    img1 = Image.open(screenshot_path)
    img2 = Image.open(reference_image_path)
    return img1 == img2  

def find_image_and_click(reference_image_path):
    screenshot_path = "screenshot.png"  
    take_screenshot()

    # Load images
    screenshot = cv2.imread(screenshot_path)
    reference_image = cv2.imread(reference_image_path)

    # Template Matching
    result = cv2.matchTemplate(screenshot, reference_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Get center of the match
    top_left = max_loc
    w, h = reference_image.shape[:-1]  
    center_x = top_left[0] + w // 2
    center_y = top_left[1] + h // 2

    # Perform the click
    click_on_screen(center_x, center_y)

# --- Main Script ---
if __name__ == "__main__":
    connect_to_emulator()
    find_image_and_click(REFERENCE_IMAGE_PATH) 

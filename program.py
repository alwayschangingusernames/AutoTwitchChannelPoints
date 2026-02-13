import sys, os, subprocess
def install_requirements():
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_file):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
install_requirements()

import time
from typing import Tuple, Dict
from PIL import Image
import mss
from PIL import Image
import pyautogui


BUTTON_COLOR = (0, 219, 132)
COLOR_TOLERANCE = 5
PRIMARY_MONITOR_BUTTONS: Dict[str, Dict[str, int]] = {
    "fullscreen": {"x": 1700, "y": 1050},
    "theater_mode": {"x": 1700, "y": 1000},
}
SECONDARY_MONITOR_BUTTONS: Dict[str, Dict[str, int]] = {
    "fullscreen": {"x": 1700, "y": 1050},
    "theater_mode": {"x": 1700, "y": 1000},
}

def move_mouse_to_secondary_center() -> None:
    try:
        with mss.mss() as sct:
            if len(sct.monitors) < 3:
                return
            secondary = sct.monitors[2]
            center_x = secondary["left"] + (secondary["width"] // 2)
            center_y = secondary["top"] + (secondary["height"] // 2)
            pyautogui.moveTo(center_x, center_y)
    except Exception as e:
        print(f"Error moving mouse to secondary center: {e}")
def color_matches(pixel_color: Tuple[int, int, int], target_color: Tuple[int, int, int], tolerance: int) -> bool:
    return all(abs(pixel_color[i] - target_color[i]) <= tolerance for i in range(3))
def check_pixel_on_monitor(monitor_num: int, x: int, y: int, expected_color: Tuple[int, int, int]) -> bool:
    try:
        with mss.mss() as sct:
            region = {
                "left": x,
                "top": y,
                "width": 1,
                "height": 1
            }
            
            screenshot = sct.grab(region)
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            pixel_color = img.getpixel((0, 0))
            
            return color_matches(pixel_color, expected_color, COLOR_TOLERANCE)
    
    except Exception as e:
        print(f"Error checking pixel: {e}")
        return False
def check_buttons_on_monitor(monitor_num: int, buttons: Dict[str, Dict[str, int]], monitor_name: str) -> bool:
    found = False
    
    for button_name, coords in buttons.items():
        if check_pixel_on_monitor(monitor_num, coords["x"], coords["y"], BUTTON_COLOR):
            pyautogui.click(coords["x"], coords["y"])
            move_mouse_to_secondary_center()
            found = True
    
    return found

class PixelCheckerCLI:
    def __init__(self):
        self.running = True   
    def clear_terminal(self):
        os.system("cls" if os.name == "nt" else "clear")
    def show_menu(self):
        self.clear_terminal()
        print("\n" + "="*50)
        print("Multi-Monitor Pixel Checker")
        print("="*50)
        print("1. Check Pixels")
        print("2. Calibrate (Get Pixel Color)")
        print("3. Debug Check (Test Button Coordinates)")
        print("4. Exit")
        print("="*50)    
    def check_pixels(self):
        minutes_since_last_click = 0
        total_clicks = 0

        try:
            while True:
                found_primary = check_buttons_on_monitor(1, PRIMARY_MONITOR_BUTTONS, "Primary Monitor")
                found_secondary = check_buttons_on_monitor(2, SECONDARY_MONITOR_BUTTONS, "Secondary Monitor")

                if found_primary or found_secondary:
                    total_clicks += 1
                    minutes_since_last_click = 0
                else:
                    minutes_since_last_click += 1

                self.clear_terminal()
                print("\n" + "="*50)
                print("AutoTwitchChannelPoints")
                print("="*50)
                print(f"Minutes since Last Click: {minutes_since_last_click} | Times Button has been Clicked: {total_clicks}")
                print("Press Ctrl+C to stop.")

                time.sleep(60)

        except KeyboardInterrupt:
            print("\n\nPixel check stopped by user.")   
    def calibrate(self):
        print("\n" + "="*50)
        print("Calibration Mode - Get Pixel Color")
        print("="*50)
        
        try:
            x = int(input("Enter X coordinate: "))
            y = int(input("Enter Y coordinate: "))
            
            with mss.mss() as sct:
                region = {"left": x, "top": y, "width": 1, "height": 1}
                screenshot = sct.grab(region)
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                pixel_color = img.getpixel((0, 0))
                
                print(f"\nPixel at ({x}, {y}): RGB{pixel_color}")
                print(f"Hex: #{pixel_color[0]:02x}{pixel_color[1]:02x}{pixel_color[2]:02x}")
        
        except ValueError:
            print("Invalid input. Please enter numbers only.")
        except Exception as e:
            print(f"Error: {e}")
    def debug_check(self):
        print("\n" + "="*50)
        print("Debug Check - Test Button Coordinates")
        print("="*50)
        
        try:
            x = int(input("Enter X coordinate: "))
            y = int(input("Enter Y coordinate: "))
            
            with mss.mss() as sct:
                region = {"left": x, "top": y, "width": 1, "height": 1}
                screenshot = sct.grab(region)
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                pixel_color = img.getpixel((0, 0))
                
                print(f"\nActual pixel color at ({x}, {y}): RGB{pixel_color}")
                print(f"Target color: RGB{BUTTON_COLOR}")
                print(f"Tolerance: ±{COLOR_TOLERANCE}")
                
                if color_matches(pixel_color, BUTTON_COLOR, COLOR_TOLERANCE):
                    print("✓ Color MATCHES target within tolerance!")
                else:
                    print("✗ Color does NOT match target")
                    diff_r = abs(pixel_color[0] - BUTTON_COLOR[0])
                    diff_g = abs(pixel_color[1] - BUTTON_COLOR[1])
                    diff_b = abs(pixel_color[2] - BUTTON_COLOR[2])
                    print(f"  Difference: R={diff_r}, G={diff_g}, B={diff_b}")
        
        except ValueError:
            print("Invalid input. Please enter numbers only.")
        except Exception as e:
            print(f"Error: {e}")    
    def run(self):
        while self.running:
            self.show_menu()
            choice = input("Select an option (1-4): ").strip()
            
            if choice == "1":
                self.check_pixels()
            elif choice == "2":
                self.calibrate()
            elif choice == "3":
                self.debug_check()
            elif choice == "4":
                print("Exiting...")
                self.running = False
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    cli = PixelCheckerCLI()
    cli.run()

    

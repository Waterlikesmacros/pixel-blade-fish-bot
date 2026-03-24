"""
Pixel Blade Fishing Bot - Core Detection Logic
Handles all computer vision and fishing automation
"""

import cv2
import numpy as np
import pyautogui
import time
import mss
from typing import Tuple, Optional, List
import logging

logger = logging.getLogger(__name__)

class PixelBladeFishingBot:
    def __init__(self):
        # Default settings
        self.fishing_key = 'e'
        self.fishing_key_modifiers = []
        self.check_interval = 0.1
        self.circle_detection_threshold = 0.3
        self.radius_ranges = [(10, 40), (30, 80), (60, 150), (100, 250)]
        self.green_hsv_min = np.array([40, 40, 40])
        self.green_hsv_max = np.array([80, 255, 255])
        self.min_green_area = 200
        self.green_circularity_threshold = 0.3
        
        # Screen capture setup
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]
        
        # Safety settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """Capture screen region or full screen"""
        if region:
            monitor = {"top": region[1], "left": region[0], "width": region[2], "height": region[3]}
        else:
            monitor = self.monitor
        
        screenshot = self.sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    
    def detect_fishing_ui(self, image: np.ndarray) -> bool:
        """Enhanced detection for Pixel Blade fishing circles"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Method 1: Enhanced light blue outer circle detection
        blue_ranges = [
            ([80, 80, 180], [120, 255, 255]),
            ([90, 100, 200], [110, 255, 255]),
            ([70, 60, 160], [100, 240, 240])
        ]
        
        for lower_blue, upper_blue in blue_ranges:
            lower = np.array(lower_blue)
            upper = np.array(upper_blue)
            blue_mask = cv2.inRange(hsv, lower, upper)
            
            blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in blue_contours:
                area = cv2.contourArea(contour)
                if area > 300:
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        if circularity > 0.3:
                            return True
        
        # Method 2: Look for "10x" text (final circle at full strength)
        if self.detect_10x_text(image):
            return True
        
        return False
    
    def detect_circle_overlap(self, image: np.ndarray) -> bool:
        """Detect when inner circle touches outer circle OR when inner circle turns green"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Method 1: Check for green color indication
        lower_green = self.green_hsv_min
        upper_green = self.green_hsv_max
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        
        contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_green_area:
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    if circularity > self.green_circularity_threshold:
                        return True
        
        return False
    
    def detect_loot(self, image: np.ndarray) -> tuple:
        """Detect loot text and return (found, rarity, position)"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        loot_colors = {
            'Vaulted(Red)': ([0, 150, 100], [10, 255, 255]),
            'Legendary(Yellow)': ([20, 150, 100], [30, 255, 255]), 
            'Rare(Blue)': ([100, 150, 100], [130, 255, 255]),
            'Epic(Purple)': ([130, 150, 100], [170, 255, 255]),
            'Common(Grey)': ([0, 0, 150], [180, 30, 255])
        }
        
        for rarity_name, (lower, upper) in loot_colors.items():
            lower = np.array(lower)
            upper = np.array(upper)
            mask = cv2.inRange(hsv, lower, upper)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 200:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    if 0.5 < aspect_ratio < 5:
                        return True, rarity_name, (x, y, w, h)
        
        return False, None, None
    
    def detect_10x_text(self, image: np.ndarray) -> bool:
        """Detect '10x' text pattern (final circle at full strength)"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive threshold for better text detection
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # Look for text patterns
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if 20 < w < 100 and 20 < h < 100:  # Reasonable text size for "10x"
                # Extract region and check for '10x' pattern
                roi = binary[y:y+h, x:x+w]
                if self.detect_10x_pattern(roi):
                    return True
        
        return False
    
    def detect_10x_pattern(self, roi: np.ndarray) -> bool:
        """Detect '10x' character pattern in ROI"""
        h, w = roi.shape
        if h < 15 or w < 30:  # Minimum size for "10x"
            return False
        
        # Check for '1', '0', and 'x' characters
        # Split ROI into 3 parts for '1', '0', 'x'
        third_w = w // 3
        
        # '1' should have vertical lines
        part1 = roi[:, :third_w]
        has_vertical = np.sum(part1) > 100
        
        # '0' should have circular shape (hollow center)
        part2 = roi[:, third_w:2*third_w]
        has_circular = np.sum(part2) > 100
        
        # 'x' should have diagonal lines
        part3 = roi[:, 2*third_w:]
        has_diagonal = np.trace(part3) > 30 and np.trace(np.fliplr(part3)) > 30
        
        return has_vertical and has_circular and has_diagonal
    
    def press_fishing_key(self):
        """Press the fishing key with modifiers"""
        try:
            modifiers = []
            if self.fishing_key_modifiers:
                for modifier_group in self.fishing_key_modifiers:
                    modifiers.extend(modifier_group.split('+'))
            
            for modifier in modifiers:
                modifier = modifier.lower()
                if modifier == 'alt':
                    pyautogui.keyDown('alt')
                elif modifier == 'shift':
                    pyautogui.keyDown('shift')
                elif modifier == 'ctrl':
                    pyautogui.keyDown('ctrl')
            
            pyautogui.press(self.fishing_key)
            
            for modifier in reversed(modifiers):
                modifier = modifier.lower()
                if modifier == 'alt':
                    pyautogui.keyUp('alt')
                elif modifier == 'shift':
                    pyautogui.keyUp('shift')
                elif modifier == 'ctrl':
                    pyautogui.keyUp('ctrl')
            
        except Exception as e:
            logger.error(f"Error pressing fishing key: {e}")
        
        time.sleep(0.2)
    
    def anti_stuck_check(self, timeout=5.0):
        """Anti-stuck mechanism - spam E if no fishing UI found"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            image = self.capture_screen()
            if self.detect_fishing_ui(image):
                return True
            
            time.sleep(0.5)
        
        logger.info("Anti-stuck activated: No fishing UI detected, spamming E key")
        for _ in range(10):
            self.press_fishing_key()
            time.sleep(0.1)
        
        return False
    
    def wait_for_circle_overlap(self, timeout: float = 10.0) -> bool:
        """Wait for inner circle to touch outer circle"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            image = self.capture_screen()
            if self.detect_circle_overlap(image):
                return True
            time.sleep(self.check_interval)
        return False
    
    def spam_until_ui_gone(self, max_spams=20):
        """Spam E key until fishing UI disappears (for 10x situations)"""
        spams = 0
        while spams < max_spams:
            # Check if UI is still visible
            image = self.capture_screen()
            if not self.detect_fishing_ui(image):
                logger.info(f"Fishing UI disappeared after {spams} E presses")
                break
            
            # Press E
            self.press_fishing_key()
            spams += 1
            time.sleep(0.1)  # Quick spam
        
        if spams >= max_spams:
            logger.warning(f"UI still visible after {max_spams} E presses - stopping spam")
        
        # Extra spam to make sure UI is completely gone
        self.spam_fishing_key()
    
    def spam_fishing_key(self, duration: float = 2.0):
        """Spam fishing key to clear remaining UI"""
        end_time = time.time() + duration
        while time.time() < end_time:
            self.press_fishing_key()
            time.sleep(0.1)

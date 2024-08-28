from typing import Tuple, List
import cv2
import numpy as np
import pyautogui
import sys


def find_button_coordinates(
        template_path: str,
        step: int = 25,
        match_threshold: float = 0.6,
        show_img_flag: bool = True,
) -> Tuple[int, int]:
    pyautogui.dragTo(0, 0)
    screenshot = get_screenshot()
    template = get_grayscale_template_image(template_path)
    template_h, template_w = template.shape[:2]
    regions = get_sliced_regions(screenshot, (template_w, template_h), step)
    highest_match = -100
    best_region = None
    center_x, center_y = (None, None)
    for (x1, y1), (x2, y2) in regions:
        sub_region = screenshot[y1:y2, x1:x2]
        match_percentage = get_match_percentage(sub_region, template)
        if match_percentage > highest_match and match_percentage > match_threshold:
            highest_match = match_percentage
            best_region = (x1, y1, x2, y2)
            center_x = x1 + ((x2 - x1) // 2)
            center_y = y1 + ((y2 - y1) // 2)
            print(
                'highest_match:', highest_match,
                'center_x:', center_x,
                'center_y:', center_y,
            )
    if best_region == None or highest_match < match_threshold:
        raise Exception("Button not found in any region")
    if show_img_flag is True:
        x1, y1, x2, y2 = best_region
        cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(screenshot, (center_x, center_y), 5, (0, 0, 255), -1)
        cv2.imshow("Match Result", screenshot)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    scale_factor = 1
    if sys.platform == "darwin":
        scale_factor = 2
    return (center_x // scale_factor, center_y // scale_factor)


def get_sliced_regions(
    image: np.ndarray,
    template_size: Tuple[int, int],
    step: int = 25
) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    h, w = image.shape[:2]
    regions = []
    for y in range(0, h - template_size[1] + 1, step):
        for x in range(0, w - template_size[0] + 1, step):
            x1, y1 = x, y
            x2, y2 = x + template_size[0], y + template_size[1]
            regions.append(((x1, y1), (x2, y2)))
    return regions


def get_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    return cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)


def get_grayscale_template_image(template_path: str) -> np.ndarray:
    template = cv2.imread(template_path, 0)
    if template is None:
        raise FileNotFoundError(f"Template image not found at {template_path}")
    return template


def get_match_percentage(
    region: np.ndarray,
    template: np.ndarray
) -> float:
    result = cv2.matchTemplate(region, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    return max_val

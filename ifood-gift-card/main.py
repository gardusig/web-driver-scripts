from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from util.chromium import create_driver
import csv
import logging
import pyautogui
import pyperclip
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

SHEET_DATA_PATH = '/Users/gardusig/code/web-driver-scripts/ifood-gift-card/resources/sheet_data.csv'


def load_sheet_data(csv_path: str):
    sheet_data = []
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                row = row[0].split('\t')
                if len(row) < 2:
                    print(row)
                    logging.warning(f"Skipping invalid row in {
                                    csv_path}: {row}")
                    continue
                sheet_data.append({
                    "link": row[0],
                    "password": row[1],
                    "code": None
                })
        logging.info(f"Successfully loaded sheet data from {csv_path}.")
    except Exception as e:
        logging.error(f"Failed to load sheet data from {csv_path}: {e}")
    return sheet_data


def fill_gift_card_password(driver, sheet_data):
    input_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "body > flutter-view > flt-text-editing-host > input")
        )
    )
    if not input_element:
        raise Exception(f"Failed to find password input for link: {
                        sheet_data['link']}")
    input_element.send_keys(sheet_data["password"])


def find_button(img_path: str, retina_scale_factor: float = 2.0):
    button_location = pyautogui.locateOnScreen(img_path)
    if button_location is None:
        logging.warning(f'Button not found: {img_path}')
        return None
    button_center = pyautogui.center(button_location)
    adjusted_x = button_center[0] / retina_scale_factor
    adjusted_y = button_center[1] / retina_scale_factor
    logging.info(f'Adjusted coordinates: {(adjusted_x, adjusted_y)}')
    return (adjusted_x, adjusted_y)


def open_gift_card(img_path: str = '/Users/gardusig/code/web-driver-scripts/ifood-gift-card/resources/open-gift-card-button.png'):
    button_coordinates = find_button(img_path)
    if button_coordinates:
        pyautogui.click(button_coordinates)
    else:
        logging.error('Failed to find the open gift card button.')


def get_gift_card_code(driver, img_path: str = '/Users/gardusig/code/web-driver-scripts/ifood-gift-card/resources/copy-gift-card-button.png'):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "iframe[src='https://www.youtube.com/embed/Tkc0M8vwDTU']")
            )
        )
        logging.info('YouTube iframe loaded successfully.')
    except Exception as e:
        raise Exception(f"Failed to load YouTube iframe: {e}")
    time.sleep(1)
    button_coordinates = find_button(img_path)
    if button_coordinates:
        pyautogui.click(button_coordinates)
        time.sleep(1)
        return pyperclip.paste()
    else:
        logging.error('Failed to find the copy gift card button.')
        return None


def handle_gift_card(driver, sheet_data):
    logging.info(f'Starting process for gift card: {sheet_data["link"]}')
    driver.get(sheet_data["link"])
    fill_gift_card_password(driver, sheet_data)
    open_gift_card()
    return get_gift_card_code(driver)


def main():
    sheet_data_list = load_sheet_data(SHEET_DATA_PATH)
    if not sheet_data_list:
        logging.error('No sheet data found, exiting.')
        return
    driver = create_driver()
    try:
        for sheet_data in sheet_data_list:
            try:
                sheet_data['code'] = handle_gift_card(driver, sheet_data)
                logging.info(f"Finished processing gift card for {
                             sheet_data['link']}")
            except Exception as e:
                logging.error(f"Error handling gift card for link: {
                              sheet_data['link']}, reason: {e}")
    finally:
        driver.quit()
    for sheet_data in sheet_data_list:
        print(sheet_data['code'])


if __name__ == "__main__":
    main()

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from util.chromium import create_driver
from util.find_button import find_button_coordinates
import pyautogui
import pyperclip
import time

sheet_data_list = [
    {
        "link": "https://loja.smash.gifts/resgatar/0LLluqMIZcLdZwwUoZ6U",
        "password": "588285",
    },
    {
        "link": "https://loja.smash.gifts/resgatar/0ayzLvwmuhdHhsmbiADz",
        "password": "792534",
    },
]


def fill_gift_card_password(driver, sheet_data):
    input_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "body > flutter-view > flt-text-editing-host > input")
        )
    )
    if not input_element:
        raise Exception(
            f"Failed to find password input for link: {sheet_data['link']}")
    input_element.send_keys(sheet_data["password"])


def open_gift_card(
        img_path: str = '/Users/gardusig/code/hybrid-web-scripts/web-driver/resources/open-gift-card-button.png',
):
    button_coordinates = find_button_coordinates(img_path)
    print('found open_gift_card button_coordinates:', button_coordinates)
    pyautogui.click(button_coordinates)


def get_gift_card_code(
        driver,
        img_path: str = '/Users/gardusig/code/hybrid-web-scripts/web-driver/resources/copy-gift-card-button.png',
):
    flutter_view = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "body > flutter-view")
        )
    )
    if not flutter_view:
        raise Exception(f"Failed to load flutter view")
    button_coordinates = find_button_coordinates(
        template_path=img_path,
    )
    print('found copy_gift_card button_coordinates:', button_coordinates)
    pyautogui.click(button_coordinates)
    time.sleep(1)
    return pyperclip.paste()


def handle_gift_card(driver, sheet_data):
    print('starting process for gift card:', sheet_data['link'])
    driver.get(sheet_data["link"])
    fill_gift_card_password(driver, sheet_data)
    open_gift_card()
    return get_gift_card_code(driver)


def main():
    driver = create_driver()
    for sheet_data in sheet_data_list:
        try:
            code = handle_gift_card(driver, sheet_data)
            print(
                f"Finished processing gift card for {sheet_data['link']}, code: {code}")
        except Exception as e:
            error_message = f"Error handling gift card for link: {
                sheet_data['link']}, reason:"
            print(error_message, e)
    driver.quit()


if __name__ == "__main__":
    main()

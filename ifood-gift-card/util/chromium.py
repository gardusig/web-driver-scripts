from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_driver_path = "/Users/gardusig/tool/chromedriver"
chromium_path = "/Users/gardusig/tool/chrome/mac_arm-113.0.5672.63/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"


def create_driver():
    options = Options()
    options.binary_location = chromium_path
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

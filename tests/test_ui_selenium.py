import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(service=service)

    chrome_driver.implicitly_wait(5)
    chrome_driver.maximize_window()

    yield chrome_driver

    chrome_driver.quit()


def test_add_product_ui(driver):

    driver.get("http://127.0.0.1:5000")

    name_input = driver.find_element(By.ID, "name")
    price_input = driver.find_element(By.ID, "price")
    image_input = driver.find_element(By.ID, "image")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    name_input.clear()
    name_input.send_keys("נעלי ספורט")

    price_input.clear()
    price_input.send_keys("250")

    image_input.clear()
    image_input.send_keys("http://example.com/shoes.jpg")

    submit_button.click()

    time.sleep(2)

    page_source = driver.page_source
    assert "נעלי ספורט" in page_source
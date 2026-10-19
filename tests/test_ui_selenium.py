import time
import random
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    chrome_driver = webdriver.Chrome()

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

    unique_name = f"נעלי ספורט_{random.randint(1000, 9999)}"

    name_input.clear()
    name_input.send_keys(unique_name)

    price_input.clear()
    price_input.send_keys("250")

    image_input.clear()
    image_input.send_keys("http://example.com/shoes.jpg")

    submit_button.click()

    time.sleep(2)



    page_source = driver.page_source
    assert unique_name in page_source


def test_add_product_empty_form_fails(driver):
    driver.get("http://127.0.0.1:5000")

    rows_before = len(driver.find_elements(By.CSS_SELECTOR, "#product-table tr"))

    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()

    time.sleep(1)


    rows_after = len(driver.find_elements(By.CSS_SELECTOR, "#product-table tr"))

    assert rows_before == rows_after


def test_add_product_negative_price_fails(driver):
    driver.get("http://127.0.0.1:5000")

    name_input = driver.find_element(By.ID, "name")
    price_input = driver.find_element(By.ID, "price")
    image_input = driver.find_element(By.ID, "image")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    unique_name = f"מוצר בדיקה_{random.randint(1000, 9999)}"

    name_input.send_keys(unique_name)
    price_input.send_keys("-100")
    image_input.send_keys("http://example.com/shoes.jpg")
    submit_button.click()

    time.sleep(1)


    alert = driver.switch_to.alert
    alert.accept()

    assert unique_name not in driver.page_source


def test_add_product_name_too_short_ui(driver):
    driver.get("http://127.0.0.1:5000")

    name_input = driver.find_element(By.ID, "name")
    price_input = driver.find_element(By.ID, "price")
    image_input = driver.find_element(By.ID, "image")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    name_input.send_keys("א")
    price_input.send_keys("50")
    image_input.send_keys("http://example.com/shoes.jpg")
    submit_button.click()

    time.sleep(1)


    alert = driver.switch_to.alert
    alert.accept()

    assert "א" not in driver.page_source


def test_product_fields_are_required(driver):
    driver.get("http://127.0.0.1:5000")

    name_input = driver.find_element(By.ID, "name")

    name_input.get_attribute("required")
    is_valid_form = driver.execute_script("return document.getElementById('name').checkValidity();")

    assert is_valid_form is False
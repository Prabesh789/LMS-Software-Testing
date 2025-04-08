import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path fix for credentials
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from creds.credentials import OPENLIBRARY_USERNAME, OPENLIBRARY_PASSWORD

# Setup
driver = webdriver.Chrome()
driver.get("https://openlibrary.org/account/login")
driver.maximize_window()

try:
    # Login
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(OPENLIBRARY_USERNAME)
    driver.find_element(By.ID, "password").send_keys(OPENLIBRARY_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[name='login']").click()

    # Wait for login confirmation
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "prabesh78")))

    # Search for the book
    search_box = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search']"))
    )
    search_box.clear()
    search_box.send_keys("Rich Dad Poor Dad")
    search_box.send_keys(Keys.RETURN)

    # Wait for the result page and click the first book link
    book_link = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='/works/']"))
    )
    book_link.click()

    # Wait for the Borrow button
    borrow_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'cta-dropper')]/a"))
    )
    borrow_button.click()

    # Wait to confirm borrow (e.g., button changes or reader opens)
    time.sleep(5)  # give it a few seconds to transition

    print("✅ Borrow Book test - PASSED")

except Exception as e:
    print("❌ Borrow Book test - FAILED")
    print(f"Error: {e}")
    driver.save_screenshot("borrow_failed.png")

finally:
    driver.quit()

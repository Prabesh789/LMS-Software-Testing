from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys

# Add creds directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from creds.credentials import OPENLIBRARY_USERNAME, OPENLIBRARY_PASSWORD

# Setup
driver = webdriver.Chrome()
driver.get("https://openlibrary.org/account/login")
driver.maximize_window()

try:
    # Log in
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(OPENLIBRARY_USERNAME)
    driver.find_element(By.ID, "password").send_keys(OPENLIBRARY_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[name='login']").click()

    # Wait until login successful
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "My Books")))

    # Navigate to borrowed book
    driver.get("https://openlibrary.org/works/OL2010879W")  # Adjust this if needed

    # Click 'Return book' button
    return_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Return book')]"))
    )
    return_button.click()

    # Wait for the reader to load with 'Return now' button
    return_now = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Return now')]"))
    )
    return_now.click()

    print("✅ Return Book test - PASSED")

except Exception as e:
    print("❌ Return Book test - FAILED")
    print(f"Error: {e}")
    driver.save_screenshot("return_failed_debug.png")

finally:
    time.sleep(3)
    driver.quit()

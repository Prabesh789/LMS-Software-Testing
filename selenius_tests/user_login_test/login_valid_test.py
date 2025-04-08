import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add project root to path for credentials import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from creds.credentials import OPENLIBRARY_USERNAME, OPENLIBRARY_PASSWORD

# Setup
driver = webdriver.Chrome()  # Ensure chromedriver is in PATH
driver.get("https://openlibrary.org/account/login")
driver.maximize_window()

try:
    # Wait for username field to load and input credentials
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(OPENLIBRARY_USERNAME)
    driver.find_element(By.ID, "password").send_keys(OPENLIBRARY_PASSWORD)

    # Wait for and click the login button
    login_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='login']"))
    )
    login_button.click()

    # Wait for successful login indicator — you may need to change this
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.LINK_TEXT, "prabesh78"))
    )
    print("Login with valid credentials - PASSED")

except Exception as e:
    print("Login with valid credentials - FAILED")
    print(f"Error: {e}")
    driver.save_screenshot("login_failed.png")  # Optional: for debugging

finally:
    driver.quit()

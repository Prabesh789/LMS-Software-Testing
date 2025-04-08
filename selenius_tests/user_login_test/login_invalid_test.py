import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from creds.credentials import OPENLIBRARY_USERNAME

# Using correct username but wrong password for invalid login
INVALID_PASSWORD = "wrongpassword123"

# Setup
driver = webdriver.Chrome()
driver.get("https://openlibrary.org/account/login")
driver.maximize_window()

try:
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(OPENLIBRARY_USERNAME)
    driver.find_element(By.ID, "password").send_keys(INVALID_PASSWORD)

    login_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='login']"))
    )
    login_button.click()

    # Wait for error message
    error_msg = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "flash-error"))
    )

    print("Login with invalid credentials - PASSED")

except Exception as e:
    print("Login with invalid credentials - FAILED")
    print(f"Error: {e}")
    driver.save_screenshot("invalid_login_failed.png")

finally:
    time.sleep(2)
    driver.quit()

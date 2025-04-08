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

    # Search for an invalid book title
    search_box = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search']"))
    )
    search_box.clear()
    search_box.send_keys("xyzabc123")
    search_box.send_keys(Keys.RETURN)  # Hit Enter key

    # Wait for 'No results' message to appear
    message = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'No books directly matched your search')]"))
    )

    if message:
        print("Invalid book title search - PASSED")
    else:
        print("Invalid book title search - FAILED")

except Exception as e:
    print("Invalid book title search - FAILED")
    print(f"Error: {e}")
    driver.save_screenshot("search_invalid_failed.png")

finally:
    time.sleep(2)
    driver.quit()

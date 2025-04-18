import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add credentials path
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

    # Wait for profile to confirm login
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "prabesh78")))

    # Search for a book
    search_box = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search']"))
    )
    search_box.clear()
    search_box.send_keys("Rich Dad Poor Dad")

    # Wait for dropdown search results to load
    WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.search-results > li"))
    )

    print("Book search with valid title - PASSED")

except Exception as e:
    print("Book search with valid title - FAILED")
    print(f"Error: {e}")
    driver.save_screenshot("search_valid_failed.png")

finally:
    time.sleep(2)
    driver.quit()

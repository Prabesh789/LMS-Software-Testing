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
    # Login
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(OPENLIBRARY_USERNAME)
    driver.find_element(By.ID, "password").send_keys(OPENLIBRARY_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[name='login']").click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "My Books")))

    # Go to borrowed book
    driver.get("https://openlibrary.org/works/OL2010879W")

    read_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'cta-dropper')]//a[contains(text(),'Read')]"))
    )
    read_button.click()

    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[-1])

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3)

    # Click "Return now" inside shadow roots
    return_clicked = driver.execute_script("""
        try {
            const first = document.querySelector('ia-book-actions').shadowRoot;
            const collapsible = first.querySelector('collapsible-action-group').shadowRoot;
            const button = collapsible.querySelector('button.ia-button.danger.initial');
            if (button && button.innerText.includes("Return now")) {
                button.click();
                return true;
            }
            return false;
        } catch(e) {
            return false;
        }
    """)

    if return_clicked:
        print("✅ Return Book test - PASSED")
    else:
        print("❌ Return Book test - FAILED (Button not found)")
        driver.save_screenshot("return_not_found.png")

except Exception as e:
    print("❌ Return Book test - FAILED (Exception)")
    print(f"Error: {e}")
    driver.save_screenshot("return_failed_debug.png")

finally:
    time.sleep(3)
    driver.quit()

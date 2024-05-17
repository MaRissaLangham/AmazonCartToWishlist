"""Marissa Langham 05.16.2024
Amazon "Save for Later" items"""



import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

# Install and setup ChromeDriver
chromedriver_autoinstaller.install()

# Initialize WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Define your Amazon login credentials
AMAZON_EMAIL = 'your-email@example.com'
AMAZON_PASSWORD = 'your-password'

def amazonLogin(email, password):
    driver.get('https://www.amazon.com')
    wait = WebDriverWait(driver, 20)  # Increase the wait time to 20 seconds
    try:
        print("Waiting for the account list element to be clickable...")
        account_list = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='nav-link-accountList']")))
        account_list.click()
        print("Account list clicked.")
        email_input = wait.until(EC.element_to_be_clickable((By.ID, 'ap_email')))
        email_input.send_keys(email)
        driver.find_element(By.ID, 'continue').click()
        password_input = wait.until(EC.element_to_be_clickable((By.ID, 'ap_password')))
        password_input.send_keys(password)
        driver.find_element(By.ID, 'signInSubmit').click()
        print("Please complete the CAPTCHA and MFA steps manually.")
        time.sleep(15)  # Wait 15 seconds for manual CAPTCHA and MFA
    except TimeoutException:
        print("Timeout while waiting for the element.")
        driver.save_screenshot('debug_screenshot.png')  # Save a screenshot for debugging
        raise

def moveToWishlist():
    driver.get('https://www.amazon.com/gp/cart/view.html?ref_=nav_cart')
    time.sleep(5)  # Wait for page to load

    save_for_later_items = driver.find_elements(By.CSS_SELECTOR, '.sc-list-item')
    print(f"Found {len(save_for_later_items)} items in 'Save For Later'.")
    for item in save_for_later_items:
        try:
            actions = ActionChains(driver)
            # Find the "Add to list" button using the correct CSS selector or XPath
            add_to_list_button = item.find_element(By.XPATH, ".//input[@value='Add to list']")
            actions.move_to_element(add_to_list_button).perform()
            time.sleep(1)
            add_to_list_button.click()
            print("Clicked 'Add to list' button.")
            time.sleep(1)
            # Use class name to find the "Default List" option
            default_wishlist_option = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "a-size-small.cldd-list-name.a-nowrap"))
            )
            default_wishlist_option.click()
            print("Selected 'Default List' option.")
            time.sleep(2)  # Wait for the action to complete
        except Exception as e:
            print(f"Failed to move item: {e}")
            driver.save_screenshot('debug_screenshot.png')  # Save a screenshot for debugging

def verifyAndDelete():
    driver.get('https://www.amazon.com/gp/cart/view.html?ref_=nav_cart')
    time.sleep(5)  # Wait for page to load

    save_for_later_items = driver.find_elements(By.CSS_SELECTOR, '.sc-list-item')
    if len(save_for_later_items) == 0:
        print("All 'Save For Later' items have been moved to the wishlist.")
        # All items are moved, proceed to delete all
        while save_for_later_items:
            delete_buttons = driver.find_elements(By.XPATH, ".//input[@value='Delete']")
            for delete_button in delete_buttons:
                delete_button.click()
                time.sleep(2)  # Wait for the action to complete
            save_for_later_items = driver.find_elements(By.CSS_SELECTOR, '.sc-list-item')
    else:
        print("Some 'Save For Later' items could not be moved.")
        driver.save_screenshot('debug_screenshot.png')  # Save a screenshot for debugging

if __name__ == "__main__":
    try:
        amazonLogin(AMAZON_EMAIL, AMAZON_PASSWORD)
        moveToWishlist()
        verifyAndDelete()
    finally:
        driver.quit()


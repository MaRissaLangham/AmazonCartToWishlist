import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

# Install and setup ChromeDriver
chromedriver_autoinstaller.install()

# Initialize WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Define your Amazon login credentials
AMAZON_EMAIL = 'youremail@email.com'
AMAZON_PASSWORD = 'Password'

def amazon_login(email, password):
    driver.get('https://www.amazon.com')
    wait = WebDriverWait(driver, 10)
    account_list = wait.until(EC.element_to_be_clickable((By.ID, 'nav-link-accountList')))
    account_list.click()
    email_input = wait.until(EC.element_to_be_clickable((By.ID, 'ap_email')))
    email_input.send_keys(email)
    driver.find_element(By.ID, 'continue').click()
    password_input = wait.until(EC.element_to_be_clickable((By.ID, 'ap_password')))
    password_input.send_keys(password)
    driver.find_element(By.ID, 'signInSubmit').click()
    time.sleep(5)  # Wait for login to complete

def move_save_for_later_to_wishlist():
    driver.get('https://www.amazon.com/gp/cart/view.html?ref_=nav_cart')
    time.sleep(5)  # Wait for page to load

    save_for_later_items = driver.find_elements(By.CSS_SELECTOR, '.sc-list-save-later .sc-list-item')
    for item in save_for_later_items:
        try:
            actions = ActionChains(driver)
            move_to_wishlist_button = item.find_element(By.CSS_SELECTOR, '.a-dropdown-prompt')
            actions.move_to_element(move_to_wishlist_button).perform()
            time.sleep(1)
            move_to_wishlist_button.click()
            time.sleep(1)
            default_wishlist_option = driver.find_element(By.CSS_SELECTOR, '.a-popover-inner .a-declarative .a-dropdown-link')
            default_wishlist_option.click()
            time.sleep(2)  # Wait for the action to complete
        except Exception as e:
            print(f"Failed to move item: {e}")

def verify_and_delete_save_for_later_items():
    driver.get('https://www.amazon.com/gp/cart/view.html?ref_=nav_cart')
    time.sleep(5)  # Wait for page to load

    save_for_later_items = driver.find_elements(By.CSS_SELECTOR, '.sc-list-save-later .sc-list-item')
    if len(save_for_later_items) == 0:
        print("All 'Save For Later' items have been moved to the wishlist.")
        # All items are moved, proceed to delete all
        while save_for_later_items:
            delete_buttons = driver.find_elements(By.CSS_SELECTOR, '.sc-list-save-later .sc-action-delete input')
            for delete_button in delete_buttons:
                delete_button.click()
                time.sleep(2)  # Wait for the action to complete
            save_for_later_items = driver.find_elements(By.CSS_SELECTOR, '.sc-list-save-later .sc-list-item')
    else:
        print("Some 'Save For Later' items could not be moved.")

if __name__ == "__main__":
    amazon_login(AMAZON_EMAIL, AMAZON_PASSWORD)
    move_save_for_later_to_wishlist()
    verify_and_delete_save_for_later_items()
    driver.quit()

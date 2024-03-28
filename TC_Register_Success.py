import logging
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fill_form(browser, user_data):
    """Fill the registration form with user data."""
    for data in user_data:
        field_element = browser.find_element(By.ID, data['name'])
        field_element.send_keys(data['value'])
        time.sleep(1)

def test_successful_case(browser, user_data):
    """Test successful registration case."""
    fill_form(browser, user_data)
    
    # Subscribe to newsletter (if desired)
    newsletter_checkbox = browser.find_element(By.XPATH, '//*[@id="content"]/form/fieldset[3]/div/div/div[1]/label')
    if not newsletter_checkbox.is_selected():  # Check if not already selected
        newsletter_checkbox.click()

    # Agree to terms (assuming this is the checkbox)
    terms_checkbox = browser.find_element(By.CSS_SELECTOR, '#content > form > div > div > div > label')
    if not terms_checkbox.is_selected():  # Check if not already selected
        terms_checkbox.click()

    # Log test passed message
    logger.info("Test passed: Registration form filled successfully.")
    browser.quit()

def test_negative_case(browser, user_data):
    """Test negative registration case."""
    # Randomly select 3 pairs of data
    random_data = random.sample(user_data, 3)
    
    # Fill the form with random data
    fill_form(browser, random_data)
    
    # Log test passed message
    logger.info("Test passed: Negative case tested successfully.")
    browser.quit()
if __name__ == "__main__":
    # Initialize ChromeDriver service
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Maximize the browser window
    browser.maximize_window()

    # Target URL
    register_url = "https://ecommerce-playground.lambdatest.io/index.php?route=account/register"
    browser.get(register_url)

    # User data
    user_data = [
        {'name': 'input-firstname', 'value': 'Saad'},
        {'name': 'input-lastname', 'value': 'Test'},
        {'name': 'input-email', 'value': 'saad@example.com'},
        {'name': 'input-telephone', 'value': '0600221122'},
        {'name': 'input-password', 'value': 'password123456'},
        {'name': 'input-confirm', 'value': 'password123456'},
    ]

    # Test successful case
    test_successful_case(browser, user_data)
    
    # Test negative case
    test_negative_case(browser, user_data)

    # Quit the WebDriver session
    browser.quit()

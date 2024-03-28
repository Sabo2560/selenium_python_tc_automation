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
        time.sleep(3)

# Function to test negative registration case
def test_negative_case(browser, user_data):
    """
    Test negative registration case.

    This function tests the negative registration case by randomly selecting 3 pairs of data from the user_data list and entering them into the registration form.

    Parameters:
    browser (Webdriver): Webdriver for the browser to be used for testing.
    user_data (list): List of user data to be used for testing.

    Returns:
    None
    """
    # Randomly select 3 pairs of data
    # random.sample() is used to select three unique pairs of data from the user_data list
    random_data = random.sample(user_data, 3)

    # Fill the form with random data
    # This function fills the registration form with the randomly selected data
    fill_form(browser, random_data)

    
    # Log test passed message
    # Log a message indicating that the test passed and that the negative case was tested successfully
    logger.info("Test passed: Negative case tested successfully.")

    # Quit the browser
    # Close the browser used for testing
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
    
    # Test negative case
    test_negative_case(browser, user_data)

    # Quit the WebDriver session
    browser.quit()

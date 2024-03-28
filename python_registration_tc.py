import logging
import time
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fill_form(browser, user_data):
    """Fill the registration form with user data."""
    for data in user_data:
        field_element = browser.find_element(By.ID, data['name'])
        field_element.send_keys(data['value'])
        time.sleep(1)


def click_checkbox(browser, selector):
    """Click on checkbox if it's not already selected."""
    try:
        checkbox = browser.find_element(By.XPATH, selector)
        if not checkbox.is_selected():
            checkbox.click()
        return True
    except NoSuchElementException:
        logger.error("Checkbox element not found.")
        return False

def test_successful_case(browser, user_data):
    """Test successful registration case."""
    fill_form(browser, user_data)
    
    # Subscribe to newsletter
    if not click_checkbox(browser, '//*[@id="content"]/form/fieldset[3]/div/div/div[1]/label'):
        return
    
    # Agree to terms
    if not click_checkbox(browser, '//*[@id="content"]/form/div/div/div/label'):
        return

    # Submit the form
    try:
        submit_button = browser.find_element(By.XPATH, '//*[@id="content"]/form/div/div/input')
        submit_button.click()
        time.sleep(5)
    except NoSuchElementException:
        logger.error("Submit button element not found.")
        return

    # Check for successful registration message
    success_message = browser.find_element(By.XPATH, '//*[@id="content"]/h1')
    if "Your Account Has Been Created!" in success_message.text:
        logger.info("Test passed: Registration successful.")
    else:
        logger.error("Test failed: Registration unsuccessful.")
        
    
    # Check for successful registration message
    success_message = browser.find_element(By.XPATH, '//*[@id="content"]/h1')
    if "Your Account Has Been Created!" in success_message.text:
        logger.info("Test passed: Registration successful.")
    else:
        logger.error("Test failed: Registration unsuccessful.")
    browser.close()
    
if __name__ == "__main__":
    # Initialize ChromeDriver service
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Maximize the browser window
    browser.maximize_window()

    # Target URL
    register_url = "https://ecommerce-playground.lambdatest.io/index.php?route=account/register"
    browser.get(register_url)
    
    #
    # This Section is For Data (can be kept in different file)    
    # User data
    #
    
    fake = Faker()
    user_password =  fake.password()
    user_data = [
        {'name': 'input-firstname', 'value': fake.first_name()},
        {'name': 'input-lastname', 'value': fake.last_name()},
        {'name': 'input-email', 'value': fake.email()},
        {'name': 'input-telephone', 'value': '212641000100'},
        {'name': 'input-password', 'value': user_password},
        {'name': 'input-confirm', 'value': user_password},  # Generating another random password for confirmation
    ]
    
    # Test successful case
    test_successful_case(browser, user_data)
    
    # Quit the WebDriver session
    browser.quit()

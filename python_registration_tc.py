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

def fill_form(browser, form_data):
    """Fill the form with user data."""
    for data in form_data:
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

def registration_test_case(browser, registration_data):
    """Perform registration test case."""
    fill_form(browser, registration_data)

    # Subscribe to newsletter
    if not click_checkbox(browser, '//*[@id="content"]/form/fieldset[3]/div/div/div[1]/label'):
        return
    
    # Agree to terms
    if not click_checkbox(browser, '//*[@id="content"]/form/div/div/div/label'):
        return

    # Submit the registration form
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

def login_test_case(browser, email, password):
    """Perform login test case."""
    # Navigate to login page
    login_url = "https://ecommerce-playground.lambdatest.io/index.php?route=account/login"
    browser.get(login_url)

    # Fill login form with saved email and password
    login_data = [
        {'name': 'input-email', 'value': email},
        {'name': 'input-password', 'value': password},
    ]
    fill_form(browser, login_data)

    # Submit the login form
    try:
        submit_button = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div/form/input[1]')
        submit_button.click()
        time.sleep(5)
    except NoSuchElementException:
        logger.error("Submit button element not found.")
        return

def logout(browser):
    """Logout from the account."""
    try:
        logout_button = browser.find_element(By.XPATH, '//*[@id="column-right"]/div/a[14]')
        logout_button.click()
        time.sleep(5)
        logger.info("Logged out successfully.")
    except NoSuchElementException:
        logger.error("Logout button element not found.")

def test_successful_case(browser, registration_data):
    """Test successful registration case."""
    registration_test_case(browser, registration_data)

    # Extract email and password
    email = registration_data[2]['value']
    password = registration_data[4]['value']
    logger.info(f"Registered email: {email}, password: {password}")
    
    # Logout
    logout(browser)

    # Test login case using the registered email and password
    login_test_case(browser, email, password)

    # Check for successful login
    if "My Account" in browser.title:
        logger.info("Test passed: Login successful.")
    else:
        logger.error("Test failed: Login unsuccessful.")
    
    # Close the browser
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
    phone_number = fake.phone_number()
    
    # Extract digits from the generated phone number
    digits = ''.join(filter(str.isdigit, phone_number))
    
    # Format the phone number in 212XXXXXXXX format
    formatted_phone_number = '212' + digits[-9:]
    registration_data = [
        {'name': 'input-firstname', 'value': fake.first_name()},
        {'name': 'input-lastname', 'value': fake.last_name()},
        {'name': 'input-email', 'value': fake.email()},
        {'name': 'input-telephone', 'value': formatted_phone_number},
        {'name': 'input-password', 'value': user_password},
        {'name': 'input-confirm', 'value': user_password},  # Generating another random password for confirmation
    ]
    
    # Test successful registration case
    test_successful_case(browser, registration_data)
    
    # Quit the WebDriver session
    browser.quit()
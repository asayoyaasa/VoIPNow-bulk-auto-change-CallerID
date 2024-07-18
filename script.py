from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
import re
import time
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Configuration
login_url = 'https://your voip now ip/content.php?screen=login'
username = 'your username'
password = 'your password'
caller_id_values = [
    '1234567890', '2345678901', '3456789012'  # List of new caller ID values
]
links = [
    'https://your voip now ip/content.php?screen=extensions/terminal/edit_sip_terminal&from_details=true&extension_id={your ext id for example 1234 here}&user_id={your user id for example 12 here}',
# Add more links as needed
]

# Initialize WebDriver
options = FirefoxOptions()
options.headless = False  # Set to True if you want to run in headless mode
service = FirefoxService(executable_path='geckodriver-v0.34.0-win64\\geckodriver.exe')
driver = webdriver.Firefox(service=service, options=options)

def login():
    driver.get(login_url)
    username_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[name="login"]')
    
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()
    time.sleep(0.5)  # Wait for login to complete

def update_caller_id(link, caller_id_value):
    driver.get(link)
    time.sleep(1)  # Wait for the page to load

    # Extract the terminal identifier from the titleBox div
    title_box = driver.find_element(By.CLASS_NAME, 'titleBox')
    title_text = title_box.text
    terminal_identifier = re.search(r'\(([^)]+)\)', title_text)
    terminal_id = terminal_identifier.group(1) if terminal_identifier else "Unknown"

    # Get the current values of calleridname_user and calleridnum_user
    calleridname_field = driver.find_element(By.ID, 'calleridname_user')
    calleridnum_field = driver.find_element(By.ID, 'calleridnum_user')

    current_calleridname_value = calleridname_field.get_attribute('value')
    current_calleridnum_value = calleridnum_field.get_attribute('value')

    # Clear the fields and enter the new value
    calleridname_field.clear()
    calleridname_field.send_keys(caller_id_value)
    
    calleridnum_field.clear()
    calleridnum_field.send_keys(caller_id_value)

    # If no explicit save button, and form submission is via Enter key:
    calleridnum_field.send_keys(Keys.RETURN)
    time.sleep(1)  # Wait for the changes to be saved

    # Output the change to the terminal with current time
    current_time = datetime.now().strftime('%d/%m/%y %H:%M:%S')
    print(f'{Fore.YELLOW}{current_time}{Style.RESET_ALL} - {Fore.BLUE}{terminal_id}{Style.RESET_ALL} done changed from {Fore.RED}"{current_calleridname_value}"{Style.RESET_ALL} to {Fore.GREEN}"{caller_id_value}"')

run_count = 0

try:
    login()
    for caller_id_value in caller_id_values:
        for link in links:
            update_caller_id(link, caller_id_value)
        run_count += 1
        if caller_id_values.index(caller_id_value) < len(caller_id_values) - 1:
            time.sleep(15 * 60)  # Wait for 15 minutes
finally:
    driver.quit()
    print(f'Script run {run_count} times. Please change number.')

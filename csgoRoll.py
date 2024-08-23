import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    options = webdriver.ChromeOptions()
    
    # Set the user data directory
    user_data_dir = r"C:\Users\Sirin\AppData\Local\Google\Chrome\User Data"
    
    # Set the profile directory (usually "Default" or "Profile 1", "Profile 2", etc.)
    profile_directory = "Default"
    
    options.add_argument(f"user-data-dir={user_data_dir}")
    options.add_argument(f"profile-directory={profile_directory}")
    
    # Disable the "Chrome is being controlled by automated test software" notification
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Add these options to help with the "DevToolsActivePort file doesn't exist" error
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    
    # Use the ChromeDriverManager to get the path to chromedriver
    chromedriver_path = ChromeDriverManager().install()
    service = Service(chromedriver_path)
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error creating driver: {e}")
        return None

def click_button(driver, xpath, wait_time=10, additional_delay=0):
    button = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    button.click()
    time.sleep(2 + additional_delay)  # Wait for 2 seconds after clicking, plus any additional delay

def wait_for_cloudflare(driver, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.ID, "cf-spinner"))
        )
        print("Cloudflare challenge passed or not present.")
    except:
        print("Timed out waiting for Cloudflare. Site might be inaccessible.")

def perform_button_sequence(driver):
                # First set of buttons
    click_button(driver, "/html/body/cw-root/mat-sidenav-container/mat-sidenav-content/div/cw-daily-free-boxes/cw-box-grid/section/cw-box-grid-item-gaming[1]/div/button", additional_delay=2)
    click_button(driver, "/html/body/div[4]/div[30]/div/mat-dialog-container/cw-quick-unbox-modal/div[2]/cw-unbox-actions/div/div[2]/div[3]/button")

    # Reload the base website
    driver.get("https://www.csgoroll.com/boxes/world/daily-free")
    WebDriverWait(driver, 6).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    # Second set of buttons
    click_button(driver, "/html/body/cw-root/mat-sidenav-container/mat-sidenav-content/div/cw-daily-free-boxes/cw-box-grid/section/cw-box-grid-item-gaming[2]/div/button", additional_delay=2)
    click_button(driver, "/html/body/div[4]/div[30]/div/mat-dialog-container/cw-quick-unbox-modal/div[2]/cw-unbox-actions/div/div[2]/div[3]/button")

def main():
    while True:
        driver = setup_driver()
        if driver is None:
            print("Failed to initialize driver. Retrying in 5 minutes...")
            time.sleep(300)  # Wait for 5 minutes before retrying
            continue
        
        try:
            # Navigate to the website
            driver.get("https://www.csgoroll.com/boxes/world/daily-free")
            
            # Wait for Cloudflare
            wait_for_cloudflare(driver)
            
            # Perform the button clicking sequence
            perform_button_sequence(driver)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the browser
            driver.quit()

if __name__ == "__main__":
    main()
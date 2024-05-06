from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# Set the path to the Chrome WebDriver
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Open a webpage
driver.get('https://elmwealth.com/coin-flip/')
time.sleep(1)

startButton = driver.find_element(By.XPATH, value= "/html/body/div/div/div/div[1]/div/div[6]/input").click()

# Define a wait
wait = WebDriverWait(driver, 10)  # wait up to 10 seconds

# create all controls
headsButton = driver.find_element(By.XPATH, value= "/html/body/div/div/div/div[3]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/input")
moneyCounter = driver.find_element(By.XPATH, value= "/html/body/div/div/div/div[3]/div[2]/div[2]/div[2]/div[1]/div/span/span")
inputField = driver.find_element(By.XPATH, value= "/html/body/div/div/div/div[3]/div[2]/div[2]/div[1]/div[2]/input")
startButton = driver.find_element(By.XPATH, value= "/html/body/div/div/div/div[3]/div[2]/div[2]/div[1]/div[3]/input")
clockMinute = driver.find_element(By.XPATH, value= "/html/body/div/div/div/div[3]/div[1]/span[1]")
clockSecond = driver.find_element(By.XPATH, value= "/html/body/div/div/div/div[3]/div[1]/span[2]")

# Create Loop to play the game
# While ClockMinute >0 and ClockSecond > 0
while clockMinute.text != "0" and clockSecond.text != "0":
    # print remaining Time
    print(clockMinute.text + ":" + clockSecond.text)
    # Click the heads button after waiting for the overlay to disappear
    # Wait until the overlay is no longer present
    wait.until(EC.invisibility_of_element((By.XPATH, '/html/body/div/div/div/div[2]/div')))
    headsButton.click()

    # Get the money counter
    money = moneyCounter.text

    #print the money counter
    print(money)

    # Enter 20% of the money counter
    inputField.send_keys(int(float(money)) * 0.2)

    # Click the start button
    startButton.click()

    # Get the clock minute and second
    clockMinute = driver.find_element(By.XPATH, value= "/html/body/div/div/div/div[3]/div[1]/span[1]")
    clockSecond = driver.find_element(By.XPATH, value= "/html/body/div/div/div/div[3]/div[1]/span[2]")


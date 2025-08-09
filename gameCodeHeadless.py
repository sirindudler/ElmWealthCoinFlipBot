from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from config import FIRST_NAME, LAST_NAME, EMAIL, LOCATION, SUBSCRIBE

# Set the path to the Chrome WebDriver
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Open a webpage
driver.get('https://elmwealth.com/coin-flip/')
time.sleep(3)

# Take a debug screenshot to see the page
driver.save_screenshot("debug_initial_page_headless.png")
print("Debug: Took screenshot of initial page")

# Try multiple strategies to find and click the start button
start_clicked = False

# Strategy 1: Look for common start button patterns
try:
    startButton = driver.find_element(By.CSS_SELECTOR, 'input[value*="Start"], button[value*="Start"], input[value*="Play"], button[value*="Play"]')
    startButton.click()
    start_clicked = True
    print("Found start button with CSS selector")
except:
    pass

# Strategy 2: XPath search
if not start_clicked:
    try:
        startButton = driver.find_element(By.XPATH, "//input[contains(@value, 'Start') or contains(@value, 'Play')] | //button[contains(@value, 'Start') or contains(@value, 'Play') or contains(text(), 'Start') or contains(text(), 'Play')]")
        startButton.click()
        start_clicked = True
        print("Found start button with XPath")
    except:
        pass

# Strategy 3: Look for any clickable element that might start the game
if not start_clicked:
    try:
        # Look for buttons or inputs anywhere on the page
        all_buttons = driver.find_elements(By.CSS_SELECTOR, 'input[type="button"], input[type="submit"], button')
        for button in all_buttons:
            button_text = button.get_attribute('value') or button.text or button.get_attribute('id') or button.get_attribute('class')
            if button_text and ('start' in button_text.lower() or 'play' in button_text.lower() or 'begin' in button_text.lower()):
                button.click()
                start_clicked = True
                print(f"Found start button by searching all buttons: {button_text}")
                break
    except:
        pass

if not start_clicked:
    print("Could not find start button automatically, trying to continue anyway...")

# Define a wait
wait = WebDriverWait(driver, 10)  # wait up to 10 seconds

# Wait for form to appear and fill it out
print("Waiting for form to appear...")
try:
    wait.until(EC.presence_of_element_located((By.ID, "form_page")))
    print("Form appeared!")
except:
    print("Form with ID 'form_page' not found, trying alternative selectors...")
    try:
        # Try to find the form by looking for form elements
        wait.until(EC.presence_of_element_located((By.NAME, "firstname")))
        print("Found form elements!")
    except:
        print("No form found - trying to continue without form...")

time.sleep(2)

# Fill out the form
first_name_field = driver.find_element(By.NAME, "firstname")
first_name_field.send_keys(FIRST_NAME)

last_name_field = driver.find_element(By.NAME, "lastname")
last_name_field.send_keys(LAST_NAME)

email_field = driver.find_element(By.NAME, "email")
email_field.send_keys(EMAIL)

# Select location using JavaScript to avoid click interception
if LOCATION == "US":
    location_radio = driver.find_element(By.CSS_SELECTOR, 'input[name="territory_2024"][value="US"]')
else:
    location_radio = driver.find_element(By.CSS_SELECTOR, 'input[name="territory_2024"][value="Non-US"]')
driver.execute_script("arguments[0].click();", location_radio)

# Handle subscription checkbox using JavaScript
subscribe_checkbox = driver.find_element(By.NAME, "game_subscribe")
if SUBSCRIBE != subscribe_checkbox.is_selected():
    driver.execute_script("arguments[0].click();", subscribe_checkbox)

# Find and click the "Start Playing" button
print("Looking for 'Start Playing' submit button...")

# First, scroll down to make sure we can see the submit button
print("Scrolling to bottom of form...")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)

try:
    submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Start Playing"]')
    print("Found 'Start Playing' button with CSS selector")
except:
    try:
        submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Start Playing']")
        print("Found 'Start Playing' button with XPath")
    except:
        try:
            # Try to find any submit button
            submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
            print(f"Found submit button with value: {submit_button.get_attribute('value')}")
        except:
            print("Could not find any submit button")
            exit()

print("Clicking 'Start Playing' button...")
# Make sure the button is in view and clickable
driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
time.sleep(1)

# Click the button
try:
    submit_button.click()
    print("Successfully clicked 'Start Playing' button")
except:
    driver.execute_script("arguments[0].click();", submit_button)
    print("Clicked 'Start Playing' button with JavaScript")

print("Waiting for game to load after clicking 'Start Playing'...")
time.sleep(8)  # Wait longer for the game to actually start

# Wait for the game to start and form to completely disappear
print("Waiting for form to disappear and game to start...")
try:
    # Wait for the form to disappear
    wait.until(EC.invisibility_of_element_located((By.ID, "form_page")))
    print("Form disappeared - game should be starting")
except:
    print("Form still visible, trying to close it...")
    try:
        # Try to close the form overlay
        driver.execute_script("document.getElementById('form_page').style.display = 'none';")
        print("Hid form with JavaScript")
    except:
        pass

# Additional wait and check for overlays
time.sleep(3)
try:
    # Check if there are any remaining overlays
    overlays = driver.find_elements(By.CSS_SELECTOR, '.hbspt-form, #form_page, [class*="overlay"], [class*="modal"]')
    for overlay in overlays:
        if overlay.is_displayed():
            driver.execute_script("arguments[0].style.display = 'none';", overlay)
            print("Hid overlay element")
except:
    pass
    
time.sleep(5)

print("Looking for game elements...")

# Try to find game elements with more flexible selectors
try:
    headsButton = driver.find_element(By.CSS_SELECTOR, 'input[value*="Heads"], button[value*="Heads"], input[id*="heads"], button[id*="heads"]')
    print("Found heads button")
except:
    try:
        headsButton = driver.find_element(By.XPATH, "//input[contains(@value, 'Heads')] | //button[contains(@value, 'Heads') or contains(text(), 'Heads')]")
        print("Found heads button with XPath")
    except:
        print("Could not find heads button")
        exit()

try:
    # Try various selectors for the money counter
    moneyCounter = driver.find_element(By.CSS_SELECTOR, 'span[class*="money"], span[class*="balance"], span[class*="amount"], span[class*="dollar"], div[class*="balance"], div[class*="money"]')
    print("Found money counter with CSS")
except:
    try:
        moneyCounter = driver.find_element(By.XPATH, "//span[contains(@class, 'money') or contains(@class, 'balance') or contains(@class, 'amount') or contains(@class, 'dollar')] | //div[contains(@class, 'money') or contains(@class, 'balance') or contains(@class, 'amount')]")
        print("Found money counter with XPath")
    except:
        try:
            # Look for any element containing a dollar sign
            moneyCounter = driver.find_element(By.XPATH, "//*[contains(text(), '$')]")
            print("Found money counter by dollar sign")
        except:
            print("Could not find money counter with any method")
            exit()

try:
    inputField = driver.find_element(By.CSS_SELECTOR, 'input[type="number"], input[placeholder*="bet"], input[placeholder*="amount"]')
    print("Found input field")
except:
    try:
        inputField = driver.find_element(By.XPATH, "//input[@type='number' or contains(@placeholder, 'bet') or contains(@placeholder, 'amount')]")
        print("Found input field with XPath")
    except:
        print("Could not find input field")
        exit()

try:
    startButton = driver.find_element(By.CSS_SELECTOR, 'input[value*="Flip"], button[value*="Flip"], input[value*="Play"], button[value*="Play"]')
    print("Found start/flip button")
except:
    try:
        startButton = driver.find_element(By.XPATH, "//input[contains(@value, 'Flip') or contains(@value, 'Play')] | //button[contains(@value, 'Flip') or contains(@value, 'Play') or contains(text(), 'Flip') or contains(text(), 'Play')]")
        print("Found start/flip button with XPath")
    except:
        print("Could not find start/flip button")
        exit()

try:
    # Try to find clock elements with various approaches
    clockMinute = driver.find_element(By.CSS_SELECTOR, 'span[class*="minute"], span[class*="time"]:first-child, div[class*="time"] span:first-child')
    clockSecond = driver.find_element(By.CSS_SELECTOR, 'span[class*="second"], span[class*="time"]:last-child, div[class*="time"] span:last-child')
    print("Found clock elements")
except:
    try:
        clockMinute = driver.find_element(By.XPATH, "//span[contains(@class, 'minute') or contains(@class, 'time')][1] | //*[contains(@class, 'time')]//span[1]")
        clockSecond = driver.find_element(By.XPATH, "//span[contains(@class, 'second') or contains(@class, 'time')][2] | //*[contains(@class, 'time')]//span[2]")
        print("Found clock elements with XPath")
    except:
        try:
            # Look for any elements that might contain time format MM:SS or just numbers
            time_elements = driver.find_elements(By.XPATH, "//*[contains(text(), ':') and string-length(text()) < 6]")
            if time_elements:
                # Try to parse MM:SS format
                time_text = time_elements[0].text
                if ':' in time_text:
                    parts = time_text.split(':')
                    if len(parts) == 2:
                        # Create fake elements that return the minute and second values
                        class FakeElement:
                            def __init__(self, text):
                                self.text = text
                        clockMinute = FakeElement(parts[0])
                        clockSecond = FakeElement(parts[1])
                        print("Found clock elements by parsing MM:SS format")
                    else:
                        raise Exception("Invalid time format")
                else:
                    raise Exception("No colon found in time")
            else:
                raise Exception("No time elements found")
        except:
            print("Could not find clock elements with any method")
            # For now, let's use a fallback - assume we have 30 minutes
            class FakeElement:
                def __init__(self, text):
                    self.text = text
            clockMinute = FakeElement("30")
            clockSecond = FakeElement("00")
            print("Using fallback clock values (30:00)")

# Create data file
with open("CoinFlipGameData.txt", "w") as f:
    f.write("#RandomWalk1\n")

# Create Loop to play the game
# While ClockMinute >0 and ClockSecond > 0
iteration_count = 0
max_iterations = 50  # Prevent infinite loops
print(f"Starting game loop with max {max_iterations} iterations...")

while int(clockMinute.text) * 60 + int(clockSecond.text) > 4 and iteration_count < max_iterations:
    iteration_count += 1
    print(f"Iteration {iteration_count}/{max_iterations} - Time: {clockMinute.text}:{clockSecond.text}")
    # Click the heads button after waiting for the overlay to disappear
    # Wait until any overlays are no longer present and use JavaScript click to avoid interception
    try:
        wait.until(EC.invisibility_of_element((By.XPATH, '/html/body/div/div/div/div[2]/div')))
    except:
        pass
    
    # Use JavaScript to click the heads button to avoid click interception
    driver.execute_script("arguments[0].click();", headsButton)

    # Get the money counter and log all potential money elements
    money = moneyCounter.text.strip()
    print(f"Money counter text: '{money}'")
    
    # Debug: Find all elements that might contain money information
    try:
        all_money_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '$') or contains(@class, 'balance') or contains(@class, 'money') or contains(@class, 'amount')]")
        print("All potential money elements found:")
        for i, elem in enumerate(all_money_elements[:10]):  # Limit to first 10 to avoid spam
            elem_text = elem.text.strip()
            elem_class = elem.get_attribute('class') or 'no-class'
            elem_tag = elem.tag_name
            print(f"  {i+1}. {elem_tag}.{elem_class} = '{elem_text}'")
            if '$' in elem_text and elem_text != money:
                print(f"     ^ This element has $ but we're not using it!")
    except:
        print("Could not debug money elements")

    # Extract numeric value from money text (remove $ and other characters)
    try:
        # Remove $ and other non-numeric characters except decimal point
        money_clean = ''.join(c for c in money if c.isdigit() or c == '.')
        if money_clean:
            money_value = float(money_clean)
        else:
            # If no money found, start with default amount
            money_value = 100.0
            print(f"No money value found, using default: {money_value}")
    except:
        money_value = 100.0
        print(f"Error parsing money, using default: {money_value}")

    print(f"Money value: {money_value}")

    # Enter 20% of the money counter
    bet_amount = int(money_value * 0.2)
    print(f"Betting: {bet_amount}")
    
    # Clear the input field first
    inputField.clear()
    inputField.send_keys(str(bet_amount))

    # Click the start button using JavaScript to avoid click interception
    driver.execute_script("arguments[0].click();", startButton)

    # Save data to file
    with open("CoinFlipGameData.txt", "a") as f:
        f.write(f"{money_value}\n")
        f.write(f"{clockMinute.text}:{clockSecond.text}\n")

    # Get the clock minute and second (try to refresh them)
    try:
        time_elements = driver.find_elements(By.XPATH, "//*[contains(text(), ':') and string-length(text()) < 6]")
        if time_elements:
            time_text = time_elements[0].text
            if ':' in time_text:
                parts = time_text.split(':')
                if len(parts) == 2:
                    class FakeElement:
                        def __init__(self, text):
                            self.text = text
                    clockMinute = FakeElement(parts[0])
                    clockSecond = FakeElement(parts[1])
                    print(f"Updated clock to: {clockMinute.text}:{clockSecond.text}")
    except:
        # Use fallback if we can't update the clock
        pass

    # Add a small delay between iterations to avoid overwhelming the server
    time.sleep(0.5)

print(f"Game loop completed after {iteration_count} iterations")

# wait for 10 seconds
time.sleep(10)

# screenshot the page, name it screenshot + date and time
driver.save_screenshot("screenshot_" + time.strftime("%Y%m%d-%H%M") + ".png")
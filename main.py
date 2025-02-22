from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import requests



url = "https://google.com"
response = requests.get(url, timeout=10)
print(f"Status Code: {response.status_code}")
print(f"Response Headers: {response.headers}")



# Replace with your bot token and chat ID
BOT_TOKEN = "7057194211:AAF_StFo_FwRn1AR_XOJQurXuYgh5ZvO2b4"
CHAT_ID = "6260151149"


# Set up Selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-http2")  # Disable HTTP/2 protocol
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

# Specify the path to the ChromeDriver binary
chrome_service = Service("/usr/local/bin/chromedriver")

# Enable browser logging
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}


# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


# Capture and print browser logs
logs = driver.get_log('performance')
for log in logs:
    print(log)

# Open the website
# Set a higher timeout for page loading
driver.set_page_load_timeout(300)  # Wait up to 5 minutes for page to load


driver.get(url)
    
    # Wait until an important element loads (modify selector as needed)
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)

print("Page loaded successfully.")




# Print the page title to confirm the page loaded
print("Page title:", driver.title)


 


def Container():
    try:
        Ball_Container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//html/body/div[1]/div/div/div/footer/div[2]/div[1]/div/div[1]"))
        )

        Ball_numbers = []
        for i in range(1, 7):
            container_xpath = f'/html/body/div[1]/div/div/div/footer/div[2]/div[1]/div/div[1]/div[{i}]/div/div'
            container_numbers = driver.find_element(By.XPATH, container_xpath)
            Numbers = container_numbers.text

            # Convert to integer before appending
            try:
                Ball_numbers.append(int(Numbers))
                print(f"Container {i}, Ball-Number is: {int(Numbers)}")
                
            except ValueError:
                print(f"Container {i}, Ball-Number is not a valid integer: {Numbers}")

        return Ball_numbers

    except Exception as e:
        print(f'Error: {e}')

def Hot_Numbers():
    try:

        Hot_Balls = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/main/div[1]/div[2]/div[2]/div[1]"))
    )
        print("Element found:", Hot_Numbers.text)

        First_Hot_Ball = Hot_Balls.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div[2]/div[2]/div[1]/div[1]/span').text
        Second_Hot_Ball = Hot_Balls.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div[2]/div[2]/div[1]/div[2]/span').text
        Third_Hot_Ball = Hot_Balls.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div[2]/div[2]/div[1]/div[3]/span').text
        Fourth_Hot_Ball = Hot_Balls.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div[2]/div[2]/div[1]/div[4]/span').text

        # Convert strings to integers
        try:
            Balls = [int(First_Hot_Ball), int(Second_Hot_Ball), int(Third_Hot_Ball), int(Fourth_Hot_Ball)]
            print(Balls)
        except ValueError:
            print("One or more hot balls are not valid integers")
            Balls = []

        return Balls

    except Exception as e:
        print(f"An error occured: {e}")

def send_telegram_message(message):
    """Sends a message to your Telegram bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("Telegram notification sent successfully!")
        else:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def checker():
    failure_count = 0
    max_failure_count = 0

    # Initialize the flag for the first run
    waiting_for_container = True

    while True:
       
            if waiting_for_container:
                # Call the Hot_Numbers function
                Balls = Hot_Numbers()
                print(Balls)
                print("Hot numbers updated.")
                waiting_for_container = False  # Now wait for the timer to reach 40
            else:
                # Wait for the timer element to be present
                Timer = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/footer/div[2]/div[4]/div/div/div'))
                )

                # Get the timer value
                Time = Timer.text.strip()

                # Check if the timer equals 40
                if Time.isdigit() and int(Time) == 40:
                    print(f"Timer matched 40. Current time: {Time}")
                    
                    # Call the Container function
                    Ball_numbers = Container()

                    # Check if any of the hot numbers are in the container numbers
                    if any(ball in Ball_numbers for ball in Balls):
                        failure_count += 1  # Increment failure count when a match is found
                        print(f"Match found! Failure count incremented to {failure_count}")
                        
                        if failure_count >= 2:
                            message = (
                                f"The bot has failed {failure_count} times.\n"
                                f"Play {Balls} as ball zero in the next round.\n"
                                f"The highest failure count so far is {max_failure_count}."
                            )
                            send_telegram_message(message)

                    else:
                        failure_count = 0  # Reset failure count when no match is found
                        print(f"No match found. Failure count reset to {failure_count}")

                    # Update the maximum failure count if the current one exceeds it
                    if failure_count > max_failure_count:
                        max_failure_count = failure_count
                        print(f"New highest failure count: {max_failure_count}")

                    # Wait 10 seconds and prepare to call Hot_Numbers again
                    time.sleep(10)
                    waiting_for_container = True  # Switch back to update Hot_Numbers
        

checker()

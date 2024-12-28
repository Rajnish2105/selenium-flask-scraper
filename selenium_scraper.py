from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # Add this import
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime
from dotenv import load_dotenv
import uuid
import os
import time

# Load environment variables
load_dotenv()
X_EMAIL = os.getenv('X_EMAIL')
X_USERNAME = os.getenv('X_USERNAME')
X_PASSWORD = os.getenv('X_PASSWORD')

def wait_and_find_element(driver, by, value, timeout=30):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def scrape_trending_topics(max_retries=3):
    driver = None
    try:
        # Configure Chrome options
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # Comment this out for debugging
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        # Remove proxy configuration temporarily for testing
        current_dir = os.path.dirname(os.path.abspath(__file__))
        chromedriver_path = os.path.join(current_dir, "chromedriver.exe")
        service = Service(chromedriver_path)
        
        print("Launching Chrome...")
        driver = webdriver.Chrome(service=service, options=options)
        
        print("Navigating to x login...")
        driver.get("https://x.com/i/flow/login")
        time.sleep(5)  # Increase initial wait time
        
        print("Entering email...")
        # Updated selector for email input
        email_input = wait_and_find_element(
            driver, 
            By.XPATH, 
            "//input[@autocomplete='username']"
        )
        email_input.send_keys(X_EMAIL)
        email_input.send_keys(Keys.RETURN)
        time.sleep(3)
        
        print("Handling possible username verification...")
        try:
            username_input = wait_and_find_element(
                driver,
                By.XPATH,
                "//input[@data-testid='ocfEnterTextTextInput']",
                timeout=5
            )
            username_input.send_keys(X_USERNAME)
            username_input.send_keys(Keys.RETURN)
            time.sleep(2)
        except TimeoutException:
            print("Username verification skipped")
            
        print("Entering password...")
        password_input = wait_and_find_element(
            driver,
            By.XPATH,
            "//input[@name='password']"
        )
        password_input.send_keys(X_PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)
        
        print("Navigating to Explore...")
        driver.get("https://x.com/explore")
        time.sleep(5)
        
        print("Getting trending topics...")
        # Updated selector for trends
        trends = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@data-testid='trend']//span[contains(@class, 'css-')]")
            )
        )
        
        trending_topics = []
        for trend in trends[:5]:
            try:
                trending_topics.append(trend.text)
            except:
                continue
                
        print(f"Found {len(trending_topics)} trending topics")
        
        return {
            "_id": str(uuid.uuid4()),
            "trend1": trending_topics[0] if len(trending_topics) > 0 else "N/A",
            "trend2": trending_topics[1] if len(trending_topics) > 1 else "N/A",
            "trend3": trending_topics[2] if len(trending_topics) > 2 else "N/A",
            "trend4": trending_topics[3] if len(trending_topics) > 3 else "N/A",
            "trend5": trending_topics[4] if len(trending_topics) > 4 else "N/A",
            "trend6": trending_topics[5] if len(trending_topics) > 5 else "N/A",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {"error": str(e)}

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # Test the scraper
    result = scrape_trending_topics()
    print(result)

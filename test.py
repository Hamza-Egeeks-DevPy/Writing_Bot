# test_bot_interaction.py

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
from webdriver_manager.chrome import ChromeDriverManager
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("test_bot_interaction.log"),
        logging.StreamHandler()
    ]
)

def initialize_driver():
    """
    Initializes the Chrome WebDriver using webdriver_manager for automatic driver management.
    Returns:
        driver (webdriver.Chrome): An instance of Chrome WebDriver.
    """
    chrome_options = Options()
    # Uncomment the following line to run Chrome in headless mode
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )
        logging.info("Chrome WebDriver initialized successfully.")
        return driver
    except Exception as e:
        logging.error(f"Failed to initialize Chrome WebDriver: {e}")
        raise

def send_prompt(driver, prompt_text, article_index, wait_time=60):
    """
    Sends a prompt to the bot, clicks the "Generate" button, waits for the response,
    clicks the "Copy" button, and extracts the response text.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        prompt_text (str): The prompt to send to the bot.
        article_index (int): The index of the article element to interact with.
        wait_time (int): Maximum time to wait for elements to appear.

    Returns:
        response_text (str): The text of the bot's response.
    """
    try:
        # Locate the prompt text area
        prompt_area = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.ID, "prompt-textarea"))
        )
        prompt_area.clear()
        prompt_area.send_keys(prompt_text)
        logging.info(f"Entered prompt: '{prompt_text}'")

        # Locate and click the "Generate" button
        generate_button = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send prompt']"))
        )
        generate_button.click()
        logging.info("Clicked the 'Generate' button.")

        # Construct dynamic XPath for the "Copy" button
        copy_button_xpath = (
            f"/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[{article_index}]/"
            f"div/div/div[2]/div/div[2]/div/div/span[2]/button"
        )

        # Wait for the "Copy" button to appear
        copy_button = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, copy_button_xpath))
        )
        copy_button.click()
        logging.info(f"Clicked the 'Copy' button in article[{article_index}].")

        # Optional: Wait briefly to ensure the copy action is complete
        time.sleep(2)

        # Extract the response text directly from the response container
        response_text_xpath = (
            f"/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[{article_index}]/"
            f"div/div/div[2]/div/div[1]/div/div"
        )
        response_element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, response_text_xpath))
        )
        response_text = response_element.text
        logging.info(f"Extracted response from article[{article_index}]: '{response_text[:100]}...'")  # Log first 100 chars

        return response_text

    except TimeoutException as te:
        logging.error(f"Timeout while processing prompt '{prompt_text}': {te}")
        take_screenshot(driver, f"timeout_prompt_{article_index}.png")
        return f"❌ Timeout: Failed to process prompt '{prompt_text}'."

    except NoSuchElementException as nse:
        logging.error(f"Element not found while processing prompt '{prompt_text}': {nse}")
        take_screenshot(driver, f"no_element_prompt_{article_index}.png")
        return f"❌ Error: Required element not found for prompt '{prompt_text}'."

    except ElementClickInterceptedException as ece:
        logging.error(f"Click intercepted while processing prompt '{prompt_text}': {ece}")
        take_screenshot(driver, f"click_intercepted_prompt_{article_index}.png")
        return f"❌ Error: Click intercepted for prompt '{prompt_text}'."

    except Exception as e:
        logging.error(f"Unexpected error while processing prompt '{prompt_text}': {e}")
        take_screenshot(driver, f"unexpected_error_prompt_{article_index}.png")
        return f"❌ Unexpected error: {e}."

def take_screenshot(driver, filename):
    """
    Takes a screenshot of the current browser window.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        filename (str): The filename for the screenshot.
    """
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    filepath = os.path.join(screenshots_dir, filename)
    try:
        driver.save_screenshot(filepath)
        logging.info(f"Screenshot saved as '{filepath}'.")
    except Exception as e:
        logging.error(f"Failed to take screenshot '{filepath}': {e}")

def main():
    # Replace this URL with the actual URL of your bot
    BOT_URL = "https://chatgpt.com/g/g-6737360a422881909250d42d11f53ea5-614-man-research-proposal-writing-bot"

    # Define the test prompts
    test_prompts = ["hello", "how are you"]

    # Initialize WebDriver
    driver = initialize_driver()

    try:
        # Navigate to the bot's URL
        driver.get(BOT_URL)
        logging.info(f"Navigated to bot URL: {BOT_URL}")

        # Allow the page to load completely
        time.sleep(5)  # Adjust sleep time as necessary

        # Iterate over test prompts
        for idx, prompt in enumerate(test_prompts, 1):
            article_index = 2 + 2 * (idx - 1)  # Starts at 2 and increments by 2
            logging.info(f"Processing Prompt {idx}: '{prompt}' with article_index={article_index}")

            response = send_prompt(driver, prompt, article_index)
            print(f"**Prompt {idx}:** {prompt}\n**Response {idx}:** {response}\n")

            # Optional: Wait before sending the next prompt
            time.sleep(3)  # Adjust sleep time as necessary

    finally:
        # Close the browser after the test
        driver.quit()
        logging.info("Chrome WebDriver closed.")

if __name__ == "__main__":
    main()


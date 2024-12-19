

# import os
# import time
# import logging
# import undetected_chromedriver as uc
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import (
#     TimeoutException,
#     NoSuchElementException,
#     WebDriverException
# )

# def init_driver():
#     """
#     Initializes the Selenium WebDriver using an existing Chrome session with user-data-dir.
#     Ensure Chrome is running with remote debugging enabled at 127.0.0.1:9222.
#     """
#     chrome_options = Options()
#     # Update this path as needed for your local system.
#     chrome_options.add_argument(r'--user-data-dir=C:\\Users\\AbuBakar\\Desktop\\sessions')
#     chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

#     try:
#         driver = uc.Chrome(
#             options=chrome_options,
#             executable_path=ChromeDriverManager().install(),
#             service=Service(ChromeDriverManager().install())
#         )
#         logging.info("Initialized Chrome WebDriver successfully in visible mode.")
#     except WebDriverException as e:
#         logging.error(f"Error initializing Chrome WebDriver: {e}")
#         raise Exception(f"Error initializing Chrome WebDriver: {e}")
#     return driver

# def process_bot(driver, bot_url, prompts):
#     """
#     Sends prompts to the bot and extracts responses using fixed XPaths.
#     After collecting all responses, waits 30 seconds before returning.

#     Args:
#         driver: Selenium WebDriver instance.
#         bot_url: URL of the bot interface.
#         prompts: List of dictionaries with 'prompt' and 'expected'.

#     Returns:
#         A list of dictionaries containing 'prompt' and 'answer' for each prompt.
#     """
#     responses = []
#     try:
#         driver.get(bot_url)
#         logging.info(f"Navigated to bot URL: {bot_url}")

#         # Define fixed XPaths for each prompt
#         fixed_xpaths = {
#             1: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[2]/div/div/div[2]/div/div[1]/div/div",
#             2: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[4]/div/div/div[2]/div/div[1]/div/div",
#             3: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[6]/div/div/div[2]/div/div[1]/div/div",
#             4: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[1]/div/div",
#             5: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[10]/div/div/div[2]/div/div[1]/div/div",
#             6: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[12]/div/div/div[2]/div/div[1]/div/div"
#         }

#         for idx, prompt_obj in enumerate(prompts, start=1):
#             if idx > 6:
#                 logging.warning(f"Received more than 6 prompts. Ignoring Prompt {idx}.")
#                 break  # Limit to 6 prompts as per provided XPaths

#             prompt = prompt_obj["prompt"]
#             logging.info(f"Sending Prompt {idx}: {prompt}")

#             # Locate the prompt text area
#             try:
#                 prompt_area = WebDriverWait(driver, 120).until(
#                     EC.presence_of_element_located((By.ID, "prompt-textarea"))
#                 )
#                 prompt_area.click()
#                 prompt_area.clear()
#                 prompt_area.send_keys(prompt)
#                 logging.info(f"Entered Prompt {idx} into the text area.")
#             except TimeoutException:
#                 logging.error(f"Timeout: Prompt text area not found for Prompt {idx}.")
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': "❌ Timeout: Prompt text area not found."
#                 })
#                 continue
#             except Exception as e:
#                 logging.error(f"Error interacting with prompt text area for Prompt {idx}: {e}")
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': f"❌ Error entering prompt: {e}"
#                 })
#                 continue

#             # Locate and click the generate button
#             try:
#                 generate_button = WebDriverWait(driver, 40).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send prompt']"))
#                 )
#                 generate_button.click()
#                 logging.info(f"Clicked 'Send prompt' button for Prompt {idx}.")
#             except TimeoutException:
#                 logging.error(f"Timeout: Generate button not found or not clickable for Prompt {idx}.")
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': "❌ Timeout: Generate button not found or not clickable."
#                 })
#                 continue
#             except Exception as e:
#                 logging.error(f"Error clicking generate button for Prompt {idx}: {e}")
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': f"❌ Error clicking generate button: {e}"
#                 })
#                 continue

#             # Wait for 5 seconds to allow the response to generate
#             logging.info(f"Waiting 5 seconds for Prompt {idx} response to generate.")
#             time.sleep(5)

#             # Locate the response using the fixed XPath
#             try:
#                 response_element = WebDriverWait(driver, 60).until(
#                     EC.presence_of_element_located((By.XPATH, fixed_xpaths[idx]))
#                 )
#                 response_text = response_element.text.strip()
#                 logging.info(f"Captured response for Prompt {idx}: {response_text[:100]}...")

#                 responses.append({
#                     'prompt': prompt,
#                     'answer': response_text
#                 })
#             except TimeoutException:
#                 logging.error(f"Timeout: Response not received for Prompt {idx}.")
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': f"❌ Timeout: Response not received for Prompt {idx}."
#                 })
#             except NoSuchElementException:
#                 logging.error(f"No such element: Unable to locate response text for Prompt {idx}.")
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': f"❌ No such element: Response text not found for Prompt {idx}."
#                 })
#             except Exception as e:
#                 logging.error(f"Error retrieving the response for Prompt {idx}: {e}")
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': f"❌ Failed to retrieve response: {e}"
#                 })

#             # Wait 5 seconds before sending the next prompt
#             logging.info(f"Waiting 5 seconds before sending the next prompt.")
#             time.sleep(5)

#         # After collecting all responses, wait 30 seconds before returning
#         logging.info("All prompts processed. Waiting 30 seconds before returning responses.")
#         time.sleep(30)
#         return responses

#     except Exception as e:
#         logging.error(f"An unexpected error occurred while interacting with the bot: {e}")
#         return responses


# import os
# import time
# import logging
# import undetected_chromedriver as uc
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import (
#     TimeoutException,
#     NoSuchElementException,
#     WebDriverException
# )

# def init_driver():
#     """
#     Initializes the Selenium WebDriver using an existing Chrome session with user-data-dir.
#     Ensure Chrome is running with remote debugging enabled at 127.0.0.1:9222.
#     """
#     chrome_options = Options()
#     # Update this path as needed for your local system.
#     chrome_options.add_argument(r'--user-data-dir=C:\\Users\\AbuBakar\\Desktop\\sessions')
#     chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

#     try:
#         driver = uc.Chrome(
#             options=chrome_options,
#             executable_path=ChromeDriverManager().install(),
#             service=Service(ChromeDriverManager().install())
#         )
#         logging.info("Initialized Chrome WebDriver successfully in visible mode.")
#     except WebDriverException as e:
#         logging.error(f"Error initializing Chrome WebDriver: {e}")
#         raise Exception(f"Error initializing Chrome WebDriver: {e}")
#     return driver

# def wait_for_full_response(driver, xpath, timeout=120):
#     """
#     Waits until the response text at the given XPath stops changing, indicating that
#     the response is fully loaded.

#     Args:
#         driver: Selenium WebDriver instance.
#         xpath: XPath of the response element.
#         timeout: Maximum time to wait for the response to fully load.

#     Returns:
#         The fully loaded response text, or an empty string if timeout occurs.
#     """
#     wait = WebDriverWait(driver, timeout)
#     try:
#         response_element = wait.until(
#             EC.presence_of_element_located((By.XPATH, xpath))
#         )
#         logging.info(f"Located response element at XPath: {xpath}")

#         previous_text = ""
#         stable_count = 0
#         max_stable = 3  # Number of consecutive checks with no change to consider the text stable
#         check_interval = 2  # Seconds between checks

#         while stable_count < max_stable:
#             current_text = response_element.text.strip()
#             if current_text == previous_text:
#                 stable_count += 1
#                 logging.debug(f"Response text stable count: {stable_count}")
#             else:
#                 stable_count = 0
#                 logging.debug("Response text changed. Resetting stable count.")
#                 previous_text = current_text
#             time.sleep(check_interval)

#         logging.info("Response text has stabilized.")
#         return current_text

#     except TimeoutException:
#         logging.error(f"Timeout: Unable to fully load response at XPath: {xpath}")
#         return ""

# def process_bot(driver, bot_url, prompts):
#     """
#     Sends prompts to the bot and extracts responses using fixed XPaths.
#     After collecting all responses, waits 30 seconds before returning.

#     Args:
#         driver: Selenium WebDriver instance.
#         bot_url: URL of the bot interface.
#         prompts: List of dictionaries with 'prompt' and 'expected'.

#     Returns:
#         A list of dictionaries containing 'prompt' and 'answer' for each prompt.
#     """
#     responses = []
#     try:
#         driver.get(bot_url)
#         logging.info(f"Navigated to bot URL: {bot_url}")

#         # Define fixed XPaths for each prompt
#         fixed_xpaths = {
#             1: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[2]/div/div/div[2]/div/div[1]/div/div",
#             2: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[4]/div/div/div[2]/div/div[1]/div/div",
#             3: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[6]/div/div/div[2]/div/div[1]/div/div",
#             4: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[1]/div/div",
#             5: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[10]/div/div/div[2]/div/div[1]/div/div",
#             6: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[12]/div/div/div[2]/div/div[1]/div/div"
#         }

#         for idx, prompt_obj in enumerate(prompts, start=1):
#             if idx > 6:
#                 logging.warning(f"Received more than 6 prompts. Ignoring Prompt {idx}.")
#                 break  # Limit to 6 prompts as per provided XPaths

#             prompt = prompt_obj["prompt"]
#             logging.info(f"Sending Prompt {idx}: {prompt}")

#             # Locate the prompt text area
#             try:
#                 prompt_area = WebDriverWait(driver, 120).until(
#                     EC.presence_of_element_located((By.ID, "prompt-textarea"))
#                 )
#                 prompt_area.click()
#                 prompt_area.clear()
#                 prompt_area.send_keys(prompt)
#                 logging.info(f"Entered Prompt {idx} into the text area.")
#             except TimeoutException:
#                 logging.error(f"Timeout: Prompt text area not found for Prompt {idx}.")
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': "❌ Timeout: Prompt text area not found."
#                 })
#                 continue
#             except Exception as e:
#                 logging.error(f"Error interacting with prompt text area for Prompt {idx}: {e}")
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': f"❌ Error entering prompt: {e}"
#                 })
#                 continue

#             # Locate and click the generate button
#             try:
#                 generate_button = WebDriverWait(driver, 40).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send prompt']"))
#                 )
#                 generate_button.click()
#                 logging.info(f"Clicked 'Send prompt' button for Prompt {idx}.")
#             except TimeoutException:
#                 logging.error(f"Timeout: Generate button not found or not clickable for Prompt {idx}.")
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': "❌ Timeout: Generate button not found or not clickable."
#                 })
#                 continue
#             except Exception as e:
#                 logging.error(f"Error clicking generate button for Prompt {idx}: {e}")
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': f"❌ Error clicking generate button: {e}"
#                 })
#                 continue

#             # Wait for a short duration to allow the response to start generating
#             logging.info(f"Waiting 5 seconds for Prompt {idx} response to generate.")
#             time.sleep(5)

#             # Use the fixed XPath to extract the response text
#             xpath = fixed_xpaths.get(idx)
#             if not xpath:
#                 logging.error(f"No fixed XPath defined for Prompt {idx}.")
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': "❌ No XPath defined for this prompt."
#                 })
#                 continue

#             response_text = wait_for_full_response(driver, xpath, timeout=120)
#             if response_text:
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': response_text
#                 })
#                 logging.info(f"Successfully captured response for Prompt {idx}.")
#             else:
#                 responses.append({
#                     'prompt': prompt,
#                     'answer': f"❌ Unable to capture response for Prompt {idx}."
#                 })

#             # Wait 5 seconds before sending the next prompt
#             logging.info(f"Waiting 5 seconds before sending the next prompt.")
#             time.sleep(5)

#         # After collecting all responses, wait 30 seconds before returning
#         logging.info("All prompts processed. Waiting 30 seconds before finalizing responses.")
#         time.sleep(30)
#         return responses

#     except Exception as e:
#         logging.error(f"An unexpected error occurred in process_bot: {e}")
#         return responses

import os
import time
import logging
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)

def init_driver():
    """
    Initializes the Selenium WebDriver using an existing Chrome session with user-data-dir.
    Ensure Chrome is running with remote debugging enabled at 127.0.0.1:9222.
    """
    chrome_options = Options()
    # Update this path as needed for your local system.
    chrome_options.add_argument(r'--user-data-dir=C:\\Users\\Mussadiq Ali\\Desktop\\session')
    # E:\Writing_Bot\Bot with updated code using frontend\session
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    try:
        driver = uc.Chrome(
            options=chrome_options,
            executable_path=ChromeDriverManager().install(),
            service=Service(ChromeDriverManager().install())
        )
        logging.info("Initialized Chrome WebDriver successfully in visible mode.")
    except WebDriverException as e:
        logging.error(f"Error initializing Chrome WebDriver: {e}")
        raise Exception(f"Error initializing Chrome WebDriver: {e}")
    return driver

def wait_for_full_response(driver, xpath, timeout=150):
    """
    Waits until the response text at the given XPath stops changing, indicating that
    the response is fully loaded.

    Args:
        driver: Selenium WebDriver instance.
        xpath: XPath of the response element.
        timeout: Maximum time to wait for the response to fully load.

    Returns:
        The fully loaded response text, or an empty string if timeout occurs.
    """
    wait = WebDriverWait(driver, timeout)
    try:
        response_element = wait.until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        logging.info(f"Located response element at XPath: {xpath}")

        previous_text = ""
        stable_count = 0
        max_stable = 3  # Number of consecutive checks with no change to consider the text stable
        check_interval = 2  # Seconds between checks

        while stable_count < max_stable:
            current_text = response_element.text.strip()
            if current_text == previous_text:
                stable_count += 1
                logging.debug(f"Response text stable count: {stable_count}")
            else:
                stable_count = 0
                logging.debug("Response text changed. Resetting stable count.")
                previous_text = current_text
            time.sleep(check_interval)

        logging.info("Response text has stabilized.")
        return current_text

    except TimeoutException:
        logging.error(f"Timeout: Unable to fully load response at XPath: {xpath}")
        return ""

def process_bot(driver, bot_url, prompts):
    """
    Sends prompts to the bot and extracts responses using fixed XPaths.
    After collecting all responses, waits 30 seconds before returning.

    Args:
        driver: Selenium WebDriver instance.
        bot_url: URL of the bot interface.
        prompts: List of dictionaries with 'prompt' and 'expected'.

    Returns:
        A list of dictionaries containing 'prompt' and 'answer' for each prompt.
    """
    responses = []
    try:
        driver.get(bot_url)
        logging.info(f"Navigated to bot URL: {bot_url}")

        # Define fixed XPaths for each prompt
        fixed_xpaths = {
            1: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[2]/div/div/div[2]/div/div[1]/div/div",
            2: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[4]/div/div/div[2]/div/div[1]/div/div",
            3: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[6]/div/div/div[2]/div/div[1]/div/div",
            4: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[1]/div/div",
            5: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[10]/div/div/div[2]/div/div[1]/div/div",
            6: "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[12]/div/div/div[2]/div/div[1]/div/div"
        }

        for idx, prompt_obj in enumerate(prompts, start=1):
            if idx > 6:
                logging.warning(f"Received more than 6 prompts. Ignoring Prompt {idx}.")
                break  # Limit to 6 prompts as per provided XPaths

            prompt = prompt_obj["prompt"]
            logging.info(f"Sending Prompt {idx}: {prompt}")

            # Locate the prompt text area
            try:
                prompt_area = WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.ID, "prompt-textarea"))
                )
                prompt_area.click()
                prompt_area.clear()
                prompt_area.send_keys(prompt)
                logging.info(f"Entered Prompt {idx} into the text area.")
            except TimeoutException:
                logging.error(f"Timeout: Prompt text area not found for Prompt {idx}.")
                responses.append({
                    'prompt': prompt,
                    'answer': "❌ Timeout: Prompt text area not found."
                })
                continue
            except Exception as e:
                logging.error(f"Error interacting with prompt text area for Prompt {idx}: {e}")
                responses.append({
                    'prompt': prompt,
                    'answer': f"❌ Error entering prompt: {e}"
                })
                continue

            # Locate and click the generate button
            try:
                generate_button = WebDriverWait(driver, 40).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send prompt']"))
                )
                generate_button.click()
                logging.info(f"Clicked 'Send prompt' button for Prompt {idx}.")
            except TimeoutException:
                logging.error(f"Timeout: Generate button not found or not clickable for Prompt {idx}.")
                responses.append({
                    'prompt': prompt,
                    'answer': "❌ Timeout: Generate button not found or not clickable."
                })
                continue
            except Exception as e:
                logging.error(f"Error clicking generate button for Prompt {idx}: {e}")
                responses.append({
                    'prompt': prompt,
                    'answer': f"❌ Error clicking generate button: {e}"
                })
                continue

            # Wait for a short duration to allow the response to start generating
            logging.info(f"Waiting 5 seconds for Prompt {idx} response to generate.")
            time.sleep(5)

            # Use the fixed XPath to extract the response text
            xpath = fixed_xpaths.get(idx)
            if not xpath:
                logging.error(f"No fixed XPath defined for Prompt {idx}.")
                responses.append({
                    'prompt': prompt,
                    'answer': "❌ No XPath defined for this prompt."
                })
                continue

            response_text = wait_for_full_response(driver, xpath, timeout=180)
            if response_text:
                responses.append({
                    'prompt': prompt,
                    'answer': response_text
                })
                logging.info(f"Successfully captured response for Prompt {idx}.")
            else:
                responses.append({
                    'prompt': prompt,
                    'answer': f"❌ Unable to capture response for Prompt {idx}."
                })

            # Wait 5 seconds before sending the next prompt
            logging.info(f"Waiting 5 seconds before sending the next prompt.")
            time.sleep(5)

        # After collecting all responses, wait 30 seconds before returning
        logging.info("All prompts processed. Waiting 30 seconds before finalizing responses.")
        time.sleep(30)
        return responses

    except Exception as e:
        logging.error(f"An unexpected error occurred in process_bot: {e}")
        return responses
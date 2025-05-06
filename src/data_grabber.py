from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
from src.configs import URL

# FOR LOCAL DEV
from dotenv import load_dotenv

load_dotenv()


# --- Setup ---
USERNAME = os.getenv("PPL_USERNAME")
PASSWORD = os.getenv("PPL_PWD")


def get_data():
    # Launch browser
    driver = webdriver.Chrome()  # or webdriver.Firefox() if you have geckodriver
    driver.get(URL)

    # Wait for page to load
    time.sleep(3)

    # Example: find the email field
    email_field = driver.find_element(By.NAME, "Email Address")
    email_field.send_keys(USERNAME)
    email_field.send_keys(Keys.RETURN)

    time.sleep(2)

    # Example: find the PASSWORD field
    password_field = driver.find_element(By.NAME, "Password")
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    # --- Done: at this point you should be logged in ---

    time.sleep(25)
    select_box = driver.find_element(By.CLASS_NAME, "select-text")
    select_box.click()

    time.sleep(10)
    timesheet_tab = driver.find_element(By.LINK_TEXT, "Timesheet")
    timesheet_tab.click()

    wait = WebDriverWait(driver, 10)

    # Wait for table to load
    table_body = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//table[contains(@class, 'p-datatable-table')]//tbody")
        )
    )
    rows = table_body.find_elements(By.TAG_NAME, "tr")

    datapoints = []

    for index, row in enumerate(rows):
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 8:
            data = {
                "pa_name": cols[0].text.strip(),
                "pa_ppl_id": cols[1].text.strip(),
                "service_date": cols[2].text.strip(),
                "time_in": cols[3].text.strip(),
                "time_out": cols[4].text.strip(),
                "payroll_start_date": cols[5].text.strip(),
                "payroll_end_date": cols[6].text.strip(),
                "status": cols[7].text.strip(),
            }
            datapoints.append(data)

            # Click the View button (usually the last td)
            # view_button = row.find_element(By.XPATH, ".//button[contains(text(), 'View')]")
            # view_button.click()

            # # Wait for submission detail modal/page
            # submission_date = wait.until(
            #     EC.presence_of_element_located(
            #         (
            #             By.XPATH,
            #             "//th[div[contains(text(), 'Submission Date')]]/following-sibling::td/span",
            #         )
            #     )
            # ).text.strip()

            # billed_units = wait.until(
            #     EC.presence_of_element_located(
            #         (
            #             By.XPATH,
            #             "//th[div[contains(text(), 'Billed Units')]]/following-sibling::td/span",
            #         )
            #     )
            # ).text.strip()

            # data["Submission Date"] = submission_date
            # data["Billed Units"] = billed_units

            # print(data)

            # # Close modal or go back, depending on UI
            # close_button = wait.until(
            #     EC.element_to_be_clickable(
            #         (
            #             By.XPATH,
            #             "//button[contains(text(), 'Close') or contains(@aria-label, 'Close')]",
            #         )
            #     )
            # )
            # close_button.click()

            # # Wait for table to be ready again
            # table_body = wait.until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, "//table[contains(@class, 'p-datatable-table')]//tbody")
            #     )
            # )
            # rows = table_body.find_elements(By.TAG_NAME, "tr")

    return datapoints

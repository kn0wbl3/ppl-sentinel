import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import os
from src.configs import URL

logger = logging.getLogger(__name__)


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
    logger.debug("email successful")

    time.sleep(2)

    # Example: find the PASSWORD field
    password_field = driver.find_element(By.NAME, "Password")
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)
    logger.debug("password successful")
    # --- Done: at this point you should be logged in ---

    time.sleep(15)
    select_box = driver.find_element(By.CLASS_NAME, "select-text")
    select_box.click()
    logger.debug("box click successful")

    time.sleep(10)
    timesheet_tab = driver.find_element(By.LINK_TEXT, "Timesheet")
    timesheet_tab.click()
    logger.debug("timesheet click successful")

    # wait = WebDriverWait(driver, 15)
    logger.info("so far so good")
    time.sleep(10)

    html = driver.page_source

    # Optional: Save to a file
    with open("rendered_page.html", "w", encoding="utf-8") as f:
        f.write(html)

    driver.quit()
    logger.debug("html grabbed")


def html_scrubber():
    datapoints = []
    # Load your HTML file or string
    with open("rendered_page.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find the table by ID
    table = soup.find("table", id="pn_id_1-table")

    # Get all rows from the tbody
    rows = table.find("tbody").find_all("tr")
    for row in rows:
        tds = row.find_all("td")
        cols = [td.get_text(strip=True) for td in tds]
        datapoints.append(
            {
                "pa_name": cols[0],
                "pa_ppl_id": cols[1],
                "service_date": cols[2],
                "time_in": cols[3],
                "time_out": cols[4],
                # "payroll_start_date": cols[5],
                # "payroll_end_date": cols[6],
                "status": cols[5],
            }
        )
    return datapoints
    # # Extract and print the text from each cell
    # for row in rows:
    #     cells = [td.get_text(strip=True) for td in row.find_all("td")]
    #     print(cells)

    # Wait for table to load
    # table_body = wait.until(
    #     EC.presence_of_element_located(
    #         (
    #             By.XPATH,
    #             "//div[@id='pn_id_1']//table[contains(@class, 'p-datatable-table')]//tbody",
    #         )
    # (By.XPATH, "//tbody[contains(@class, 'p-datatable-tbody')]")
    # (By.XPATH, "//table[contains(@class, 'p-datatable-table')]//tbody")
    # (
    #     By.XPATH,
    #     "//table[contains(@class, 'p-datatable-scrollable-table')]/following::tbody[contains(@class, 'p-datatable-tbody')]",
    # )
    #     )
    # )

    # wait.until(EC.presence_of_element_located((By.XPATH, "//th[div[text()='PA Name']]")))

    # rows = table_body.find_elements(By.TAG_NAME, "tr")
    # logger.info(rows)

    # datapoints = []
    # time.sleep(4)
    # for index, row in enumerate(rows):
    #     cols = row.find_elements(By.TAG_NAME, "td")
    #     if len(cols) >= 8:
    # data = {
    #     "pa_name": cols[0],
    #     "pa_ppl_id": cols[1],
    #     "service_date": cols[2],
    #     "time_in": cols[3],
    #     "time_out": cols[4],
    #     "payroll_start_date": cols[5],
    #     "payroll_end_date": cols[6],
    #     "status": cols[7],
    # }
    #         datapoints.append(data)

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

    # return datapoints

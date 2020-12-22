import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as check
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


from ..db_utils.db_queries import sql_insert_weather_report, sql_get_remaining_dates
from ..db_utils.mysql_db_connection import get_mysql_connection


GECKODRIVER_PATH = '/Users/mikelawrence/Downloads/geckodriver'

weather_css_selectors = {
    "high":          "tbody.ng-star-inserted:nth-child(2) > tr:nth-child(1) > td:nth-child(2)",
    "low":           "tbody.ng-star-inserted:nth-child(2) > tr:nth-child(2) > td:nth-child(2)",
    "avg":           "tbody.ng-star-inserted:nth-child(2) > tr:nth-child(3) > td:nth-child(2)",
    "precipitation": "tbody.ng-star-inserted:nth-child(4) > tr:nth-child(1) > td:nth-child(2)",
    "visibility":    "tbody.ng-star-inserted:nth-child(8) > tr:nth-child(2) > td:nth-child(2)",
    "wind_max":      "tbody.ng-star-inserted:nth-child(8) > tr:nth-child(1) > td:nth-child(2)",
    "sea_pressure":  "tbody.ng-star-inserted:nth-child(10) > tr:nth-child(1) > td:nth-child(2)"
}

targets = ['low', 'avg', 'high', 'precipitation', 'visibility', 'wind_max', 'sea_pressure']


def extract_text_css_path(driver, field):
    css_selector = weather_css_selectors[field]
    return driver.find_element_by_css_selector(css_selector).text


def scrape_weather_page(weather_url):
    options = Options()
    options.headless = True

    timeout = 15
    with webdriver.Firefox(executable_path=GECKODRIVER_PATH, options=options) as driver:
        try:
            driver.get(weather_url)
            element_present = check.presence_of_element_located((By.CSS_SELECTOR, weather_css_selectors['high']))
            WebDriverWait(driver, timeout).until(element_present)
            weather_data = {field: float(extract_text_css_path(driver, field)) for field in targets}
        except Exception as e:
            print(f"failed to collect data for url {weather_url}")
            raise e

    return weather_data


if __name__ == "__main__":
    weather_station_code = "KSAN"
    SCRAPE_DELAY = 5

    db = get_mysql_connection()

    remaining_dates = sql_get_remaining_dates(db)
    date_count      = len(remaining_dates)

    for iteration, date in enumerate(remaining_dates):
        if iteration % 5 == 0:
            print(f"Finished {iteration} of {date_count}")
        day   = date.day
        month = date.month
        year  = date.year
        formatted_date = f"{year}-{month}-{day}"
        weather_history_url = f"https://www.wunderground.com/history/daily/us/ca/san-diego/{weather_station_code}/date/{formatted_date}"

        try:
            weather_data = scrape_weather_page(weather_history_url)
            sql_insert_weather_report(db, formatted_date, **weather_data)
            time.sleep(SCRAPE_DELAY)
        except Exception as e:
            print(f"failed to get weather data for date {formatted_date} with error {e}")

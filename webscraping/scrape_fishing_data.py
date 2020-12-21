import re
import logging
import requests
import time

from ..db_utils.db_queries import sql_insert_fishing_report, sql_get_completed_fishing_report_links
from ..db_utils.mysql_db_connection import get_mysql_connection

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_table_rows(page_number):
    base_url  = "https://www.fishreports.com/embed/independence-fishreports.php?page={}"
    page_html = requests.get(base_url.format(page_number))
    soup = BeautifulSoup(page_html.text)
    # get table rows (these contain fish report)
    rows = soup.find_all('tr')

    # trim header and footer, even if the page has less than 10 posts
    rows = rows[2:]
    rows = rows[:-1]

    return rows


def extract_fish_report(report_row):
    # get needed data from row
    date, description = report_row.find_all('td')
    date = date.text
    main_post_link = description.find_all('a', href=True)[0].get('href', None).replace("\\", "/")

    # grab the main post and extract its post text
    main_post_content = requests.get(main_post_link)
    main_post = BeautifulSoup(main_post_content.text)
    headline = main_post.find_all("p", attrs={'class': "text-center lead"})[0].text

    main_post_text = main_post.find_all("div", attrs={"class": "report_descript_data"})[0]

    # not all paragraphs are in a <p> tag for whatever reason... hack it!
    try:
        main_post_text = main_post_text.p.text.strip()
    except AttributeError:
        main_post_text = main_post_text.text.strip()
    except Exception as e:
        print(f"Failed to extract text body for {headline}, date {date}")
        raise e

    return date, headline, main_post_link, main_post_text


def clean_string(target_string):
    # get rid of punctuation and other useless info
    return re.sub(r'\W+', ' ', target_string.replace("'", "")).strip()


if __name__ == "__main__":
    # in seconds. be nice to their website
    db = get_mysql_connection()
    completed_links = sql_get_completed_fishing_report_links(db)

    scrape_delay = 3

    first_page   = 1
    highest_page = 302
    # you can adjust final page if you dont want the whole dataset. This takes awhile, after all
    final_page   = highest_page

    for page in range(first_page, final_page + 1):
        if page % 5 == 0:
            print(f"Starting page", page)
        data_rows = get_table_rows(page_number=page)
        for entry in data_rows:
            time.sleep(scrape_delay)
            try:
                date, headline, main_post_link, main_post_text = extract_fish_report(entry)
                if main_post_link not in completed_links:
                    main_post_text = clean_string(main_post_text)
                    headline       = clean_string(headline)
                    sql_insert_fishing_report(db_obj=db, date=date, headline=headline, post_url=main_post_link,
                                              post_body=main_post_text)
                else:
                    print(f"Already completed for date {date}")
            except Exception as e:
                # this errors out for bad scraping.
                # error handling on the sql_insert should be clean and handle errors gracefully
                print("***** ERROR ***** \n\n", entry)
                raise e

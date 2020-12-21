import logging
import pandas as pd

logger = logging.getLogger(__name__)


# TODO: refactor insertions into def safe_insert(db_obj, query):
def sql_insert_weather_report(db_obj, date, high, low, avg, precipitation, visibility, wind_max, sea_pressure):
    weather_insert_query = ("INSERT INTO weather_reports "
                            "(date, high_temp, low_temp, avg_temp, inches_precip, miles_visible, max_wind, sea_pressure) " 
                            "VALUES "
                            f'(STR_TO_DATE("{date}", "%Y-%m-%d"), "{high}", "{low}", "{avg}", "{precipitation}", "{visibility}", "{wind_max}", "{sea_pressure}")')
    cursor = db_obj.cursor()
    try:
        cursor.execute(weather_insert_query)
        db_obj.commit()
        print(f"Finished for date {date}")
    except Exception as e:
        print(f"failed to run query \n {weather_insert_query} \n with error {e}\n\n")
        db_obj.rollback()
        print(f"failed to upload data for date {date}")
    finally:
        cursor.close()


def sql_insert_fishing_report(db_obj, date, headline, post_url, post_body):
    fishing_insert_query = ("INSERT INTO fishing_reports "
                            "(date_posted, headline, post_url, post_body) " 
                            "VALUES "
                            f'(STR_TO_DATE("{date}", "%m-%d-%Y"), "{headline}", "{post_url}", "{post_body}")')
    cursor = db_obj.cursor()
    try:
        cursor.execute(fishing_insert_query)
        db_obj.commit()
    except Exception as e:
        print(f"failed to run query \n\n {fishing_insert_query} \n\n with error {e}")
        db_obj.rollback()
        print(f"failed to upload data for date {date} with headline {headline}")
    finally:
        cursor.close()
    print(f"Finished for date {date} with headline {headline}")


def sql_get_completed_fishing_report_links(db_obj):
    cursor = db_obj.cursor()

    cursor.execute("SELECT * FROM fishing_reports;")

    # 'fetchall()' method fetches all the rows from the last executed statement
    completed_rows = cursor.fetchall()
    return set(list(map(lambda x: x[3], completed_rows)))


def sql_all_reports_with_weather(db_obj):
    weather_columns = ["low_temp", "avg_temp", "high_temp",
                       "inches_precip", "miles_visible", "max_wind",
                       "sea_pressure"]

    fishing_columns = ["date_posted", "headline", "post_body"]

    weather_columns_sql = ", ".join([f"weather_reports.{field}" for field in weather_columns])
    fishing_columns_sql = ", ".join([f"fishing_reports.{field}" for field in fishing_columns])

    join_query = f"""
    SELECT {fishing_columns_sql}, {weather_columns_sql}
    FROM fishing_reports 
    INNER JOIN weather_reports ON weather_reports.date=fishing_reports.date_posted;
    """
    return pd.read_sql(sql=join_query, con=db_obj)

import mysql.connector as mysql
import json


def get_mysql_connection():
    with open("../mysql_config/config.json", "r") as credential_handle:
        sql_creds = json.load(credential_handle)

    db = mysql.connect(
        host     = sql_creds['host'],
        user     = sql_creds['username'],
        password = sql_creds['password'],
        use_pure = True,
        database = "sportfishing"
    )
    return db

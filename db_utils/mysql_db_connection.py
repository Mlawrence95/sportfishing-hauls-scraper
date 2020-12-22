import json
import os

import mysql.connector as mysql
from db_utils.os_utils import get_project_dir


def get_mysql_connection():
    credential_path = os.path.join(get_project_dir(), "..", "mysql_config", "config.json")
    with open(credential_path, "r") as credential_handle:
        sql_creds = json.load(credential_handle)

    db = mysql.connect(
        host     = sql_creds['host'],
        user     = sql_creds['username'],
        password = sql_creds['password'],
        use_pure = True,
        database = "sportfishing"
    )
    return db

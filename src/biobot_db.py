import os
import sqlite3

class BioBotDB():
    def __init__(
        self
    ):
        #
        # sql commands
        #
        cls.create_table = (
            "CREATE TABLE IF NOT EXISTS BIOBOT_ENTRIES ("
            "SLACK_ID VARCHAR(64) NOT NULL, "
            "NAME VARCHAR(64) NOT NULL, "
            "COMPANY_ROLE VARCHAR(64) NOT NULL, "
            "BIO TEXT NOT NULL"
            ")"
        )

        cls.sqlite_path = os.getenv("HOME") + "/biobot_sqlite.db"

        #
        # Connect to sqlite database
        #
        cls.conn = sqlite3.connect(sqlite_path)
        cls.conn.text_factory = str
        cls.cursor = cls.conn.cursor()

        #
        # Create table
        #
        cls.cursor.execute(create_table)
        cls.conn.commit()

    def delete_bio_db(slack_id):
        # constructing delete command
        delete_cmd = "DELETE FROM BIOBOT_ENTRIES WHERE SLACK_ID='{}'".format(slack_id)

        #
        # execute delete command
        #
        cls.cursor.execute(delete_cmd)
        cls.conn.commit()

    def insert_bio_db(slack_id, name, company_role, bio):
        insert_cmd = (
            "insert into BIOBOT_ENTRIES ("
            "SLACK_ID,"
            "NAME,"
            "COMPANY_ROLE,"
            "BIO"
            ") "
            "values (?, ?, ?, ?, ?)"
        )

        params = (
            slack_id,
            name,
            company_role,
            bio
        )

        cls.cursor.execute(insert_cmd, params)
        cls.conn.commit()

    def select_bio_db(slack_id):
        select_cmd = (
            "SELECT * FROM BIOBOT_ENTRIES WHERE SLACK_ID='{}'".format(slack_id)
        )

        cls.cursor.execute(select_cmd)
        cls.conn.commit()

        message = (
            "Name: {}\n"
            "Role: {}\n"
            "Biography: {}"
        ).format(cls.cursor.fetchone()[1], cls.cursor.fetchone()[2], cls.cursor.fetchone()[3])

        return message


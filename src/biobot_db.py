import os
import sqlite3

class BioBotDB():
    def __init__(
        self
    ):
        #
        # sql commands
        #
        self.create_table = (
            "CREATE TABLE IF NOT EXISTS BIOBOT_ENTRIES ("
            "SLACK_ID VARCHAR(64) NOT NULL, "
            "NAME VARCHAR(64) NOT NULL, "
            "COMPANY_ROLE VARCHAR(64) NOT NULL, "
            "BIO TEXT NOT NULL, "
            "PICTURE BLOB NOT NULL"
            ")"
        )

        self.sqlite_path = os.getenv("HOME") + "/biobot_sqlite.db"

        #
        # Connect to sqlite database
        #
        self.conn = sqlite3.connect(self.sqlite_path)
        self.conn.text_factory = str
        self.cursor = self.conn.cursor()

        #
        # Create table
        #
        self.cursor.execute(self.create_table)
        self.conn.commit()

    def delete_bio_db(self, slack_id):
        # constructing delete command
        delete_cmd = "DELETE FROM BIOBOT_ENTRIES WHERE SLACK_ID='{}'".format(slack_id)

        #
        # execute delete command
        #
        self.cursor.execute(delete_cmd)
        self.conn.commit()

    def insert_bio_db(self, slack_id, name, company_role, bio, img):
        insert_cmd = (
            "insert into BIOBOT_ENTRIES ("
            "SLACK_ID,"
            "NAME,"
            "COMPANY_ROLE,"
            "BIO, "
            "PICTURE"
            ") "
            "values (?, ?, ?, ?, ?)"
        )

        params = (
            slack_id,
            name,
            company_role,
            bio,
            img
        )

        self.cursor.execute(insert_cmd, params)
        self.conn.commit()

    def select_bio_db(self, slack_id):
        select_cmd = (
            "SELECT * FROM BIOBOT_ENTRIES WHERE SLACK_ID='{}'".format(slack_id)
        )

        self.cursor.execute(select_cmd)
        self.conn.commit()

        message = (
            "Name: {}\n"
            "Role: {}\n"
            "Biography: {}"
        ).format(self.cursor.fetchone()[1], self.cursor.fetchone()[2], self.cursor.fetchone()[3])

        return [cursor.fetchone()[4], message]


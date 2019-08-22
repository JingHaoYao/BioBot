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
            "BIO TEXT NOT NULL "
            ")"
        )
        self.sqlite_path = "/tmp/biobot_sqlite.db"

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

    def insert_bio_db(self, slack_id, name, company_role, bio):
        select_cmd = (
            "SELECT * FROM BIOBOT_ENTRIES WHERE SLACK_ID='{}'".format(slack_id)
        )

        self.cursor.execute(select_cmd)
        self.conn.commit()
        if self.cursor.fetchone() is not None:
            self.delete_bio_db(slack_id)
        
        insert_cmd = (
            "insert into BIOBOT_ENTRIES ("
            "SLACK_ID,"
            "NAME,"
            "COMPANY_ROLE,"
            "BIO "
            ") "
            "values (?, ?, ?, ?)"
        )

        params = (
            slack_id,
            name,
            company_role,
            bio
        )

        self.cursor.execute(insert_cmd, params)
        self.conn.commit()

    def select_bio_db(self, slack_id):
        select_cmd = (
            "SELECT * FROM BIOBOT_ENTRIES WHERE SLACK_ID='{}'".format(slack_id)
        )

        self.cursor.execute(select_cmd)
        self.conn.commit()

        message = None
        image_bin = None
        data = self.cursor.fetchone()
        if data is not None:
            message = (
                "Name: {}\n"
                "Role: {}\n"
                "Biography: {}"
            ).format(data[1], data[2], data[3])
        else:
            message = "No biography to display."

        return image_bin, message


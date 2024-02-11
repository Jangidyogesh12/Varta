import sqlite3
import numpy as np
from loguru import logger


"""
This class is created to perform the basic crude operations on the database
"""


class CRUD:

    def __init__(
        self,
        table_name,
        path: str = "src/rag_search/database/database.db",
    ):
        self.table_name = table_name
        self.path = path
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()

    def create(self):

        self.cur.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table_name}(chunk TEXT PRIMARY KEY, embedding_data BLOB)"
        )

        self.con.commit()

    def insert(self, key: str, value: list):
        """
        Insert data into the table.

        Store the embedding in the database
        """
        self.create()
        value = np.array(value).astype(np.float32).tobytes()
        try:
            # Insert the embedding into the database
            self.cur.execute(
                f"INSERT INTO {self.table_name} (chunk, embedding_data) VALUES (?,?)",
                (key, value),
            )
            self.con.commit()

        except sqlite3.Error as e:
            # Handle unique constraint violation
            logger.error(f"Insertion failed: {e}")
            # Here you might choose to ignore the error, update the existing row, or abort the transaction

    def get_embedding(self, key: str):
        """
        returns the value stored correspondig to particular key
        """
        try:
            self.cur.execute(
                f"SELECT embedding_data FROM {self.table_name} WHERE chunk = ?", (key,)
            )
            rows = self.cur.fetchall()
            for row in rows:
                embedding = np.frombuffer(row[0], np.float32)
                return embedding

        except sqlite3.Error as e:
            logger.error(f"Key not found: {e}")

    def get_data(self):
        self.cur.execute(f"SELECT embedding_data FROM {self.table_name}")
        data = self.cur.fetchall()
        embeddings = []
        for row in data:
            embeddings.append(np.frombuffer(row[0], np.float32))
        return np.array(embeddings)

    def delete_row(self, key: str):
        try:
            # Construct and execute the DELETE SQL statement using parameterized query
            self.cur.execute(f"DELETE FROM {self.table_name} WHERE chunk = ?", (key,))

            # Get the number of rows affected by the DELETE statement
            rows_deleted = self.cur.rowcount

            # Commit the transaction to make the changes permanent
            self.con.commit()

            if rows_deleted == 0:
                # If no rows were deleted, print an error message
                logger.error(f"The key '{key}' does not exist in the database table")

            else:
                # Print a success message
                logger.info("The data has been successfully deleted")

        except sqlite3.Error as e:
            # Handle any errors that occur during the deletion process
            logger.error(f"An error occured:{e}")

    def clear_database(self):
        """
        This function deletes all the table creted inside the database

        - we are using DROP feature of the sqlite3 to do this
        """
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()
        for table in tables:
            self.cur.execute(f"DROP TABLE {table[0]};")
        self.con.commit()

    def clear_tables(self):
        """
        This function deletes all the table data inserted inside the tables

        - we are using DELETE feature of the sqlite3 to do this
        """
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()
        for table in tables:
            self.cur.execute(f"DELETE FROM {table[0]};")
        self.con.commit()

    def is_empty(self):
        """
        This function check if the databse is Empty or not
        """
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()
        return len(tables == 0)

    def close_db(self):
        """
        This function closes the database
        """
        self.con.close()
        logger.info("The database has been closed")

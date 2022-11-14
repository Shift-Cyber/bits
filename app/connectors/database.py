import mysql.connector
import logging
import os


# local imports
from structures.user import User


class Database:
    def __init__(self):
        self.host          = os.environ.get("DB_HOST", None)
        self.username      = os.environ.get("DB_USER", None) or "root"
        self.password      = os.environ.get("DB_PASS", None)
        self.database_name = os.environ.get("DB_NAME", None) or "hack_a_bit"

        self.__connect__()


    def __connect__(self) -> None:
        self.connector = mysql.connector.connect(host = self.host,
                                                 user = self.username,
                                                 password = self.password,
                                                 database = self.database_name)
        
        if self.connector.is_connected():
            logging.info(f"connected to MySQL server, version '{self.connector.get_server_info()}'")


    def lookup_user_email(self, email:str) -> User:
        try:
            # determine all registered user's uids
            cursor = self.connector.cursor(prepared=True)
            query_user_by_id = """SELECT * FROM users WHERE email=%s"""

            user_tuple = cursor.execute(query_user_by_id, email)
            cursor.close()

            if user_tuple:
                return User(*user_tuple)
            else:
                return None

        except Exception as e:
            logging.error("Error while connecting to MySQL", e)
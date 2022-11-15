import mysql.connector
import logging
import os


# local imports
from structures.user import User
from structures.token_record import TokenRecord


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

            cursor.execute(query_user_by_id, (email,))
            user_tuple = cursor.fetchone()

            cursor.close()

            if user_tuple:
                return User(*user_tuple)
            else:
                return None

        except Exception as e:
            logging.error("Error while connecting to MySQL", e)


    def save_token(self, token:str, email:str, issued_epoch:str) -> None:
        try:
            cursor = self.connector.cursor(prepared=True)

            query_save_token = """INSERT INTO email_tokens
                                  (token, email, issued_epoch)
                                  VALUE (%s, %s, %s)"""
            
            cursor.execute(query_save_token,
                                (token,
                                 email,
                                 issued_epoch)
                        )

            self.connector.commit()

            cursor.close()

        except Exception as e:
            logging.error("Error while connecting to MySQL", e)


    def get_token_record(self, token:str) -> tuple:
        try:
            cursor = self.connector.cursor(prepared=True)
            query_token = """SELECT * FROM email_tokens WHERE token=%s"""

            cursor.execute(query_token, (token,))
            token_tuple = cursor.fetchone()

            cursor.close()

            if token_tuple:
                return TokenRecord(*token_tuple)
            else:
                return None

        except Exception as e:
            logging.error("Error while connecting to MySQL", e)



"""
# connect to GCP database for bits user context
    bits_connector = mysql.connector.connect(
        host     = os.environ.get("BITS_DB_HOST", None),
        port     = os.environ.get("BITS_DB_PORT", None) or 3306,
        user     = os.environ.get("BITS_DB_USER", None),
        password = os.environ.get("BITS_DB_PASS", None),
        database = os.environ.get('BITS_DB', None) or "hack_a_bit"
    )

    if not bits_connector.is_connected(): logging.error("Error connecting to bits database") and exit(-1)

    #format query
    cursor = bits_connector.cursor(prepared=True)
    query_create_user = ""INSERT INTO users
                           (user_id, first_name, last_name, email, registered)
                           VALUES (%s,%s,%s,%s,%s)""




    #execute query
    cursor.execute(query_create_user,
                    (user.uid,
                     user.first_name,
                     user.last_name,
                     user.email,
                     user.registered))
    bits_connector.commit()
    cursor.close()
    bits_connector.close()
"""
# python native imports
import os
import time
import logging
from dataclasses import dataclass
from threading import Thread

# third party imports
import mysql.connector

THREAD_COUNT = os.environ.get("THREAD_COUNT", None) or 25

# structures
@dataclass
class User:
    uid: int
    first_name: str
    last_name: str
    email: str
    registered: bool


# connect to arcustech database for craft user context
craft_connector = mysql.connector.connect(
    host     = os.environ.get("ARC_HOST", None) or "127.0.0.1",
    port     = os.environ.get("ARC_PORT", None) or 3336,
    user     = os.environ.get("ARC_DB_USER", None),
    password = os.environ.get("ARC_DB_PASS", None),
    database = f"{os.environ.get('ARC_DB_USER', None)}_craft"
)


# verify database connections
if not craft_connector.is_connected(): logging.error("Error connecting to craft database") and exit(-1)


# record a new user in the bits user database
def create_user(user:User) -> None:
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
    query_create_user = """INSERT INTO users
                           (user_id, first_name, last_name, email, registered)
                           VALUES (%s,%s,%s,%s,%s)"""

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

# update an existing user in the bits user database
def update_user(user:User) -> None:
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
    query_update_user = """UPDATE users 
                        SET first_name = %s, last_name = %s, email = %s, registered = %s
                        WHERE user_id = %s"""

    #execute query
    cursor.execute(query_update_user,
                    (user.first_name,
                     user.last_name,
                     user.email,
                     user.registered,
                     user.uid,))
    bits_connector.commit()
    cursor.close()
    bits_connector.close()


# lookup a user in the bits user database
def lookup_user(user:User) -> User:
    # connect to GCP database for bits user context
    bits_connector = mysql.connector.connect(
        host     = os.environ.get("BITS_DB_HOST", None),
        port     = os.environ.get("BITS_DB_PORT", None) or 3306,
        user     = os.environ.get("BITS_DB_USER", None),
        password = os.environ.get("BITS_DB_PASS", None),
        database = os.environ.get('BITS_DB', None) or "hack_a_bit"
    )

    if not bits_connector.is_connected(): logging.error("Error connecting to bits database") and exit(-1)

    # format query
    cursor = bits_connector.cursor(prepared=True)
    query_create_user = """SELECT * FROM users WHERE user_id = %s"""
    
    # execute query
    cursor.execute(query_create_user, (user.uid,))
    user_tuple = cursor.fetchone()

    cursor.close()
    bits_connector.close()

    # expand the tuple into the User object and return it
    if user_tuple: return User(*user_tuple)
    else: return None



def get_users() -> list:
    # determine all registered user's uids
    cursor = craft_connector.cursor(prepared=True)
    query_registered_userIds = """SELECT userId FROM usergroups_users WHERE groupId=1"""


    cursor.execute(query_registered_userIds)
    registered_userIds = [ uid[0] for uid in cursor.fetchall() ]
    

    # determine all existing users
    cursor = craft_connector.cursor(prepared=True)
    query_users = """SELECT * FROM users"""

    cursor.execute(query_users)
    users = cursor.fetchall()

    
    # analyze and structure the data
    return [
        User( first_name = user[3], last_name = user[4],
            email = user[5], uid = user[0], registered = True )

            if user[0] in registered_userIds else

        User( first_name = user[3], last_name = user[4],
            email = user[5], uid = user[0], registered = False )
            
            for user in users 
        ]


def thread_process_user(user:User) -> None:
    # try to get record of this user in bits db, by uid
    bits_user_lookup = lookup_user(user)

    # if user doesnt exist create the record
    if not bits_user_lookup:
        print(f"couldnt find {(user)} in bits db, creating...")
        create_user(user)

    # uid exists, verify that the record completly matches the current craft entry
    else: 
        print(f"found user {(user)}, not creating")
        print(f"current record: {bits_user_lookup}")

        if (user.uid != int(bits_user_lookup.uid)) or\
            (user.first_name != bits_user_lookup.first_name) or\
            (user.last_name != bits_user_lookup.last_name) or\
            (user.email != bits_user_lookup.email) or\
            (user.registered != bool(bits_user_lookup.registered)):
           print(f"something changed for user {bits_user_lookup}, updating...")
           update_user(user)

while True:
    try:
        # retreive all users on server
        users = get_users()

        # parse through users
        jobs = [ Thread(target=thread_process_user, args=(user,)) for user in users ]

        for index, job in enumerate(jobs):
            job.start()

            if (index % THREAD_COUNT) == 0 or ((len(jobs) - index) < THREAD_COUNT):
                job.join()

            
                
    except Exception as err:
        print("Error while connecting to MySQL:", err)
        exit()

    # pause for some amount of time, specified in the environment
    sleep_time = os.environ.get("WORKER_INTERVAL_SEC", None)
    print(f"sleeping for {sleep_time}")
    time.sleep(int(sleep_time))

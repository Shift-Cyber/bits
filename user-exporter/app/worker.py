# python native imports
import os
import sys
import time
import logging
from dataclasses import dataclass
from threading import Thread

# third party imports
import mysql.connector
import google.cloud.logging

THREAD_COUNT = int(os.environ.get("THREAD_COUNT", None)) or 5
LOG_LOCAL = os.environ.get("LOG_LOCAL", 0)


# logging configuration, local or remote
if int(LOG_LOCAL):
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d (%(levelname)s | %(filename)s:%(lineno)d) - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("logging set to stdout rather than GCP")
else: google.cloud.logging.Client().setup_logging()


# structures
@dataclass
class User:
    uid: int
    first_name: str
    last_name: str
    email: str
    registered: bool
    discord_id: int

# connect to ARCUSTECH database
def connect_to_craft():
    logging.info('Connecting to craft DB')
    return mysql.connector.connect(
        host     = os.environ.get("ARC_HOST", None) or "127.0.0.1",
        port     = os.environ.get("ARC_PORT", None) or 3336,
        user     = os.environ.get("ARC_DB_USER", None),
        password = os.environ.get("ARC_DB_PASS", None),
        database = f"{os.environ.get('ARC_DB_USER', None)}_craft"
    )

# connect to local BITS database
def connect_to_bits():
    logging.info('Connecting to Bits DB')
    return mysql.connector.connect(
        host     = os.environ.get("BITS_DB_HOST", None),
        port     = os.environ.get("BITS_DB_PORT", None) or 3306,
        user     = os.environ.get("BITS_DB_USER", None),
        password = os.environ.get("BITS_DB_PASS", None),
        database = os.environ.get('BITS_DB', None) or "bits"
    )

# record a new user in the bits user database
def create_bits_user(bits_connector, user:User) -> None:
    # ensure connector is established
    if not bits_connector.is_connected():
        logging.warning("Connector not connected, attempting to reconnect")
        bits_connector = connect_to_bits()

    #format query
    cursor = bits_connector.cursor(prepared=True)
    query_create_bits_user = """INSERT INTO users
                           (user_id, first_name, last_name, email, registered)
                           VALUES (%s,%s,%s,%s,%s)"""

    #execute query
    cursor.execute(query_create_bits_user,
                    (user.uid,
                     user.first_name,
                     user.last_name,
                     user.email,
                     user.registered))
    bits_connector.commit()
    cursor.close()

# update an existing user in the bits user database
def update_bits_user(bits_connector, craft_user:User) -> None:
    # ensure connector is established
    if not bits_connector.is_connected():
        logging.warning("Connector not connected, attempting to reconnect")
        bits_connector = connect_to_bits()

    #format query
    cursor = bits_connector.cursor(prepared=True)
    query_update_bits_user = """UPDATE users 
                        SET first_name = %s, last_name = %s, email = %s, registered = %s
                        WHERE user_id = %s"""

    #execute query
    logging.info(f"Updating {(craft_user)} in Bits database")
    cursor.execute(query_update_bits_user,
                    (craft_user.first_name,
                     craft_user.last_name,
                     craft_user.email,
                     craft_user.registered,
                     craft_user.uid,))
    bits_connector.commit()
    cursor.close()


# lookup a user in the bits user database
def bits_lookup_user(bits_connector:object, user:User) -> User:
    # ensure connector is established
    if not bits_connector.is_connected():
        logging.warning("Connector not connected, attempting to reconnect")
        bits_connector = connect_to_bits()

    # exit if we still cant connect
    if not bits_connector.is_connected():
        logging.error("Error connecting to bits database, exiting...") and exit(-1)

    # format query
    cursor = bits_connector.cursor(prepared=True)
    query_bits_lookup_user = """SELECT * FROM users WHERE user_id = %s"""
    
    # execute query
    cursor.execute(query_bits_lookup_user, (user.uid,))
    user_tuple = cursor.fetchone()

    cursor.close()

    # expand the tuple into the User object and return it
    if user_tuple: return User(*user_tuple)
    else: return None



def get_arcustech_users(craft_connector:object, bits_connector:object) -> list:
    # ensure the arcustech connector is connected
    if not craft_connector.is_connected():
        logging.error("Error connecting to arcustech database, trying to reconnect")
        craft_connector = connect_to_craft()

    # determine all registered user's uids
    cursor = craft_connector.cursor(prepared=True)
    query_craft_uids = """SELECT userId FROM usergroups_users WHERE groupId=1"""

    cursor.execute(query_craft_uids)
    craft_uids = [ uid[0] for uid in cursor.fetchall() ]
    
    # ensure the bits connector is connected
    if not bits_connector.is_connected():
        logging.error("Error connecting to arcustech database, trying to reconnect")
        bits_connector = connect_to_bits()

    # determine all existing users
    cursor = bits_connector.cursor(prepared=True)
    query_users = """SELECT * FROM users"""

    cursor.execute(query_users)
    bits_users = cursor.fetchall()
    
    # analyze and structure the data, list instantiated with switch for registration status
    return [
        User( first_name = user[1], last_name = user[2],
            email = user[3], uid = user[0], registered = True, discord_id = None )

            if user[0] in craft_uids else

        User( first_name = user[1], last_name = user[2],
            email = user[3], uid = user[0], registered = False, discord_id = None )
            
            for user in bits_users 
        ]


def thread_process_user(craft_user:User) -> None:
    bits_connector  = connect_to_bits()

    # try to get record of this user in bits db, by uid
    bits_user = bits_lookup_user(bits_connector, craft_user)
    logging.info(f"Queried user:{craft_user}, resulting in: {bits_user}")


    # if user doesnt exist create the record
    if not bits_user:
        logging.info(f"Couldnt locate {(craft_user.uid)} in current Bits database, creating...")
        create_bits_user(bits_connector, craft_user)

    # uid exists, verify that the record completly matches the current craft entry
    else: 
        logging.info(f"Located {(craft_user)} in Bits database, testing for delta")

        logging.info(f"current record: {bits_user}")

        print()

        if (craft_user.uid != int(bits_user.uid)) or\
            (craft_user.first_name != bits_user.first_name) or\
            (craft_user.last_name != bits_user.last_name) or\
            (craft_user.email != bits_user.email) or\
            (craft_user.registered != bool(bits_user.registered)):
           logging.info(f"Something changed for user {bits_user} in craft, updating bits record...")
           update_bits_user(bits_connector, craft_user)
    
    bits_connector.close()


# establish main thread
while True:
    try:
        bits_connector  = connect_to_bits()
        craft_connector = connect_to_craft()
        
        # retreive all users on server
        users = get_arcustech_users(craft_connector, bits_connector)
        if not users: logging.error('Couldn\'t get users from Arcustech') and exit(-1)

        bits_connector.close()
        craft_connector.close()

        logging.info(f"Retrieved {len(users)} users from the Arcustech CraftCMS database")

        # parse through users and initialize jobs
        jobs = [
            Thread(target=thread_process_user, args=(user,)) for user in users
        ]

        for index, job in enumerate(jobs):
            job.start()

            if (index % THREAD_COUNT) == 0 or ((len(jobs) - index) < THREAD_COUNT):
                job.join()


    except Exception as e:
        logging.error("An unknown error occured:", e) and exit(-1)

    # pause for some amount of time, specified in the environment
    sleep_time = os.environ.get("WORKER_INTERVAL_SEC", None)
    print(f"sleeping for {sleep_time}")
    time.sleep(int(sleep_time))

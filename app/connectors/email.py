# python native imports
import logging
import os

# third party invites
import mysql.connector
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# local imports
from structures.user import User


# environmnet setup
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")


class EmailClient:
    def __init__(self): pass
        
    
    def send_registration_code(self, user:User, token:str):
        
        message = Mail(from_email="noreply@hackabit.com",
            to_emails=user.email,
            subject="Hack a Bit: Discord Registration Code",
            html_content=f"<html><p>Welcome to the Hack a Bit Discord, here's your token: </p><p><b>{token}</b></p><br><p>Now you need to use the register command to sync your accounts by running...</p><p>!register use-token {token}</p></html>")

        try:
            sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
            response = sendgrid_client.send(message)

            logging.info(response.status_code)
            logging.info(response.body)
            logging.info(response.headers)

        except Exception as e:
            logging.error(e.message)


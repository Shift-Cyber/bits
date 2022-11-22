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
SENDGRID_REG     = os.environ.get("SENDGRID_REG")


class EmailClient:
    def send_registration_code(self, user:User, token:str):    
        try:
            # set message addressing
            message = Mail(from_email="noreply@hackabit.com",
                to_emails=user.email,
                subject="Hack a Bit: Discord Registration Code",
            )
            
            # configure template settings
            message.dynamic_template_data = { "registration-code": token }
            message.template_id = SENDGRID_REG

            logging.info(f"sending registration code to: {user.email}")
            
            sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
            response = sendgrid_client.send(message)

            logging.info(f"got response from the sendgrid API [{response.status_code}]")

        except Exception as e:
            logging.error(e.message)

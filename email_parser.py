#!/usr/bin/env python3

"""
The following program demonstrates how to access an email account using imaplib.
You need a valid username, password, and imap host address. Once authenticated, you can access the account folders.
Select the folder you want to retrieve data from, and search for the info you want.
This program gathers the email's sender, recipient, subject, date, and message and returns a summary as a json object.

"""


import email
from getpass import getpass
import imaplib
import json


def get_data(username, password, host):

    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(host)

    # Authenticate for access to email account
    imap.login(username, password)

    # print(imap.list())  # Returns all folders available in email account

    imap.select("INBOX")  # Select "INBOX" folder
    _, messages = imap.search(None, '(FROM "example@host.com")')  # Search for messages from a specific sender

    print("Total number of messages from sender:", len(messages[0].split()))

    summary = []

    # Iterate through each email from the specified sender
    for num in messages[0].split():
        _, data = imap.fetch(num, "(RFC822)")  # Returns entire body of email
        _, bytes = data[0]

        #convert the byte data to HTML message
        email_message = email.message_from_bytes(bytes)

        # Initiate dict to store data from email
        email_dict = {}
        email_dict["Subject: "] = email_message["subject"]
        email_dict["To: "] = email_message["to"]
        email_dict["From: "] = email_message["from"]
        email_dict["Date: "] = email_message["date"]


        for item in email_message.walk():
            if item.get_content_type()=="text/plain" or item.get_content_type()=="text/html":
                message = item.get_payload(decode=True)
                email_dict["Message: "] = message.decode()
                
                break
        
        # Add dict to summary list
        summary.append(email_dict)

    # Convert summary object into json format
    summary = json.dumps(summary, indent = 4)

    return summary



if __name__ == "__main__":

    username = "example@host.com"  # Enter your email here
    password = getpass("Please Enter Your Password: ")  # Input password from command line. Hidden visibility.
    host = "imap.gmail.com"
    print(get_data(username, password, host))



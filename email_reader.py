import imaplib
import email
import os
from datetime import datetime
from config import EMAIL, PASSWORD, IMAP_SERVER


def save_attachment(msg, download_folder="bills"):
    #email sender address
    sender = msg.get("From")
    #Extracts the vendor name and removes angle brackets and extra spaces.
    vendor = sender.split("@")[0].replace("<", "").replace(">", "").strip()

    # Extract Email date 
    #parsedate_tz--Converts the email's "Date" header into a tuple with timezone info.
    date_tuple = email.utils.parsedate_tz(msg["Date"])
    if date_tuple:
        #Converts tuple to Unix timestamp and after converts timestamp to Python datetime object
        local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        #strftime--Formats date as YYYYMM to use in folder names
        folder_date = local_date.strftime("%Y%m")
    else:
        folder_date = "unknown"

    #Construct folder path and Creates the folder if it doesn’t exist already
    folder_path = os.path.join(download_folder, folder_date, vendor)
    os.makedirs(folder_path, exist_ok=True)

    #It store the full paths of all attachments downloaded for this email.
    files = []
    
    # Email can have multiple parts
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        if part.get("Content-Disposition") is None:
            continue
        filename = part.get_filename()
        if filename:
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
            print("Downloaded:", filepath)
            files.append(filepath)
    #Returns all attachments downloaded for that email.
    return files

#Connects to our email inbox and downloads attachments from the last limit emails
def read_emails(limit=10):
    #Connects securely to the IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    #Logs in using your credentials
    mail.login(EMAIL, PASSWORD)
    #Selects the "inbox" folder
    mail.select("inbox")
    #Fetch all emails in the inbox
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()
    #Initialize list to store attachments from all emails
    all_files = []
    #Loop through the last limit emails
    for num in email_ids[-limit:]:
      #Fetch the full email content
        status, msg_data = mail.fetch(num, "(RFC822)")

        for response_part in msg_data:

            if isinstance(response_part, tuple):

                msg = email.message_from_bytes(response_part[1])
                #Print the email subject for tracking
                print("\nProcessing:", msg["Subject"])
                #Here Calls a save_attachment(msg) to download attachments
                files = save_attachment(msg)
                #Add all downloaded files to all_files
                all_files.extend(files)

    mail.logout()

    return all_files
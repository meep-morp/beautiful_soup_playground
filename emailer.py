from dotenv import load_dotenv
from email.message import EmailMessage
import os
import smtplib

load_dotenv()
#  Use os.getenv to access your .env variables

# Options example ->
"""
    options {
        attachments: [],
        subject: "",
        content: [],
        html: "",
    }
"""

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')


def email_file(receiver, options={}):
    # Setup Message
    msg = EmailMessage()
    msg['Subject'] = options['subject']
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver

    msg.set_content(options['content'])

    # Add attachments if available
    if options['attachments']:
        for file in options['attachments']:
            with open(file, 'rb') as f:
                file_data = f.read()
                file_name = f.name

            msg.add_attachment(file_data, file_name, maintype='application',
                               subtype='octet-stream', filename=file_name)

    # Attach HTML if available
    if options['html']:
        msg.add_alternative(options['html'], subtype='html')

    # Sending Message
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("Message Sent.")

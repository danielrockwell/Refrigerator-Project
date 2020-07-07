'''The sendEmail script sends an email of the
    weekly refrigerator report.

    The sendEmail script uses source code from the following GitHub repository:
    https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Emails/mail-demo.py'''
import os
import smtplib
from email.message import EmailMessage
from datetime import date

'''Newly created email address and passwordto send
    the email saved as an environment variable'''
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_APP_PSS')

# The attached Weekly report generated from the report.py script
FILE = f'reports/refrigeratordash_{date.today().strftime("%Y_%m_%d")}.pdf'

msg = msg = EmailMessage()
msg['Subject'] = f'Weekly Refrigerator Reports - {date.today().strftime("%b.%d.%Y")}'
msg['From'] = EMAIL_ADDRESS
msg['To'] = ['valid_email_address']

# Message content
msg.set_content(f"Hello Refrigerator Owner!\n"
                f"Here is a weekly summary for the Refrigerator Usage\n\n"
                )

with open(FILE, 'rb') as f:
    file_data = f.read()
    file_name = f.name

# Add PDF attachment to the email
msg.make_mixed()
msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)


# Sending the email with the message and attachment
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

'''This script sends an SMS when the refrigerator is open for more
    than a certain amount of time (default is 30 seconds in this application).

    This code is from Twilio documentation:
    https://www.twilio.com/blog/2016/10/how-to-send-an-sms-with-python-using-twilio.html'''
from secret import ACCOUNT_SID,AUTH_TOKEN, PHONE_NUMBER
from twilio.rest import Client

client = Client(ACCOUNT_SID,AUTH_TOKEN)

def sendTextMessage(duration, phoneNumber=PHONE_NUMBER):
    try:
        client.messages.create(
            to = phoneNumber,
            from_ = 'NEW PHONE NUMBER CREATED FROM TWILIO ACCOUNT',
            body = f"🔋Your Refrigerator has been left open for {duration:.0f} seconds! Please close the Refrigerator now!!🔌"
            )
        print("Text was successfully sent!")

    except:
        print("Unsuccessful Text")


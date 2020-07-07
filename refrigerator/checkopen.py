import RPi.GPIO as GPIO
from messages import sendTextMessage
from datetime import datetime
import csv
import time

ALLOWED_THRESHOLD_OPEN = 30
ALLOWED_TEXT_MESSAGES = 1

'''The setupRp function uses source code from the following GitHub repository:
    https://github.com/simonprickett/pidoorsensor/blob/master/pidoorsensor1.py'''
def setupRP():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def wasOpenAndIsOpen(wasOpen,nowOpen):
    return wasOpen and nowOpen

def wasClosedButNowOpen(wasOpen,nowOpen):
    return not wasOpen and nowOpen

def wasClosedandIsClosed(wasOpen,nowOpen):
    print("Refrigerator is closed")

def wasOpenButNowClosed(wasOpen,nowOpen):
    return wasOpen and not nowOpen

# The writeToCSV function writes the collected data to an open_log CSV file
def writeToCSV(current_day,elapsed_time):
    date_format = str(current_day.date()).replace("-","_")
    with open(f"/home/pi/4740_project1/logs/open_logs/{date_format}_open_log.csv", "a") as file:
        field_names = ['date','time_opened_seconds']
        writer = csv.DictWriter(file, fieldnames=field_names)

        # Create header for file if new day (new file is created each day)
        if file.tell() < 1:
            writer.writeheader()
        currentTime = current_day.isoformat(sep=' ', timespec='milliseconds')
        writer.writerow({'date': currentTime, 'time_opened_seconds':f'{elapsed_time:.2f}' })

def aboveThreshold(currOpenTime,threshold):
    return currOpenTime > threshold

def sendNotification(numSentTexts, numAllowedTexts, currOpenTime):
    if numSentTexts < numAllowedTexts:
        # TESTING
        # print(f"Sent text message")
        sendTextMessage(currOpenTime)
        numSentTexts+=1
    else:
        # TESTING
        # print(f"OPEN FOR {currOpenTime} SECONDS!!!!!")
        pass

    return numSentTexts


def logAndNotify(allowed_threshold, num_allowed_texts):
    wasOpen = False
    numOfSentTexts = 0

    while True:
        currentDay = datetime.now()
        nowOpen = GPIO.input(18)

        # Check to see if the refrigerator was closed but is now open
        if wasClosedButNowOpen(wasOpen,nowOpen):
            wasOpen = True
            opened_time = time.time()
            # TESTING
            # print("Refrigerator is now open")

        # Check to see if the refrigerator was open and is still open
        elif wasOpenAndIsOpen(wasOpen,nowOpen):
            currentOpenTime = time.time() - opened_time
            # Send text notification if the refrigerator is left open for more than allowed threshold
            if aboveThreshold(currentOpenTime,allowed_threshold):
                numOfSentTexts = sendNotification(numOfSentTexts, ALLOWED_TEXT_MESSAGES, currentOpenTime)
            else:
                # TESTING
                # print("Refrigerator open")
                pass

        # Check to see if the refrigerator was open but is now closed
        elif wasOpenButNowClosed(wasOpen,nowOpen):
            wasOpen = False
            elapsed_time = time.time() - opened_time
            numOfSentTexts = 0
            writeToCSV(currentDay,elapsed_time)
            # TESTING
            # print(f"Refrigerator is now closed and was open for {elapsed_time} seconds")

        # Check to see if the refrigerator was closed and is still closed
        else:
            # TESTING
            # wasClosedandIsClosed(wasOpen,nowOpen)
            pass

        time.sleep(0.1)


def main():
    setupRP()
    logAndNotify(ALLOWED_THRESHOLD_OPEN,ALLOWED_TEXT_MESSAGES)

if __name__ == '__main__':
    main()
